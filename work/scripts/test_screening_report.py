#!/usr/bin/env python3
"""Test screening validation and stage-specific rendering without network access.

Usage: python3 work/scripts/test_screening_report.py
"""
import copy
import unittest
from screening_report import validate_record, verdict_label, markdown_report


class ScreeningTests(unittest.TestCase):
    def record(self):
        return dict(openalex_id='W-test', ai_decision='include', human_decision='not_screened',
                    stage='title_abstract', evidence_level='abstract_only',
                    description='A survey of visual sign recognition.', reason='Broader review warrants full-text assessment.',
                    criteria={k:dict(status='uncertain',reason='Needs assessment') for k in ('M1','M2','M3')},
                    failed_criteria=[], source_ids=['test-source'],
                    evidence=[dict(source_id='test-source',url='https://example.org/paper',path='protocol.md',
                                   locator='Abstract',passage='Synthetic test fixture')],
                    unresolved_issues=[], next_action='', classification=None, qualifying_studies=[], assessments=[])

    def test_advancement_does_not_require_full_text(self):
        r=self.record(); validate_record(r)
        self.assertEqual(verdict_label(r),'Proposed advance to full text')

    def test_full_text_requires_threshold_and_history(self):
        r=self.record(); r.update(stage='full_text',evidence_level='full_text')
        with self.assertRaises(AssertionError):validate_record(r)
        r.update(assessments=[dict(stage='title_abstract',ai_decision='include')],classification='broader',
                 qualifying_studies=['Study A','Study B'])
        for c in r['criteria'].values():c['status']='pass'
        validate_record(r)
        self.assertEqual(verdict_label(r),'Proposed eligible review')

    def test_exclusion_requires_linked_failure_and_evidence(self):
        r=self.record(); r['ai_decision']='exclude'
        with self.assertRaises(AssertionError):validate_record(r)
        r['failed_criteria']=['M1']; r['criteria']['M1']['status']='fail'; validate_record(r)
        self.assertIn('../../index.html#M1',markdown_report(r,dict(display_name='Test paper')))
        r['evidence']=[]
        with self.assertRaises(AssertionError):validate_record(r)

    def test_uncertainty_requires_next_action(self):
        r=self.record(); r['ai_decision']='uncertain'
        with self.assertRaises(AssertionError):validate_record(r)
        r.update(unresolved_issues=['Full text unavailable'],next_action='Obtain full text.')
        validate_record(r)
        self.assertIn('Next: Obtain full text.',markdown_report(r,dict(display_name='Test paper')))

    def test_unknown_source_and_missing_path_rejected(self):
        r=self.record(); r['evidence'][0]['source_id']='unknown'
        with self.assertRaises(AssertionError):validate_record(r)
        r=self.record(); r['evidence'][0]['path']='missing-file'
        with self.assertRaises(AssertionError):validate_record(r)


if __name__=='__main__':unittest.main()
