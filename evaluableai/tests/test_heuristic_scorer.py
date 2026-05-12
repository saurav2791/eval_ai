import unittest
import os
import time
from evaluableai.client import EvaluableAI
from evaluableai.scorers.heuristic_scorer import HeuristicScorer

class TestHeuristicScorerWithRealData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the client with real credentials
        bearer_token = os.getenv("EVALUABLEAI_API_KEY")
        cls.client = EvaluableAI(token=bearer_token)
        cls.heuristic_scorer = HeuristicScorer(client=cls.client)

        # Path to the real YAML file
        cls.yaml_file_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'evaluableai',
            'Scorer',
            'data',
            'heuristic_scorers',
            'new_heuristic_scorer.yaml'
        )

        # Initialize scorer_id and scorer_name to None
        cls.scorer_id = None
        cls.scorer_name = None

    def test_01_create_scorer_from_yaml(self):
        # Act
        result = self.heuristic_scorer.create_scorer_from_yaml(self.yaml_file_path)

        # Store scorer_id and scorer_name for use in other tests
        TestHeuristicScorerWithRealData.scorer_id = result.get('scorer_id')
        TestHeuristicScorerWithRealData.scorer_name = result.get('scorer_name')

        # Assert
        self.assertIn('scorer_id', result)
        print("Create Scorer Response:", result)

    def test_02_get_scorer_by_id(self):
        # Ensure scorer_id is available
        self.assertIsNotNone(TestHeuristicScorerWithRealData.scorer_id, "scorer_id is not set. Run test_create_scorer_from_yaml first.")

        # Add a delay to allow the scorer to be available
        time.sleep(5)

        # Act
        result = self.heuristic_scorer.get_scorer_by_id(TestHeuristicScorerWithRealData.scorer_id)

        # Assert
        self.assertEqual(result.get('scorer_id'), TestHeuristicScorerWithRealData.scorer_id)
        print("Get Scorer by ID Response:", result)

    def test_03_get_scorer_by_name(self):
        # Ensure scorer_name is available
        self.assertIsNotNone(TestHeuristicScorerWithRealData.scorer_name, "scorer_name is not set. Run test_create_scorer_from_yaml first.")

        # Add a delay to allow the scorer to be available
        time.sleep(5)

        # Retry mechanism to handle potential delays in scorer availability
        for _ in range(3):
            result = self.heuristic_scorer.get_scorer_by_name(TestHeuristicScorerWithRealData.scorer_name)
            if result.get('scorer_name') == TestHeuristicScorerWithRealData.scorer_name:
                break
            time.sleep(2)

        # Debugging: Print the full response to understand what is returned
        print("Get Scorer by Name Response:", result)

        # Assert
        if 'scorer_name' in result:
            self.assertEqual(result['scorer_name'], TestHeuristicScorerWithRealData.scorer_name)
        else:
            self.fail(f"Failed to retrieve scorer by name: {TestHeuristicScorerWithRealData.scorer_name}")

    def test_04_get_scorers(self):
        # Act
        result = self.heuristic_scorer.get_scorers()

        # Assert
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)  # Ensure there is at least one scorer
        print("Get All Scorers Response:", result)

    def test_05_update_scorer(self):
        # Ensure scorer_id is available
        self.assertIsNotNone(TestHeuristicScorerWithRealData.scorer_id, "scorer_id is not set. Run test_create_scorer_from_yaml first.")

        # Update the scorer by ID with the provided payload
        updated_data = {
            "scorer_id": TestHeuristicScorerWithRealData.scorer_id,
            "scorer_type": "user",
            "scorer_name": "meteor",
            "scorer_display_name": "METEOR",
            "scorer_function": "Pseudo code for calculateMeteorScore: 1. Align words between the generated text and the reference text(s) considering synonyms, stemming, and paraphrases. 2. Calculate precision, recall, and F-mean scores based on the alignments. 3. Apply a penalty for too many short matches to discourage word-by-word matching. 4. Combine the precision, recall, and penalty into the final METEOR score.",
            "score_type": "Double",
            "scorer_short_description": "Evaluates translation quality through advanced linguistic analysis of alignment between machine-translated text and reference translations.",
            "scorer_long_description": "The METEOR (Metric for Evaluation of Translation with Explicit ORdering) scorer extends beyond basic lexical matching to consider synonyms, paraphrasing, and stemming, providing a more nuanced assessment of translation quality. It aligns words between the generated text and reference texts, calculates precision and recall, applies a penalty for excessive short matches, and derives an F-mean score adjusted by the penalty to produce the final METEOR score. This approach aims to closely mimic human judgment, offering a balance between precision and recall in translation evaluation.",
            "scorer_variables": [
                {
                    "name": "referenceTexts",
                    "type": "List<String>",
                    "source": "ground_truth",
                    "description": "A list of reference translations."
                },
                {
                    "name": "translatedText",
                    "type": "String",
                    "source": "llm_output",
                    "description": "The machine-translated text to evaluate."
                }
            ]
        }

        try:
            update_response = self.heuristic_scorer.update_scorer(TestHeuristicScorerWithRealData.scorer_id, updated_data)
            print("Update Response:", update_response)
        except Exception as e:
            print(f"Failed to update scorer: {e}")

    def test_06_delete_scorer(self):
        # Ensure scorer_id is available
        self.assertIsNotNone(TestHeuristicScorerWithRealData.scorer_id, "scorer_id is not set. Run test_create_scorer_from_yaml first.")

        # Act
        result = self.heuristic_scorer.delete_scorer(TestHeuristicScorerWithRealData.scorer_id)

        # Assert
        self.assertEqual(result.get('message'), f'{TestHeuristicScorerWithRealData.scorer_id}was deleted successfully')
        print("Delete Scorer Response:", result)


if __name__ == '__main__':
    unittest.main()
