#!/usr/bin/env python3
"""Archive public evidence URLs without using an OpenAlex key.

Usage: python3 work/scripts/fetch_sources.py
       python3 work/scripts/fetch_sources.py --input work/new_sources.json --source-id paper1
Reads work/sources.json; caches immutable responses and optional PDF text.
PDF extraction requires pypdf; HTML extraction uses the standard library.
"""
import datetime as dt
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.hidden = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.hidden += 1
        if tag in ('p','div','h1','h2','h3','tr','li','br'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.hidden = max(0, self.hidden - 1)
    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)

def main(input_path=None, source_ids=None):
    folder = ROOT / 'work/sources'; folder.mkdir(exist_ok=True)
    for source in json.loads((input_path or ROOT / 'work/sources.json').read_text()):
        if source_ids and source['source_id'] not in source_ids:
            continue
        name = source['source_id']; record = folder / (name + '.json')
        if record.exists():
            previous = json.loads(record.read_text())
            successes = [json.loads(p.read_text()) for p in folder.glob(name + '.attempt*.json')]
            if previous.get('status') == 200 or any(s.get('status') == 200 for s in successes):
                print(name, 'cached'); continue
            record = folder / (name + f'.attempt{len(successes) + 2}.json')
        url = source['url']
        if urllib.parse.urlparse(url).hostname in ('api.openalex.org','content.openalex.org'):
            raise ValueError('Use budgeted retriever for OpenAlex')
        entry = {**source, 'retrieved_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (compatible; CSLRResearch/1.0)'})
            with urllib.request.urlopen(req, timeout=40) as response:
                body = response.read(); entry['status'] = response.status
                entry['final_url'] = response.url; entry['content_type'] = response.headers.get('Content-Type')
            suffix = '.pdf' if body.startswith(b'%PDF') else '.docx' if body.startswith(b'PK') else '.html'
            path = folder / (name + suffix); path.write_bytes(body)
            entry.update(body=path.name, sha256=hashlib.sha256(body).hexdigest())
            if suffix == '.pdf':
                try:
                    from pypdf import PdfReader
                    import pypdf
                    entry['extractor'] = 'pypdf ' + pypdf.__version__
                    reader = PdfReader(path)
                    text = '\n'.join(f'\n--- PDF page {i+1} ---\n' + (p.extract_text() or '') for i,p in enumerate(reader.pages))
                    entry['pages'] = len(reader.pages)
                except ImportError:
                    text = ''; entry['text_status'] = 'pypdf_unavailable'
            elif suffix == '.docx':
                with zipfile.ZipFile(path) as archive:
                    tree = ET.fromstring(archive.read('word/document.xml'))
                    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    text = '\n'.join(''.join(p.itertext()) for p in tree.findall('.//w:p', ns))
                    entry['extractor'] = 'stdlib zipfile/ElementTree'
            else:
                parser = Text(); parser.feed(body.decode('utf-8', errors='replace')); text = ''.join(parser.parts)
            if text:
                (folder / (name + '.txt')).write_text(text)
                entry['text'] = name + '.txt'
            print(name, entry['status'], len(body))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            entry['error_class'] = type(exc).__name__
            entry['status'] = getattr(exc,'code',None)
            print(name, 'failed', entry['status'])
        record.write_text(json.dumps(entry, indent=2) + '\n')
        time.sleep(1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Optional separate source list')
    parser.add_argument('--source-id', action='append', help='Fetch only selected source IDs')
    args = parser.parse_args()
    main(args.input, args.source_id)
