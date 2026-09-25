import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from src.distill import distill, parts, redact, split_parts

ROOT = Path(__file__).resolve().parents[1]

class DistillationTests(unittest.TestCase):
    def test_tool_and_reasoning_payloads_are_excluded(self):
        record={'message':{'role':'assistant','content':[{'type':'text','text':'visible'},{'type':'tool_use','input':{'sensitive':'omit'}},{'type':'thinking','thinking':'omit'}]}}
        self.assertEqual(list(parts(record)),['[assistant] visible'])

    def test_meta_and_nonconversation_messages_are_excluded(self):
        self.assertEqual(list(parts({'isMeta':True,'message':{'role':'user','content':'omit'}})),[])
        self.assertEqual(list(parts({'message':{'role':'tool','content':'omit'}})),[])

    def test_named_and_quoted_credentials_are_masked(self):
        for text in ['PASSWORD=demo-value', 'API_TOKEN: "demo value with spaces"', "SECRET='demo value'"]:
            result=redact(text)
            self.assertNotIn('demo',result)
            self.assertIn('<redacted>',result)

    def test_selected_token_patterns_and_bearer_are_masked(self):
        fake='ghp_'+'x'*24
        self.assertEqual(redact(fake),'<redacted>')
        self.assertEqual(redact('Bearer demonstration-only'),'Bearer <redacted>')

    def test_plain_text_is_preserved(self):
        self.assertEqual(redact('Use separate sessions for admin and reviewer.'),'Use separate sessions for admin and reviewer.')

    def test_invalid_dates_and_malformed_records_are_counted(self):
        lines=['not json','[]','{"timestamp":"2026-02-30"}','{"timestamp":"../../outside"}']
        self.assertEqual(distill(lines),({},4))

    def test_groups_dates_in_stable_order(self):
        import json
        records=[{'timestamp':d,'message':{'role':'user','content':d}} for d in ['2026-01-02','2026-01-01']]
        days,rejected=distill(map(json.dumps,records))
        self.assertEqual(list(days),['2026-01-01','2026-01-02'])
        self.assertEqual(rejected,0)

    def test_large_single_line_respects_chunk_limit(self):
        chunks=list(split_parts('x'*31,10))
        self.assertEqual(''.join(chunks),'x'*31)
        self.assertTrue(all(len(c)<=10 for c in chunks))
        self.assertEqual(list(split_parts('abc\ndef\nghi',7)),['abc\ndef','ghi'])
        with self.assertRaises(ValueError):list(split_parts('a',0))

    def test_cli_writes_only_explicit_output_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'distilled'
            args=[sys.executable,str(ROOT/'src/distill.py'),'--input',str(ROOT/'fixtures/session.jsonl'),'--output',str(output)]
            first=subprocess.run(args,capture_output=True,text=True)
            self.assertEqual(first.returncode,0,first.stderr)
            files=list(output.glob('*.txt'));self.assertEqual(len(files),1)
            content=files[0].read_text()
            self.assertIn('<redacted>',content)
            self.assertNotIn('not-a-real-credential',content)
            second=subprocess.run(args,capture_output=True,text=True)
            self.assertNotEqual(second.returncode,0)
            self.assertEqual(files[0].read_text(),content)

    def test_no_visible_content_is_a_failed_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'empty.jsonl';source.write_text('')
            output=Path(tmp)/'out'
            result=subprocess.run([sys.executable,str(ROOT/'src/distill.py'),'--input',str(source),'--output',str(output)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(output.exists())

if __name__ == '__main__':unittest.main()
