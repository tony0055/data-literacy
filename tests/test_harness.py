import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer, verifier = load("activate"), load("verify")


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "harness", self.root / "harness")

    def test_all_presets_generate_parseable_config_and_skills(self):
        models = json.loads((self.root / "harness/models.json").read_text())
        for preset, expected in models["presets"].items():
            files = installer.planned_files(self.root, preset)
            parsed = tomllib.loads(files[Path(".codex/config.toml")].decode())
            self.assertEqual(parsed["model"], expected["model"])
            self.assertEqual(parsed["model_reasoning_effort"], expected["effort"])
            self.assertEqual(len(files), 3)

    def test_dry_run_and_repeat_install(self):
        with contextlib.redirect_stdout(io.StringIO()):
            installer.activate(self.root, dry_run=True)
            self.assertFalse((self.root / ".codex").exists())
            installer.activate(self.root)
            before = (self.root / ".codex/config.toml").stat().st_mtime_ns
            installer.activate(self.root)
            self.assertEqual(before, (self.root / ".codex/config.toml").stat().st_mtime_ns)

    def test_conflict_stops_before_any_write(self):
        target = self.root / ".agents/skills/harness-next/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("existing user instruction")
        with self.assertRaises(ValueError):
            installer.activate(self.root)
        self.assertFalse((self.root / ".codex").exists())
        self.assertEqual(target.read_text(), "existing user instruction")

    def test_symlink_destination_refused(self):
        (self.root / ".codex").symlink_to(self.root / "elsewhere")
        with self.assertRaises(ValueError):
            installer.activate(self.root)

    def test_non_directory_parent_stops_before_any_write(self):
        (self.root / ".agents").write_text("preserve me")
        with self.assertRaises(ValueError):
            installer.activate(self.root)
        self.assertFalse((self.root / ".codex").exists())

    def check_commands(self, commands, timeout=10):
        (self.root / "harness/checks.json").write_text(json.dumps({
            "commands": commands, "timeout_seconds": timeout
        }))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return verifier.verify(self.root)

    def test_real_process_pass_failure_and_skipped(self):
        self.assertEqual(self.check_commands([[sys.executable, "-c", "pass"]]), 0)
        self.assertEqual(self.check_commands([[sys.executable, "-c", "raise SystemExit(7)"]]), 1)
        self.assertEqual(self.check_commands([]), 2)

    def test_missing_tool_and_timeout_fail(self):
        self.assertEqual(self.check_commands([['/nonexistent-harness-command']]), 1)
        self.assertEqual(self.check_commands([[sys.executable, "-c", "import time; time.sleep(2)"]], .05), 1)

    def test_invalid_command_rejected_before_execution(self):
        with self.assertRaises(ValueError):
            self.check_commands(["echo shell strings are not accepted"])
        with self.assertRaises(ValueError):
            self.check_commands({})


if __name__ == "__main__":
    unittest.main()
