"""Run: python -m unittest discover -s tests -v"""
import json
import unittest
from types import SimpleNamespace
from src.dataset import create_dataset, create_holdout, validate_rows
from src.agent import Review, run_agent, validate_response

class OfflineTests(unittest.TestCase):
    def test_corpus_labels_and_no_exact_overlap(self):
        corpus,test=create_dataset(),create_holdout()
        self.assertEqual(len(corpus),1200)
        self.assertEqual(len(test),24)
        self.assertTrue(validate_rows(corpus).isdisjoint(validate_rows(test)))
        for row in corpus+test:
            validate_response(json.dumps(row['y']),row['x'])

    def test_invalid_semantic_response_rejected(self):
        row=create_dataset()[1]
        wrong={**row['y'],'line':999}
        with self.assertRaises(ValueError):
            validate_response(json.dumps(wrong),row['x'])

    def test_pipeline_with_fake_provider(self):
        row=create_holdout()[1]
        client=SimpleNamespace(interactions=SimpleNamespace(
            create=lambda **kwargs:SimpleNamespace(output_text=json.dumps(row['y']))))
        result=run_agent(row['x'],client,'fake-test-model')
        self.assertEqual(result['y'],row['y'])
        self.assertFalse(result['stages'][0]['details']['code_executed'])

if __name__=='__main__': unittest.main()
