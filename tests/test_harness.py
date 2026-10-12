import contextlib
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    # scripts/checks has no .py suffix, so name the loader explicitly
    loader = importlib.machinery.SourceFileLoader(name, str(ROOT / "scripts" / name))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


verifier = load("checks")


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "harness", self.root / "harness")

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


class LocalSkillTests(unittest.TestCase):
    names = ("course-workflow",)

    def test_project_skill_metadata(self):
        for name in self.names:
            with self.subTest(skill=name):
                skill = ROOT / ".agents/skills" / name / "SKILL.md"
                frontmatter = skill.read_text().split("---", 2)[1]
                fields = dict(line.split(": ", 1) for line in frontmatter.splitlines() if ": " in line)
                self.assertEqual(fields["name"], name)
                self.assertIn("description", fields)

    def test_claude_discovers_same_local_skill(self):
        for name in self.names:
            with self.subTest(skill=name):
                canonical = ROOT / ".agents/skills" / name
                claude = ROOT / ".claude/skills" / name
                self.assertTrue((canonical / "SKILL.md").is_file())
                self.assertTrue(claude.is_symlink())
                self.assertEqual(claude.resolve(), canonical.resolve())

    def test_agents_md_is_the_only_entry(self):
        # A CLAUDE.md would make Claude Code read it instead of AGENTS.md
        for name in ("CLAUDE.md", "CLAUDE.local.md"):
            with self.subTest(file=name):
                self.assertFalse((ROOT / name).exists())


class HarnessLinkTests(unittest.TestCase):
    """Always-loaded and routed harness docs must not point at missing files."""

    def harness_docs(self):
        yield from (ROOT / "AGENTS.md", ROOT / "README.md")
        yield from (ROOT / "docs").glob("*.md")
        yield from (ROOT / "harness").glob("*.md")
        yield from (ROOT / "school/school_project/course-domain").glob("*.md")
        yield from (ROOT / ".agents/skills").glob("*/SKILL.md")

    def test_relative_markdown_links_resolve(self):
        import re
        for doc in self.harness_docs():
            for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", doc.read_text()):
                if "://" in target or target.startswith("mailto:"):
                    continue
                with self.subTest(doc=doc.relative_to(ROOT).as_posix(), target=target):
                    self.assertTrue((doc.parent / target).exists())


if __name__ == "__main__":
    unittest.main()
