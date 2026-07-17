#!/usr/bin/env python3
"""Tests for the Fullsend repository orientation helper."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("orient.py")
SPEC = importlib.util.spec_from_file_location("fullsend_orient", MODULE_PATH)
assert SPEC and SPEC.loader
ORIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORIENT)


class OrientTests(unittest.TestCase):
    def test_discovers_per_repo_installation_and_repo_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".github" / "workflows" / "fullsend.yaml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                """name: fullsend
jobs:
  dispatch:
    uses: example/.fullsend/.github/workflows/dispatch.yml@abc123
    with:
      install_mode: per-repo
# /fs-code
""",
                encoding="utf-8",
            )
            harness = root / ".fullsend" / "harness" / "code.yaml"
            harness.parent.mkdir(parents=True)
            harness.write_text(
                """role: coder
slug: example-code
agent: agents/code.md
model: opus
policy: policies/base.yaml
skills:
  - skills/code-implementation
plugins:
  - plugins/example
""",
                encoding="utf-8",
            )
            skill = root / ".agents" / "skills" / "repo-checks" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                """---
name: repo-checks
description: Check repository-specific invariants.
---
""",
                encoding="utf-8",
            )

            result = ORIENT.inspect(root)

            self.assertTrue(result["found"])
            self.assertEqual(result["installation"]["mode"], "per-repo")
            self.assertEqual(result["harnesses"][0]["role"], "coder")
            self.assertEqual(
                result["harnesses"][0]["skills"], ["skills/code-implementation"]
            )
            self.assertEqual(result["harnesses"][0]["model"], "opus")
            self.assertEqual(result["harnesses"][0]["policy"], "policies/base.yaml")
            self.assertEqual(result["harnesses"][0]["plugins"], ["plugins/example"])
            self.assertEqual(result["skills"][0]["name"], "repo-checks")
            self.assertEqual(
                result["remote_sources"],
                ["example/.fullsend/.github/workflows/dispatch.yml@abc123"],
            )

    def test_repo_skill_alone_is_not_an_installation_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / ".agents" / "skills" / "repo-checks" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: repo-checks\ndescription: Checks.\n---\n")

            result = ORIENT.inspect(root)

            self.assertFalse(result["found"])
            self.assertEqual(result["installation"]["mode"], "unknown")


if __name__ == "__main__":
    unittest.main()
