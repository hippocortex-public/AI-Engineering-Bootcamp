import copy
import json
import tempfile
import unittest
from pathlib import Path
from evaluation_lab.core import read_rows,evaluate,compare,score
ASSETS=Path(__file__).resolve().parents[3]/"assets"
class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.data=read_rows(ASSETS/"dataset.jsonl");self.base=read_rows(ASSETS/"baseline.jsonl");self.candidate=read_rows(ASSETS/"candidate.jsonl")
    def test_baseline(self):
        r=evaluate(self.data,self.base);self.assertTrue(r["accepted"]);self.assertAlmostEqual(r["rate"],10/12)
    def test_critical_regression(self):
        a=evaluate(self.data,self.base);b=evaluate(self.data,self.candidate)
        self.assertGreater(b["rate"],a["rate"]);self.assertFalse(b["accepted"]);self.assertEqual(compare(a,b)["regressions"],["c09"])
    def test_missing_case(self):
        r=evaluate(self.data,self.base[:-1]);self.assertLess(r["coverage"],1);self.assertFalse(r["accepted"])
    def test_unknown_case(self):
        with self.assertRaises(ValueError):evaluate(self.data,self.base+[{"id":"unknown","output":"x"}])
    def test_numeric_boundary(self):
        self.assertFalse(score({"kind":"answer","expected":["3 jours"]},"30 jours"))
    def test_normalization(self):
        self.assertTrue(score({"kind":"answer","expected":["12 euros"]},"１２   EUROS"))
    def test_strict_types(self):
        self.assertFalse(score({"kind":"json","expected":{"x":1}},{"x":True}))
    def test_extra_key(self):
        self.assertFalse(score({"kind":"json","expected":{"x":1}},{"x":1,"y":2}))
    def test_protocol_mismatch(self):
        a=evaluate(self.data,self.base);b=copy.deepcopy(a);b["dataset_hash"]="changed"
        with self.assertRaises(ValueError):compare(a,b)
    def test_duplicate_id(self):
        self.check_invalid('{"id":"a"}\n{"id":"a"}')
    def test_duplicate_key(self):self.check_invalid('{"id":"a","id":"b"}')
    def test_nan(self):self.check_invalid('{"id":"a","output":NaN}')
    def test_invalid_kind(self):
        self.data[0]["kind"]="unknown"
        with self.assertRaises(ValueError):evaluate(self.data,self.base)
    def test_missing_output(self):
        del self.base[0]["output"];self.assertFalse(evaluate(self.data,self.base)["accepted"])
    def check_invalid(self,text):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"input.jsonl";p.write_text(text)
            with self.assertRaises(ValueError):read_rows(p)
if __name__=="__main__":unittest.main()
