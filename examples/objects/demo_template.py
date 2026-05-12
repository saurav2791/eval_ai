import os
import logging
from evaluableai.client import EvaluableAI
from evaluableai.objects.template import Template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the EvaluableAI client
token = os.getenv("EVALUABLEAI_API_KEY")
client = EvaluableAI(token)

# Example template data
template_data = {
    "name": "Example Template",
    "prompt": "What is {{x}} and how does it relate to {{y}}?",
    "context": "This context focuses on {{c}}."
}

# Function to demonstrate the usage of the Template class
def demo_template_operations():
    # Create a Template instance
    template = Template(name=template_data["name"], prompt=template_data["prompt"], context=template_data["context"])

    # Create the template
    logger.info("\n--- Creating Template ---")
    template_id = template.create()
    if template_id:
        logger.info(f"Template created successfully with ID: {template_id}")

    # Fetch the created template
    logger.info("\n--- Fetching Template ---")
    fetched_template = template.fetch(id=template_id)
    logger.info(f"Fetched Template: {fetched_template}")

    # Update the template
    logger.info("\n--- Updating Template ---")
    updated_template = template.update(name="Updated Example Template")
    logger.info(f"Updated Template: {updated_template}")

    # Restore the template if it was deleted
    logger.info("\n--- Restoring Template ---")
    restored_template = template.restore()
    logger.info(f"Restored Template: {restored_template}")

    # List all deleted templates
    logger.info("\n--- Listing Deleted Templates ---")
    deleted_templates = template.list_of_deletion()
    logger.info(f"Deleted Templates: {deleted_templates}")

    # Fetch all templates
    logger.info("\n--- Fetching All Templates ---")
    all_templates = template.get_all_templates()
    logger.info(f"All Templates: {all_templates}")

    # Create templates in bulk
    logger.info("\n--- Creating Templates in Bulk ---")
    bulk_templates = [
        {"name": "Bulk Template 1", "prompt": "Explain {{x}}.", "context": "Context for {{x}}."},
        {"name": "Bulk Template 2", "prompt": "Describe {{y}}.", "context": "Context for {{y}}."}
    ]
    bulk_create_response = template.create_templates_in_bulk(bulk_templates)
    logger.info(f"Bulk Create Response: {bulk_create_response}")

    # Bulk delete templates
    logger.info("\n--- Bulk Deleting Templates ---")
    template_ids_to_delete = [template_id]  # Add more template IDs as needed
    bulk_delete_response = template.bulk_delete(template_ids_to_delete)
    logger.info(f"Bulk Delete Response: {bulk_delete_response}")

    # Remove the template
    logger.info("\n--- Removing Template ---")
    delete_message = template.remove(id=template_id)
    logger.info(f"Delete Message: {delete_message}")

if __name__ == "__main__":
    demo_template_operations()
