"""Unit tests for Titanic Basic EDA script and notebook."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TITANIC_DIR = ROOT / "school_project" / "week3" / "titanic"


class TitanicEDATests(unittest.TestCase):
    def test_eda_files_exist(self):
        """Verify both python script and jupyter notebook files exist."""
        py_file = TITANIC_DIR / "basic_eda.py"
        ipynb_file = TITANIC_DIR / "basic_eda.ipynb"
        dashboard_png = TITANIC_DIR / "basic_eda_dashboard.png"

        self.assertTrue(py_file.exists(), f"Missing {py_file}")
        self.assertTrue(ipynb_file.exists(), f"Missing {ipynb_file}")
        self.assertTrue(dashboard_png.exists(), f"Missing {dashboard_png}")

    def test_notebook_valid_json_and_structure(self):
        """Verify the Jupyter Notebook is valid v4 JSON and has cells."""
        ipynb_file = TITANIC_DIR / "basic_eda.ipynb"
        data = json.loads(ipynb_file.read_text(encoding="utf-8"))

        self.assertEqual(data.get("nbformat"), 4)
        cells = data.get("cells", [])
        self.assertGreater(len(cells), 10, "Notebook should have more than 10 cells")

        # Check for core sections in markdown
        md_text = " ".join([c["source"] if isinstance(c["source"], str) else "".join(c["source"]) for c in cells if c["cell_type"] == "markdown"])
        self.assertIn("타이타닉", md_text)
        self.assertIn("대푯값", md_text)
        self.assertIn("품질 진단", md_text)
        self.assertIn("상관관계", md_text)

        # Check code cell execution count / outputs exist
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        self.assertGreater(len(code_cells), 5, "Notebook should have code cells")
        has_outputs = any(len(c.get("outputs", [])) > 0 for c in code_cells)
        self.assertTrue(has_outputs, "Notebook code cells should contain executed outputs")


if __name__ == "__main__":
    unittest.main()
