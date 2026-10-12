"""Unit tests for Pima Indians Diabetes comprehensive report notebook."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PIMA_DIR = ROOT / "school" / "school_project" / "week3" / "pima_indians"
if not PIMA_DIR.exists():
    PIMA_DIR = ROOT / "school_project" / "week3" / "pima_indians"


class PimaIndiansReportTests(unittest.TestCase):
    def test_report_notebook_exists(self):
        """Verify report notebook files exist."""
        report_ipynb = PIMA_DIR / "pima_indians_report.ipynb"
        comp_ipynb = PIMA_DIR / "comprehensive_report.ipynb"

        self.assertTrue(report_ipynb.exists(), f"Missing {report_ipynb}")
        self.assertTrue(comp_ipynb.exists(), f"Missing {comp_ipynb}")

    def test_notebook_valid_json_and_structure(self):
        """Verify the Jupyter Notebook is valid v4 JSON and has cells."""
        report_ipynb = PIMA_DIR / "pima_indians_report.ipynb"
        data = json.loads(report_ipynb.read_text(encoding="utf-8"))

        self.assertEqual(data.get("nbformat"), 4)
        cells = data.get("cells", [])
        self.assertGreater(len(cells), 15, "Notebook should have more than 15 cells")

        # Check for core sections in markdown
        md_text = " ".join([c["source"] if isinstance(c["source"], str) else "".join(c["source"]) for c in cells if c["cell_type"] == "markdown"])
        self.assertIn("피마 인디언", md_text)
        self.assertIn("0값 은폐 결측치", md_text)
        self.assertIn("상관관계 왜곡", md_text)
        self.assertIn("인과", md_text)
        self.assertIn("머신러닝", md_text)

        # Check code cell execution and outputs
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        self.assertGreater(len(code_cells), 5, "Notebook should have code cells")

        # Check that outputs are present and not empty (executed notebook)
        for idx, cell in enumerate(code_cells):
            self.assertIsNotNone(cell.get("execution_count"), f"Code cell {idx} should be executed")
            self.assertTrue(len(cell.get("outputs", [])) > 0, f"Code cell {idx} should have outputs")

        # Verify image outputs exist in the notebook
        has_image = False
        for cell in code_cells:
            for out in cell.get("outputs", []):
                if out.get("output_type") == "display_data" and "image/png" in out.get("data", {}):
                    has_image = True
                    break
        self.assertTrue(has_image, "Notebook should contain rendered plot images")


if __name__ == "__main__":
    unittest.main()
