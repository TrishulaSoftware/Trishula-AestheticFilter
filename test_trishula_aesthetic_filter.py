#!/usr/bin/env python3
"""
test_trishula_aesthetic_filter.py
Unit tests for Trishula-AestheticFilter calibrator.
"""

import unittest
import tempfile
from pathlib import Path
from trishula_aesthetic_filter import scan_file, fix_content

class TestAestheticFilter(unittest.TestCase):

    def setUp(self):
        # Create temp files for auditing and fixing
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_linguistic_checks(self):
        # Create a mock prose file containing several stop-slop tell patterns
        p = self.dir_path / "mock_prose.md"
        content = (
            "Here's the thing: we really need to double down on our strategy.\n"
            "This is genuinely a game-changer -- let that sink in.\n"
            "What makes this hard is that it is not because of X, but because of Y.\n"
            "Look, the decision was reached to circle back tomorrow."
        )
        p.write_text(content, encoding="utf-8")

        res = scan_file(p)
        self.assertEqual(res["type"], "prose")
        
        # Verify specific rules triggered
        rules_triggered = {v.rule for v in res["violations"]}
        self.assertIn("throat-clearing", rules_triggered)
        self.assertIn("adverb", rules_triggered)
        self.assertIn("jargon", rules_triggered)
        self.assertIn("crutch", rules_triggered)
        self.assertIn("structure-binary_contrast_1", rules_triggered)
        self.assertIn("sentence-starter", rules_triggered)
        self.assertIn("rhythm", rules_triggered) # em-dash
        self.assertIn("passive-voice", rules_triggered) # "decision was reached"

        self.assertLess(res["linguistic_score"], 40)

    def test_visual_checks(self):
        # Create a mock code/style file containing taste-skill design tells
        p = self.dir_path / "MockComponent.tsx"
        content = (
            "import { useState } from 'react';\n"
            "import { Button } from '@radix-ui/themes';\n"
            "// Let's use Inter font and purple/indigo gradient backdrop\n"
            "export function Hero() {\n"
            "  return (\n"
            "    <div className='hero bg-gradient-to-r from-purple-500 to-indigo-500 text-center font-sans inter'>\n"
            "      <h1 className='text-[11px] uppercase tracking-[0.2em] font-mono'>Welcome</h1>\n"
            "      <h1 className='text-[11px] uppercase tracking-[0.2em] font-mono'>Features</h1>\n"
            "      <h1 className='text-[11px] uppercase tracking-[0.2em] font-mono'>Pricing</h1>\n"
            "      <h1 className='text-[11px] uppercase tracking-[0.2em] font-mono'>Docs</h1>\n"
            "      <h1 className='text-[11px] uppercase tracking-[0.2em] font-mono'>Blog</h1>\n"
            "      <button label='Contact Us' />\n"
            "      <button label='Get in Touch' />\n"
            "    </div>\n"
            "  );\n"
            "}\n"
        )
        p.write_text(content, encoding="utf-8")

        res = scan_file(p)
        self.assertEqual(res["type"], "code")

        rules_triggered = {v.rule for v in res["violations"]}
        self.assertIn("visual-lila", rules_triggered)
        self.assertIn("visual-font", rules_triggered)
        self.assertIn("visual-layout", rules_triggered)
        self.assertIn("visual-layout-eyebrows", rules_triggered)
        self.assertIn("visual-duplicate-cta", rules_triggered)

        self.assertLess(res["visual_score"], 40)

    def test_fixer_function(self):
        # Verify that safe replacements are made correctly
        p = self.dir_path / "mock_fix.md"
        content = (
            "Here's the thing: I honestly think em-dashes -- are annoying.\n"
            "Look, we just need to simply write better."
        )
        p.write_text(content, encoding="utf-8")

        fixes_applied = fix_content(p)
        self.assertGreater(fixes_applied, 0)

        # Read back and check replacements
        fixed_text = p.read_text(encoding="utf-8")
        self.assertNotIn("Here's the thing:", fixed_text)
        self.assertNotIn("Look,", fixed_text)
        self.assertNotIn("--", fixed_text)
        self.assertNotIn("honestly", fixed_text)
        self.assertNotIn("simply", fixed_text)
        self.assertIn(", ", fixed_text)

if __name__ == "__main__":
    unittest.main()
