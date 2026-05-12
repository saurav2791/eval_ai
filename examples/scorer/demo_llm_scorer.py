import os
import logging
from evaluableai.scorers.llm_scorer import LLMScorer
from evaluableai.client import EvaluableAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Construct the path to the YAML file
    yaml_file_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'evaluableai',
        'scorers',
        'data',
        'llm_scorers',
        'new_llm_scorer.yaml'
    )

    # Verify if the YAML file exists
    if not os.path.exists(yaml_file_path):
        logger.error(f"YAML file not found at: {yaml_file_path}")
        raise FileNotFoundError(f"YAML file not found at: {yaml_file_path}")

    # Create an instance of the LLMScorer class
    llm_scorer = LLMScorer(client=EvaluableAI())

    # Create a new LLM scorer
    try:
        create_response = llm_scorer.create_scorer_from_yaml(yaml_file_path)
        logger.info(f"Create Response: {create_response}")
    except Exception as e:
        logger.error(f"Failed to create scorer: {e}")
        return

    # Get all scorers
    try:
        all_scorers = llm_scorer.get_scorers()
        logger.info(f"All Scorers: {all_scorers}")
    except Exception as e:
        logger.error(f"Failed to get all scorers: {e}")

    # Get scorer by ID
    scorer_id = create_response.get('scorer_id')
    logger.info(f"Scorer ID: {scorer_id}")
    if scorer_id:
        try:
            get_response = llm_scorer.get_scorer_by_id(scorer_id)
            logger.info(f"Get Response by ID: {get_response}")
        except Exception as e:
            logger.error(f"Failed to get scorer by ID: {e}")

    # Get scorer by name
    scorer_name = create_response.get('scorer_name')
    logger.info(f"Scorer Name: {scorer_name}")
    if scorer_name:
        try:
            get_by_name_response = llm_scorer.get_scorer_by_name(scorer_name)
            logger.info(f"Get Response by Name: {get_by_name_response}")
        except Exception as e:
            logger.error(f"Failed to get scorer by name: {e}")


    # Delete the scorer by ID
    try:
        delete_response = llm_scorer.delete_scorer(scorer_id)
        logger.info(f"Delete Response: {delete_response}")
    except Exception as e:
        logger.error(f"Failed to delete scorer by ID: {e}")


if __name__ == "__main__":
    main()
