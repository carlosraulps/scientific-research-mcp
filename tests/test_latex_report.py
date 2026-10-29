#!/usr/bin/env python3
"""
Unit tests for LaTeX Report Template (Tau-class v2.6.0) Scaffolding,
Compilation Pipeline, and MCP Integration.
"""

import os
import sys
import shutil
import tempfile
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from latex_bridge import LaTeXBridge
from mcp_server import handle_tool_call


class TestLaTeXReport(unittest.TestCase):
    def setUp(self):
        self.bridge = LaTeXBridge(BASE_DIR)
        self.test_dir = tempfile.mkdtemp(prefix="test_latex_report_")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_template_list(self):
        res = self.bridge.list_templates()
        self.assertIn("templates", res)
        self.assertIn("latex-report", res["templates"])
        self.assertIn("beamer-nord", res["templates"])
        self.assertEqual(res["templates"]["latex-report"]["type"], "report")
        self.assertEqual(res["templates"]["latex-report"]["compiler"], "pdflatex")

    def test_02_report_scaffolding(self):
        dest = Path(self.test_dir) / "my_experimental_report"
        res = self.bridge.scaffold_report(
            destination=str(dest),
            template="latex-report",
            title="Carrier Mobility in Twisted Bilayer Graphene",
            author="Prof. Richard Feynman",
            institute="California Institute of Technology (Caltech)",
            doctype="Experimental Lab Report",
            compile_pdf=False
        )
        self.assertTrue(res["success"])
        self.assertTrue((dest / "template.tex").exists())
        self.assertTrue((dest / "tau.bib").exists())
        self.assertTrue((dest / "tau-class" / "tau.cls").exists())
        self.assertTrue((dest / "figures" / "Example.pdf").exists())

        content = (dest / "template.tex").read_text(encoding="utf-8")
        self.assertIn("Carrier Mobility in Twisted Bilayer Graphene", content)
        self.assertIn("Prof. Richard Feynman", content)
        self.assertIn("California Institute of Technology (Caltech)", content)
        self.assertIn("Experimental Lab Report", content)

    def test_03_report_compilation(self):
        dest = Path(self.test_dir) / "compiled_report"
        scaffold_res = self.bridge.scaffold_report(
            destination=str(dest),
            template="latex-report",
            compile_pdf=False
        )
        self.assertTrue(scaffold_res["success"])

        tex_file = dest / "template.tex"
        comp_res = self.bridge.compile_document(
            tex_path=str(tex_file),
            compiler="pdflatex",
            passes=3,
            clean_aux=True,
            preview=True
        )
        self.assertTrue(comp_res["success"], f"Compilation failed: {comp_res.get('error')}")
        self.assertTrue(Path(comp_res["pdf_path"]).exists())
        self.assertGreater(comp_res["size_kb"], 100)

    def test_04_mcp_tool_calls(self):
        # 1. MCP list templates
        mcp_list = handle_tool_call("latex_template_list", {})
        self.assertIn("latex-report", mcp_list.get("templates", {}))

        # 2. MCP scaffold
        mcp_dest = Path(self.test_dir) / "mcp_report"
        mcp_scaffold = handle_tool_call("latex_report_scaffold", {
            "destination": str(mcp_dest),
            "template": "latex-report",
            "title": "Ab Initio Modeling of Perovskite Oxides",
            "author": "Dr. Chien-Shiung Wu",
            "compile_pdf": False
        })
        self.assertTrue(mcp_scaffold.get("success"))
        self.assertTrue((mcp_dest / "template.tex").exists())


if __name__ == "__main__":
    unittest.main()
