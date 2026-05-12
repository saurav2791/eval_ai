# api_paths.py
class APIPaths:
    CREATE_TAG = "/tag"
    UPDATE_TAG = "/tag/update/{tag_id}"
    DELETE_TAG = "/tag"

    GET_ALL_LLM_SCORERS = "/llm-scorer/get-scorers"
    CREATE_LLM_SCORER = "/llm-scorer/create-scorer"
    UPDATE_LLM_SCORER = "/llm-scorer/update-scorer"
    DELETE_LLM_SCORER = "/llm-scorer/{llm_scorer_id}"
    GET_LLM_SCORER_BY_ID = "/llm-scorer/{llm_scorer_id}"

    # Add other paths as needed
