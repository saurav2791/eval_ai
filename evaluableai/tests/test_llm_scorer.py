import unittest
import logging
import os
import time
from evaluableai.client import EvaluableAI
from evaluableai.scorers.llm_scorer import LLMScorer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestLLMScorerWithRealData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            # Set up the client with real credentials
            bearer_token = os.getenv("EVALUABLEAI_API_KEY")
            if not bearer_token:
                raise ValueError("EVALUABLEAI_API_KEY environment variable is not set.")

            cls.client = EvaluableAI(token=bearer_token)
            cls.llm_scorer = LLMScorer(client=cls.client)

            # Path to the real YAML file
            cls.yaml_file_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                '..',
                'evaluableai',
                'Scorer',
                'data',
                'llm_scorers',
                'new_llm_scorer.yaml'
            )

            if not os.path.exists(cls.yaml_file_path):
                raise FileNotFoundError(f"YAML file not found at: {cls.yaml_file_path}")

            # Initialize scorer_id and scorer_name to None
            cls.scorer_id = None
            cls.scorer_name = None
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            raise

    def test_01_create_scorer_from_yaml(self):
        try:
            # Act
            result = self.llm_scorer.create_scorer_from_yaml(self.yaml_file_path)

            # Store scorer_id and scorer_name for use in other tests
            TestLLMScorerWithRealData.scorer_id = result.get('scorer_id')
            TestLLMScorerWithRealData.scorer_name = result.get('scorer_name')

            # Assert
            self.assertIn('scorer_id', result)
            logger.info(f"Create Scorer Response: {result}")
        except Exception as e:
            logger.error(f"Failed to create scorer: {e}")
            self.fail(f"Failed to create scorer: {e}")

    def test_02_get_scorer_by_id(self):
        try:
            # Ensure scorer_id is available
            self.assertIsNotNone(TestLLMScorerWithRealData.scorer_id,
                                 "scorer_id is not set. Run test_create_scorer_from_yaml first.")

            # Add a delay to allow the scorer to be available
            time.sleep(5)

            # Act
            result = self.llm_scorer.get_scorer_by_id(TestLLMScorerWithRealData.scorer_id)

            # Assert
            self.assertEqual(result.get('scorer_id'), TestLLMScorerWithRealData.scorer_id)
            logger.info(f"Get Scorer by ID Response: {result}")
        except Exception as e:
            logger.error(f"Failed to get scorer by ID: {e}")
            self.fail(f"Failed to get scorer by ID: {e}")

    def test_03_get_scorer_by_name(self):
        try:
            # Ensure scorer_name is available
            self.assertIsNotNone(TestLLMScorerWithRealData.scorer_name,
                                 "scorer_name is not set. Run test_create_scorer_from_yaml first.")

            # Add a delay to allow the scorer to be available
            time.sleep(5)

            # Retry mechanism to handle potential delays in scorer availability
            result = None
            for _ in range(3):
                result = self.llm_scorer.get_scorer_by_name(TestLLMScorerWithRealData.scorer_name)
                if result.get('scorer_name') == TestLLMScorerWithRealData.scorer_name:
                    break
                time.sleep(2)

            # Assert
            if 'scorer_name' in result:
                self.assertEqual(result['scorer_name'], TestLLMScorerWithRealData.scorer_name)
                logger.info(f"Get Scorer by Name Response: {result}")
            else:
                self.fail(f"Failed to retrieve scorer by name: {TestLLMScorerWithRealData.scorer_name}")
        except Exception as e:
            logger.error(f"Failed to get scorer by name: {e}")
            self.fail(f"Failed to get scorer by name: {e}")

    def test_04_get_scorers(self):
        try:
            # Act
            result = self.llm_scorer.get_scorers()

            # Assert
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)  # Ensure there is at least one scorer
            logger.info(f"Get All Scorers Response: {result}")
        except Exception as e:
            logger.error(f"Failed to get all scorers: {e}")
            self.fail(f"Failed to get all scorers: {e}")

    def test_05_delete_scorer(self):
        try:
            # Ensure scorer_id is available
            self.assertIsNotNone(TestLLMScorerWithRealData.scorer_id,
                                 "scorer_id is not set. Run test_create_scorer_from_yaml first.")

            # Act
            result = self.llm_scorer.delete_scorer(TestLLMScorerWithRealData.scorer_id)

            # Assert
            self.assertEqual(result.get('message'), f'{TestLLMScorerWithRealData.scorer_id} deleted successfully')
            logger.info(f"Delete Scorer Response: {result}")
        except Exception as e:
            logger.error(f"Failed to delete scorer: {e}")
            self.fail(f"Failed to delete scorer: {e}")


if __name__ == '__main__':
    unittest.main()
