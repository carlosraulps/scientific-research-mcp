import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from ponytail_delta import PonytailDeltaComposer


class TestPonytailDeltaComposer(unittest.TestCase):
    def setUp(self):
        self.composer_vasp = PonytailDeltaComposer(engine="vasp")
        self.composer_siesta = PonytailDeltaComposer(engine="siesta")

    def test_01_parse_vasp_incar(self):
        raw_incar = """
        PREC = Accurate # [DREAMS:test] High precision
        ENCUT = 520
        ISMEAR = 0 ; SIGMA = 0.05 # [NotebookLM:dft-doc] Gaussian smearing
        ALGO = Normal # Redundant default
        """
        tags = self.composer_vasp.parse_vasp_incar(raw_incar)
        self.assertEqual(tags["PREC"]["value"], "Accurate")
        self.assertEqual(tags["PREC"]["source"], "DREAMS:test")
        self.assertEqual(tags["ENCUT"]["value"], "520")
        self.assertEqual(tags["ISMEAR"]["value"], "0")
        self.assertEqual(tags["SIGMA"]["value"], "0.05")
        self.assertEqual(tags["SIGMA"]["source"], "NotebookLM:dft-doc")
        self.assertEqual(tags["ALGO"]["value"], "Normal")

    def test_02_prune_vasp_redundancy(self):
        tags = {
            "PREC": {"value": "Accurate", "comment": "", "source": ""},
            "ALGO": {"value": "Normal", "comment": "", "source": ""},
            "SYSTEM": {"value": "Pt_Cluster", "comment": "", "source": ""},
            "IBRION": {"value": "2", "comment": "", "source": ""},
            "ISIF": {"value": "2", "comment": "", "source": ""},
            "LWAVE": {"value": ".TRUE.", "comment": "", "source": ""},
        }
        pruned = self.composer_vasp.prune_vasp_redundancy(tags)
        self.assertIn("PREC", pruned)
        self.assertNotIn("ALGO", pruned)
        self.assertNotIn("SYSTEM", pruned)
        self.assertNotIn("ISIF", pruned)  # ISIF=2 redundant when IBRION=2
        self.assertNotIn("LWAVE", pruned) # LWAVE=.TRUE. is default

    def test_03_apply_delta_with_grounding(self):
        base_incar = """
        PREC = Accurate
        ENCUT = 520
        IBRION = 2
        NSW = 200
        ISIF = 3
        ISMEAR = 0
        SIGMA = 0.05
        """
        delta = {
            "NSW": {"value": 0, "rationale": "Single point SCF", "source": "Workflow:Step-02"},
            "IBRION": -1,
            "ISMEAR": {"value": -5, "rationale": "Tetrahedron method for DOS", "source": "NotebookLM:dft-doc:DOS"},
            "NEDOS": 2001,
            "LORBIT": 11,
            "ISIF": None, # Explicit delete
        }
        composed = self.composer_vasp.apply_delta(base_incar, delta, prune_redundant=True)
        self.assertEqual(composed["NSW"]["value"], "0")
        self.assertEqual(composed["NSW"]["source"], "Workflow:Step-02")
        self.assertEqual(composed["ISMEAR"]["value"], "-5")
        self.assertEqual(composed["ISMEAR"]["source"], "NotebookLM:dft-doc:DOS")
        self.assertEqual(composed["NEDOS"]["value"], "2001")
        self.assertNotIn("ISIF", composed)
        # Verify base parameters preserved without drift
        self.assertEqual(composed["PREC"]["value"], "Accurate")
        self.assertEqual(composed["ENCUT"]["value"], "520")

    def test_04_siesta_fdf_composition(self):
        base_fdf = """
        XC.functional GGA
        XC.authors PBE
        MeshCutoff 350.0 Ry
        MD.TypeOfRun CG
        MD.NumCGsteps 100
        """
        delta = {
            "MD.TypeOfRun": "none",
            "MD.NumCGsteps": "0",
            "DM.MixingWeight": {"value": "0.04", "rationale": "Prevent charge sloshing", "source": "NotebookLM:dft-doc:Polymer"},
            "DM.NumberPulay": "5",
        }
        composed = self.composer_siesta.apply_delta(base_fdf, delta)
        self.assertEqual(composed["MD.TypeOfRun"]["value"], "none")
        self.assertEqual(composed["MD.NumCGsteps"]["value"], "0")
        self.assertEqual(composed["DM.MixingWeight"]["value"], "0.04")
        self.assertEqual(composed["DM.MixingWeight"]["source"], "NotebookLM:dft-doc:Polymer")
        self.assertEqual(composed["MeshCutoff"]["value"], "350.0 Ry")

    def test_05_end_to_end_file_composition(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base_p = Path(tmpdir) / "INCAR.base"
            out_p = Path(tmpdir) / "01_dos" / "INCAR"

            base_p.write_text("""
            PREC = Accurate # [NotebookLM:dft-doc:PREC] Standard precision
            ENCUT = 520
            ISMEAR = 0
            SIGMA = 0.05
            IBRION = 2
            NSW = 100
            """)

            delta = {
                "NSW": {"value": 0, "rationale": "Static DOS calculation", "source": "Step2"},
                "ISMEAR": -5,
                "NEDOS": 2001,
                "LORBIT": 11,
            }

            written = self.composer_vasp.compose_to_file(base_p, delta, out_p)
            self.assertTrue(written.exists())

            content = written.read_text()
            self.assertIn("PREC         = Accurate  # [NotebookLM:dft-doc:PREC] Standard precision", content)
            self.assertIn("ISMEAR       = -5", content)
            self.assertIn("NSW          = 0", content)
            self.assertIn("[Step2] Static DOS calculation", content)
            self.assertIn("NEDOS        = 2001", content)
            self.assertIn("LORBIT       = 11", content)


if __name__ == "__main__":
    unittest.main()
