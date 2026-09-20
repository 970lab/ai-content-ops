import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_release_evidence.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


class ReleaseEvidenceTest(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_complete_record_is_candidate(self):
        result = VALIDATOR.assess(self.load("templates/release-evidence.yaml"))
        self.assertEqual(result["outcome"], "candidate")

    def test_active_gate_is_blocker(self):
        result = VALIDATOR.assess(self.load("examples/fictional-preview-indexing-blocker.yaml"))
        self.assertEqual(result["outcome"], "blocker")
        self.assertTrue(any(item["field"] == "stop_gates.indexing_policy_conflict" for item in result["blockers"]))

    def test_non_release_input_is_no_candidate(self):
        result = VALIDATOR.assess(self.load("examples/fictional-no-candidate.yaml"))
        self.assertEqual(result["outcome"], "no_candidate")

    def test_missing_rollback_is_blocker(self):
        result = VALIDATOR.assess(self.load("examples/fictional-no-rollback-blocker.yaml"))
        self.assertEqual(result["outcome"], "blocker")
        fields = {item["field"] for item in result["blockers"]}
        self.assertIn("stop_gates.rollback_unavailable", fields)
        self.assertIn("rollback_ref", fields)

    def test_http_style_reference_cannot_replace_missing_layer(self):
        record = self.load("templates/release-evidence.yaml")
        record["layers"]["browser_device"]["state"] = "missing"
        record["layers"]["browser_device"]["evidence_refs"] = []
        result = VALIDATOR.assess(record)
        self.assertEqual(result["outcome"], "blocker")


if __name__ == "__main__":
    unittest.main()
