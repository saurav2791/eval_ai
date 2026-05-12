import os
import logging
from evaluableai.scorers.heuristic_scorer import HeuristicScorer
from evaluableai.client import EvaluableAI

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting the script...")

    # Construct the path to the YAML file
    yaml_file_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'evaluableai',
        'scorers',
        'data',
        'heuristic_scorers',
        'new_heuristic_scorer.yaml'
    )

    # Verify if the YAML file exists
    if not os.path.exists(yaml_file_path):
        logging.error(f"YAML file not found at: {yaml_file_path}")
        raise FileNotFoundError(f"YAML file not found at: {yaml_file_path}")

    logging.info(f"YAML file found at: {yaml_file_path}")

    # Create an instance of the HeuristicScorer class
    heuristic_scorer = HeuristicScorer(client=EvaluableAI())
    logging.info("HeuristicScorer instance created.")

    # Create a new Heuristic scorer
    try:
        create_response = heuristic_scorer.create_scorer_from_yaml(yaml_file_path)
        logging.info(f"Create Response: {create_response}")
    except Exception as e:
        logging.error(f"Failed to create scorer: {e}")
        return

    # Get all scorers
    try:
        all_scorers = heuristic_scorer.get_scorers()
        logging.info(f"All Scorers: {all_scorers}")
    except Exception as e:
        logging.error(f"Failed to get all scorers: {e}")

    # Get scorer by name
    scorer_name = create_response.get('scorer_name')
    if scorer_name:
        try:
            get_by_name_response = heuristic_scorer.get_scorer_by_name(scorer_name)
            logging.info(f"Get Response by Name: {get_by_name_response}")
        except Exception as e:
            logging.error(f"Failed to get scorer by name: {e}")

    # Get scorer by ID
    scorer_id = create_response.get('scorer_id')
    if scorer_id:
        try:
            get_response = heuristic_scorer.get_scorer_by_id(scorer_id)
            logging.info(f"Get Response by ID: {get_response}")
        except Exception as e:
            logging.error(f"Failed to get scorer by ID: {e}")

        # Update the scorer by ID with the provided payload
        updated_data = {
            "scorer_id": scorer_id,
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
            update_response = heuristic_scorer.update_scorer(scorer_id, updated_data)
            logging.info(f"Update Response: {update_response}")
        except Exception as e:
            logging.error(f"Failed to update scorer: {e}")

    # Delete the scorer by ID (uncomment if needed)
    try:
        delete_response = heuristic_scorer.delete_scorer(scorer_id)
        logging.info(f"Delete Response: {delete_response}")
    except Exception as e:
        logging.error(f"Failed to delete scorer by ID: {e}")

if __name__ == "__main__":
    logging.info("Executing the main function...")
    main()
    logging.info("Main function execution completed.")
