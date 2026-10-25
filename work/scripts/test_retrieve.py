"""Offline reliability tests. Usage: python3 -m unittest discover -s work/scripts -p 'test_*.py'."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import retrieve

class Response:
    status = 200
    headers = {'Content-Type':'application/json'}
    def __init__(self, body=b'{"results":[],"meta":{"count":0}}'):self.body=body
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self):return self.body

class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.runs=Path(self.temp.name);self.run=self.runs/'test';(self.run/'raw').mkdir(parents=True)
        retrieve.save(self.run/'config.json',{'task_budget_credits':300,'max_attempts':3,'timeout_seconds':1})
        self.m={'requests':[],'credits_reserved':0,'queries':{}}
        self.patcher=patch.object(retrieve,'RUNS',self.runs);self.patcher.start();self.addCleanup(self.patcher.stop)
    def manifest(self):retrieve.save(self.run/'manifest.json',self.m)
    def test_task_budget_blocks_before_network(self):
        self.m['credits_reserved']=300;self.manifest()
        with patch('urllib.request.urlopen') as network:
            with self.assertRaisesRegex(RuntimeError,'task_budget'):retrieve.request(self.run,self.m,'/works',{},'secret',10,100)
            network.assert_not_called()
    def test_account_budget_blocks_before_network(self):
        self.manifest()
        with patch('urllib.request.urlopen') as network:
            with self.assertRaisesRegex(RuntimeError,'account_budget'):retrieve.request(self.run,self.m,'/works',{},'secret',10,9)
            network.assert_not_called()
    def test_retries_are_reserved_and_remaining_is_conservative(self):
        self.manifest()
        error=urllib.error.HTTPError('https://api.openalex.org/works',503,'temporary',{},io.BytesIO(b'{}'))
        with patch('urllib.request.urlopen',side_effect=[error,Response()]),patch('time.sleep'):
            _,record=retrieve.request(self.run,self.m,'/works',{},'secret',10,30)
        self.assertEqual(self.m['credits_reserved'],20)
        self.assertEqual(record['conservative_account_remaining_after'],10)
        self.assertEqual([r['status'] for r in self.m['requests']],[503,200])
    def test_retry_after_long_delay_stops_safely(self):
        self.manifest()
        error=urllib.error.HTTPError('https://api.openalex.org/works',429,'limit',{'Retry-After':'120'},io.BytesIO(b'{}'))
        with patch('urllib.request.urlopen',side_effect=error),patch('time.sleep') as sleep:
            with self.assertRaisesRegex(RuntimeError,'retry_after'):retrieve.request(self.run,self.m,'/works',{},'secret',10,100)
            sleep.assert_not_called()
        self.assertEqual(self.m['credits_reserved'],10)
    def test_raw_bytes_and_no_auth_in_request_record(self):
        self.manifest();raw=b'{ "meta": {"count": 0}, "results": [] }\n'
        with patch('urllib.request.urlopen',return_value=Response(raw)):
            _,record=retrieve.request(self.run,self.m,'/works',{'cursor':'*'},'secret',10,100)
        self.assertEqual((self.run/record['body']).read_bytes(),raw)
        self.assertNotIn('secret',(self.run/'manifest.json').read_text())
    def test_echoed_key_is_not_saved(self):
        self.manifest()
        with patch('urllib.request.urlopen',return_value=Response(b'{"echo":"secret"}')):
            _,record=retrieve.request(self.run,self.m,'/rate-limit',{},'secret',0)
        self.assertEqual(record['body_omitted'],'credential_echo');self.assertNotIn('body',record)
    def test_deduplication_retains_all_provenance_and_doi_aliases(self):
        a={'id':'https://openalex.org/W1','doi':'https://doi.org/10.1/ABC','display_name':'Review','publication_date':'2025-01-01','type':'article','open_access':{}}
        b={**a,'id':'https://openalex.org/W2','doi':'http://doi.org/10.1/abc/'}
        payload={'results':[a,b],'meta':{'count':2,'next_cursor':None}}
        retrieve.save(self.run/'raw/page.json',payload)
        self.m['queries']={qid:{'pages':[{'body':'raw/page.json','cursor':'*'}],'complete':True,'total':2} for qid in ['q1','q2']}
        self.manifest();counts=retrieve.export(self.run)
        self.assertEqual(counts['retrieved_occurrences'],4)
        self.assertEqual(counts['unique_openalex_ids'],2)
        self.assertEqual(counts['unique_after_doi_grouping'],1)
        grouped=retrieve.read(self.run/'works.json')[0]
        self.assertEqual(len(grouped['provenance']),4)
        self.assertEqual(grouped['aliases'],['https://openalex.org/W2'])

if __name__=='__main__':unittest.main()
