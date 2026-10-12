import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


materials = load("course_materials")
workflow = load("course_workflow")


class CourseSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.snapshot = self.root / materials.SNAPSHOT
        self.file = self.snapshot / "dataliteracy/README.md"
        self.file.parent.mkdir(parents=True)
        data = b"course source\n"
        self.file.write_bytes(data)
        self.manifest = {
            "repository": materials.REPOSITORY,
            "revision": materials.REVISION,
            "files": [{
                "path": "dataliteracy/README.md", "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "git_blob": hashlib.sha1(b"blob 14\0" + data).hexdigest(),
            }],
        }
        self.save_manifest()

    def save_manifest(self):
        (self.snapshot / "manifest.json").write_text(json.dumps(self.manifest))

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return materials.check_snapshot(self.root)

    def test_intact_snapshot_passes(self):
        self.assertEqual(self.check(), 0)

    def test_modified_source_fails(self):
        self.file.write_bytes(b"altered source")
        self.assertEqual(self.check(), 1)

    def test_missing_source_fails(self):
        self.file.unlink()
        self.assertEqual(self.check(), 1)

    def test_unrecorded_file_fails(self):
        (self.snapshot / "unrelated.md").write_text("outside course")
        self.assertEqual(self.check(), 1)

    def test_scope_escape_fails(self):
        self.manifest["files"][0]["path"] = "dataliteracy/../../outside.md"
        self.save_manifest()
        self.assertEqual(self.check(), 1)

    def test_other_courses_are_excluded(self):
        for path in ("slides/w02/index.html", "datascience/PLAN.md",
                     "plans/컴퓨터그래픽스-5-16주-계획.md",
                     "assignments/w02/과제2-meta-개발자계정.md"):
            with self.subTest(path=path):
                self.assertFalse(materials.selected(path))


class CourseContractTests(unittest.TestCase):
    def test_analysis_keeps_slides_and_deploy_out_of_scope(self):
        result = workflow.contract("analysis", "gpt-6.1-sol-fast")
        self.assertNotIn("presentation/index.html", result["artifacts"])
        self.assertFalse(result["deploy"])
        self.assertIn("independent_check", result["steps"])

    def test_slides_requires_design_and_browser_check(self):
        result = workflow.contract("slides", "chatgpt-subscription/gpt-6-astra")
        self.assertIn("presentation/index.html", result["artifacts"])
        self.assertIn("design_standard", result["steps"])
        self.assertIn("docs/data-to-slides-workflow.md", result["reads"])
        self.assertIn("browser_check", result["steps"])

    def test_visualization_preserves_chart_data(self):
        result = workflow.contract("visualization", "gpt-6.1-sol-fast")
        self.assertIn("chart-data.csv", result["artifacts"])
        self.assertNotIn("presentation/index.html", result["artifacts"])

    def test_practice_does_not_force_analysis_code_on_written_assignments(self):
        result = workflow.contract("practice", "gpt-6.1-sol-fast")
        self.assertNotIn("analysis.py", result["artifacts"])
        self.assertIn("task_execution", result["steps"])
        self.assertIn("ai-use.csv", result["artifacts"])

    def test_selected_model_is_not_restricted_to_one_family(self):
        for model in ("anthropic/claude-sonnet-4", "gpt-5.6-sol",
                      "custom-provider/custom-model"):
            with self.subTest(model=model):
                result = workflow.contract("analysis", model)
                self.assertEqual(result["model"], model)

    def test_selected_model_is_preserved_in_worker_routes(self):
        result = workflow.contract("analysis", "openai/gpt-6.1-sol")
        self.assertEqual(result["model"], "openai/gpt-6.1-sol")
        self.assertEqual(result["worker_model"], "openai/gpt-6.1-sol")
        self.assertEqual(result["decision_model"], "openai/gpt-6.1-sol")

    def test_unqualified_model_does_not_gain_a_default_provider(self):
        result = workflow.contract("analysis", "gpt-6.1-sol-fast")
        self.assertEqual(result["model"], "gpt-6.1-sol-fast")
        self.assertEqual(result["worker_model"], "gpt-6.1-sol-fast")
        self.assertEqual(result["decision_model"], "gpt-6.1-sol-fast")

    def test_empty_model_fails(self):
        for model in ("", " "):
            with self.subTest(model=model):
                with self.assertRaises(ValueError):
                    workflow.contract("analysis", model)

    def test_cli_emits_consumable_contract(self):
        result = subprocess.run(
            [sys.executable, "scripts/course_workflow.py", "team", "gpt-6-astra"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads(result.stdout)
        self.assertEqual(contract["mode"], "team")
        self.assertIn("sensitivity_check", contract["steps"])
        self.assertIn("plan.md", contract["artifacts"])

    def test_cli_rejects_unknown_mode(self):
        result = subprocess.run(
            [sys.executable, "scripts/course_workflow.py", "unrecognized", "gpt-6-astra"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
