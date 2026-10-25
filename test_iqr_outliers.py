import os, tempfile, unittest
from iqr_outliers import scan

class T(unittest.TestCase):
    def setUp(self):
        self.p = os.path.join(tempfile.mkdtemp(), "a.csv")
        with open(self.p, "w", encoding="utf-8") as f:
            f.write("amt,qty\n10,1\n11,2\n12,x\n10,\n11,3\n500,4\n")
    def test_flags_outlier_with_line(self):
        r = scan(self.p, ["amt"])
        self.assertEqual(r["amt"]["outliers"], [{"line": 7, "value": 500.0}])
    def test_skips_sparse(self):
        r = scan(self.p, ["qty"])
        self.assertEqual(r["qty"]["outliers"], [])
    def test_too_few(self):
        p = os.path.join(tempfile.mkdtemp(), "b.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("amt\n1\n2\n")
        self.assertIn("skipped", scan(p, ["amt"])["amt"])

if __name__ == "__main__":
    unittest.main()
