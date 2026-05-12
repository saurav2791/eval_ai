import os
import logging
from evaluableai.client import EvaluableAI
from evaluableai.exceptions import EvaluableAIError
from evaluableai.objects.tag import Tag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize client and service
valid_token = os.getenv("EVALUABLEAI_API_KEY")
client = EvaluableAI(valid_token)
tag_service = Tag(client)

def create_tag(tag_name, color=None):
    try:
        response = tag_service.create_tag(tag_name, color)
        logger.info("Tag created: %s", response)
        return response['data']['tag']['tag_id']
    except EvaluableAIError as e:
        logger.error("Error creating tag: %s", e)
        return None

def create_tags_bulk(tags):
    try:
        response = tag_service.create_tags_bulk(tags)
        logger.info("Tags created: %s", response)
    except EvaluableAIError as e:
        logger.error("Error creating multiple tags: %s", e)

def update_tag(tag_id, tag_name):
    try:
        response = tag_service.update_tag(tag_id=tag_id, tag_name=tag_name)
        logger.info("Tag updated: %s", response)
    except EvaluableAIError as e:
        logger.error("Error updating tag: %s", e)

def get_tag_by_name(tag_name):
    try:
        response = tag_service.get_tag_by_name(tag_name)
        logger.info("Tag fetched by name: %s", response)
    except EvaluableAIError as e:
        logger.error("Error fetching tag by name: %s", e)

def get_tags_by_type(tag_type):
    try:
        response = tag_service.get_tags_by_type(tag_type)
        logger.info("Generic tags by type: %s", response)
    except EvaluableAIError as e:
        logger.error("Error fetching tags by type: %s", e)

def add_tags_to_responses(tags, responses):
    try:
        response = tag_service.add_tags_to_responses(tags, responses)
        logger.info("Tags added to responses: %s", response)
    except EvaluableAIError as e:
        logger.error("Error adding tags to responses: %s", e)

def add_tags_to_inputs(tags, inputs):
    try:
        response = tag_service.add_tags_to_inputs(tags, inputs)
        logger.info("Tags added to inputs: %s", response)
    except EvaluableAIError as e:
        logger.error("Error adding tags to inputs: %s", e)

def remove_tags_from_inputs(tags, inputs):
    try:
        response = tag_service.remove_tags_from_inputs(tags, inputs)
        logger.info("Tags removed from inputs: %s", response)
    except EvaluableAIError as e:
        logger.error("Error removing tags from inputs: %s", e)

def get_tag_associations(tag_id):
    try:
        response = tag_service.get_tag_associations(tag_id=tag_id)
        logger.info("Tag associations: %s", response)
    except EvaluableAIError as e:
        logger.error("Error fetching tag associations: %s", e)

def delete_tag_by_name(tag_name):
    try:
        response = tag_service.delete_tag_by_name(tag_name)
        logger.info("Tag deleted: %s", response)
    except EvaluableAIError as e:
        logger.error("Error deleting tag: %s", e)

def remove_tags_from_responses(tags, responses):
    try:
        response = tag_service.remove_tags_from_responses(tags, responses)
        if response.get('message'):
            logger.info(response['message'])
        else:
            logger.info("Tags removed from responses: %s", response)
    except EvaluableAIError as e:
        logger.error("Error removing tags from responses: %s", e)

if __name__ == "__main__":
    # Create a single tag
    tag_id = create_tag("example_tag", "#ff5733")

    if tag_id:
        # Create multiple tags
        create_tags_bulk([
            {"tag_name": "to_be_deleted_3"},
            {"tag_name": "to_be_deleted_4", "color": "#ff2344"}
        ])

        # Update the tag
        update_tag(tag_id, "updated1_tag")
        update_tag(tag_id, "example_tag")

        # Get the tag by name
        get_tag_by_name("example_tag")

        # Get tags by type
        get_tags_by_type("GENERIC")

        # Add tags to responses
        add_tags_to_responses(["example_tag1", "example_tag2"], ["response1", "response2"])

        # Add tags to inputs
        add_tags_to_inputs(["example_tag1", "example_tag2"], ["input1", "input2"])

        # Remove tags from inputs
        remove_tags_from_inputs(["example_tag1", "example_tag2"], ["input1", "input2"])

        # Get tag associations
        get_tag_associations(tag_id)

        # Delete the tag by name
        delete_tag_by_name("example_tag")

        # Remove tags from responses
        remove_tags_from_responses(["example_tag1", "example_tag2"], ["response1", "response2"])
    else:
        logger.error("Tag creation failed; subsequent operations were not performed.")
