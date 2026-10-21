import unittest, json
from pathlib import Path
from logic import run
class LogicTests(unittest.TestCase):
    def setUp(self):
        self.records=json.loads(Path(__file__).with_name("sample_data.json").read_text())
    def test_relevant_source(self):
        self.assertEqual(run({'query':'refund'},self.records)['citations'][0]['source'],'refund-policy.md')
    def test_unknown(self):
        self.assertEqual(run({'query':'volcano'},self.records)['citations'],[])
    def test_blank(self):
        with self.assertRaises(ValueError): run({'query':' '},self.records)
    def test_case_invariance(self):
        self.assertEqual(run({'query':'REFUND'},self.records)['citations'],run({'query':'refund'},self.records)['citations'])
