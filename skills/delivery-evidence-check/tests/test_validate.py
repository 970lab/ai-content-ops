import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NOW = datetime(2026, 1, 1, 13, tzinfo=timezone.utc)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((ROOT / 'examples/fictional-local.json').read_text())

    def result(self):
        return module.validate(self.packet, NOW)['outcome']

    def test_fictional_local(self):
        self.assertEqual(self.result(), 'candidate')

    def test_public_requires_public_surface(self):
        self.packet['audience'] = 'public'
        self.assertEqual(self.result(), 'blocker')
        self.packet['evidence']['access']['surface'] = 'public'
        self.assertEqual(self.result(), 'candidate')

    def test_missing_each_layer(self):
        for layer in module.LAYERS:
            packet = copy.deepcopy(self.packet)
            del packet['evidence'][layer]
            self.assertEqual(module.validate(packet, NOW)['outcome'], 'blocker')

    def test_stale(self):
        self.packet['evidence']['checks']['observed_at'] = '2025-12-01T12:00:00Z'
        self.assertEqual(self.result(), 'blocker')

    def test_future(self):
        self.packet['evidence']['checks']['observed_at'] = '2027-01-01T12:00:00Z'
        self.assertEqual(self.result(), 'blocker')

    def test_mismatched_revision(self):
        self.packet['evidence']['delivery']['revision'] = 'revision-1'
        self.assertEqual(self.result(), 'blocker')

    def test_mismatched_project(self):
        self.packet['evidence']['source']['project'] = 'another-report'
        self.assertEqual(self.result(), 'blocker')

    def test_missing_negative_path(self):
        del self.packet['evidence']['experience']['negative_ref']
        self.assertEqual(self.result(), 'blocker')

    def test_failed_check(self):
        self.packet['evidence']['experience']['result'] = 'failed'
        self.assertEqual(self.result(), 'blocker')

    def test_no_claim(self):
        self.packet = {'schema_version': 1, 'claim': 'none', 'reason': 'No deliverable requested', 'evidence': {}}
        self.assertEqual(self.result(), 'no_candidate')

    def test_invalid_shapes(self):
        for value in (None, [], {}, {'schema_version': 1, 'claim': 'delivery', 'evidence': []}):
            self.assertEqual(module.validate(value, NOW)['outcome'], 'blocker')

    def test_template_blocks(self):
        self.packet = json.loads((ROOT / 'templates/packet.json').read_text())
        self.assertEqual(self.result(), 'blocker')

    def test_bad_window(self):
        for value in (-1, 0, float('nan'), float('inf')):
            self.assertEqual(module.validate(self.packet, NOW, value)['outcome'], 'blocker')

    def test_scoped_negative_path(self):
        row = self.packet['evidence']['experience']
        row['negative_path'] = 'not-applicable'
        row['negative_reason'] = 'Static report with no interactive input'
        self.assertEqual(self.result(), 'candidate')
        row['negative_reason'] = ''
        self.assertEqual(self.result(), 'blocker')

    def test_remaining_issues(self):
        row = self.packet['evidence']['record']
        del row['remaining_issues']
        self.assertEqual(self.result(), 'blocker')
        row['remaining_issues'] = ['Recipient review unresolved']
        self.assertEqual(self.result(), 'blocker')

    def test_cli_missing_file(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py'), str(ROOT / 'absent.json')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['outcome'], 'blocker')


if __name__ == '__main__':
    unittest.main()
