#!/usr/bin/env python3
"""
Unit tests for VMD-Automation skill and Tachyon raytracing pipeline.
"""

import os
import sys
import unittest
import tempfile
import subprocess
from pathlib import Path

# Add scripts directory to path
SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import vmd_render


class TestVMDAutomation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.poscar_path = "/home/cr/computational-materials-suite/vasp.6.6.1/src/vaspml/test/data/structure/POSCAR.MAPbI3.cubic"
        cls.vmd_bin = "/home/cr/computational-materials-suite/bin/vmd"
        cls.tachyon_bin = "/home/cr/computational-materials-suite/vmd/tachyon_LINUXAMD64"

    def test_binaries_exist(self):
        self.assertTrue(os.path.exists(self.vmd_bin), f"VMD binary not found: {self.vmd_bin}")
        self.assertTrue(os.path.exists(self.tachyon_bin), f"Tachyon binary not found: {self.tachyon_bin}")

    def test_file_type_detection(self):
        self.assertEqual(vmd_render.detect_file_type("POSCAR"), "POSCAR")
        self.assertEqual(vmd_render.detect_file_type("CONTCAR_opt"), "POSCAR")
        self.assertEqual(vmd_render.detect_file_type("XDATCAR"), "XDATCAR")
        self.assertEqual(vmd_render.detect_file_type("dump.lammpstrj"), "lammpstrj")
        self.assertEqual(vmd_render.detect_file_type("protein.pdb"), "pdb")
        self.assertEqual(vmd_render.detect_file_type("structure.cif"), "pdbx")
        self.assertEqual(vmd_render.detect_file_type("density.cube"), "cube")
        self.assertEqual(vmd_render.detect_file_type("potential.dx"), "dx")

    def test_single_view_render(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_png = os.path.join(tmpdir, "render_test.png")
            args = vmd_render.argparse.Namespace(
                input_file=self.poscar_path,
                output=out_png,
                view="iso",
                preset="perovskite",
                rep="CPK",
                sphere_scale=0.5,
                bond_radius=0.15,
                sphere_res=24,
                bond_res=24,
                material="AOShiny",
                color_by="Element",
                pbc_box=True,
                pbc_box_width=2.0,
                pbc_box_color="black",
                periodic_images="",
                width=640,
                height=480,
                ao=0.7,
                samples=4,
                bg="white",
                autotrim=True,
                trim_padding=20,
                vmd_bin=self.vmd_bin,
                tachyon_bin=self.tachyon_bin
            )
            success = vmd_render.render_single_view(
                self.poscar_path, "POSCAR", "iso", out_png, args
            )
            self.assertTrue(success, "render_single_view failed")
            self.assertTrue(os.path.exists(out_png), "Output PNG was not generated")
            self.assertGreater(os.path.getsize(out_png), 1000, "Rendered file is suspiciously small")

    def test_batch_all_views(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                str(SCRIPTS_DIR / "vmd_render.py"),
                self.poscar_path,
                "-o", tmpdir,
                "-v", "all",
                "--width", "400",
                "--height", "300",
                "--samples", "2",
                "--pbc-box"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"vmd_render.py -v all failed: {res.stderr}")

            views = ["a", "b", "c", "iso"]
            for v in views:
                expected_file = os.path.join(tmpdir, f"POSCAR.MAPbI3_{v}.png")
                self.assertTrue(os.path.exists(expected_file), f"Missing view: {expected_file}")
                self.assertGreater(os.path.getsize(expected_file), 1000)


if __name__ == "__main__":
    unittest.main()
