import unittest
import uuid
import os
import logging
from evaluableai.objects.template import Template
from evaluableai import OpenAI
from evaluableai.exceptions import EvaluableAIError, NotFoundError, APIStatusError, PermissionDeniedError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual token and setup parameters
EVALUABLEAI_TOKEN = os.getenv("EVALUABLEAI_API_KEY")
EVALUABLEAI_EVAL_LIST = ["Sentiment"]
EVALUABLEAI_TAG_NAMES = ["EXP 1", "Open AI"]

class TestTemplate(unittest.TestCase):

    def setUp(self):
        self.template_name = f"Test Template {uuid.uuid4()}"
        self.template = Template(context="Test context", name=self.template_name, prompt="Test prompt")

        # Setup OpenAI client
        self.openai_client = OpenAI(
            evaluableai_params={
                "token": EVALUABLEAI_TOKEN,
                "eval": False,
                "sampling": 1,
                "eval_list": EVALUABLEAI_EVAL_LIST,
                "async": False,
                "tag_names": EVALUABLEAI_TAG_NAMES,
            }
        )

    def tearDown(self):
        if self.template.id:
            try:
                self.template.remove()
                logger.info("Template removed successfully.")
            except EvaluableAIError as e:
                logger.error(f"Teardown failed: {e}")

    def create_template(self):
        self.template = Template(context="Test context", name=self.template_name, prompt="Test prompt")
        try:
            created_id = self.template.create()
            logger.info(f"Template created successfully. ID: {created_id}")
            return created_id
        except EvaluableAIError as e:
            logger.error(f"Error during template creation: {e}")
            self.fail("Template creation failed.")

    def test_create_and_update_template(self):
        created_id = self.create_template()
        self.assertIsNotNone(created_id)

        # Attempt to update template with the same name
        updated_name = self.template_name
        try:
            updated_template = self.template.update(name=updated_name)
            logger.info(f"Template updated successfully. New Name: {updated_template['name']}")
            self.assertEqual(updated_template['name'], updated_name)
        except EvaluableAIError as e:
            if "Template with this name already exists" in str(e):
                # Append UUID to make the name unique
                updated_name = f"{updated_name}-{uuid.uuid4()}"
                updated_template = self.template.update(name=updated_name)
                logger.info(f"Template updated successfully with unique name: {updated_template['name']}")
                self.assertIn(self.template_name, updated_template['name'])  # Verify original name is part of updated name
            else:
                self.fail(f"Error during template update: {e}")

        # Delete template
        try:
            self.template.remove()
            logger.info("Template deleted successfully.")
        except EvaluableAIError as e:
            self.fail(f"Error during template deletion: {e}")

        # Attempt to fetch deleted template
        with self.assertRaises(APIStatusError):
            self.template.fetch()

    def test_create_template_success(self):
        created_id = self.create_template()
        self.assertIsNotNone(created_id)

    def test_create_update_and_delete_template(self):
        created_id = self.create_template()
        self.assertIsNotNone(created_id)

        # Update template with a name that already exists
        updated_name = self.template_name
        try:
            updated_template = self.template.update(name=updated_name)
            logger.info(f"Template updated successfully. New Name: {updated_template['name']}")
            self.assertEqual(updated_template['name'], updated_name)
        except EvaluableAIError as e:
            if "Template with this name already exists" in str(e):
                updated_name = f"{updated_name}-{uuid.uuid4()}"
                updated_template = self.template.update(name=updated_name)
                logger.info(f"Template updated successfully with unique name: {updated_template['name']}")
                self.assertIn(self.template_name, updated_template['name'])
            else:
                self.fail(f"Error during template update: {e}")

        # Delete template
        try:
            self.template.remove()
            logger.info("Template deleted successfully.")
        except EvaluableAIError as e:
            self.fail(f"Error during template deletion: {e}")

        with self.assertRaises(NotFoundError):
            self.template.fetch()

    def test_remove_template_not_found(self):
        self.template = Template(context="Test context", name="Nonexistent Template", prompt="Test prompt")
        with self.assertRaises(NotFoundError):
            self.template.remove()

    def test_fetch_template_success(self):
        created_id = self.create_template()
        self.assertIsNotNone(created_id)

        fetched_template = self.template.fetch()
        self.assertEqual(fetched_template['name'], self.template_name)
        logger.info(f"Template fetched successfully. Name: {fetched_template['name']}")

    def test_scenario_complete_lifecycle(self):
        created_id = self.create_template()

        # Update template
        updated_name = self.template_name
        try:
            updated_template = self.template.update(name=updated_name)
            logger.info(f"Template updated successfully. New Name: {updated_template['name']}")
            self.assertEqual(updated_template['name'], updated_name)
        except EvaluableAIError as e:
            if "Template with this name already exists" in str(e):
                updated_name = f"{updated_name}-{uuid.uuid4()}"
                updated_template = self.template.update(name=updated_name)
                logger.info(f"Template updated successfully with unique name: {updated_template['name']}")
                self.assertIn(self.template_name, updated_template['name'])
            else:
                self.fail(f"Error during template update: {e}")

        # Fetch updated template
        try:
            fetched_template = self.template.fetch()
            self.assertEqual(fetched_template['name'], updated_name)
        except EvaluableAIError as e:
            logger.error(f"Error during template fetch: {e}")
            self.fail("Template fetch failed.")

        # Remove template
        try:
            self.template.remove()
            logger.info("Template removed successfully.")
            with self.assertRaises(NotFoundError):
                self.template.fetch()
        except EvaluableAIError as e:
            self.fail(f"Error during template deletion: {e}")

    def test_scenario_missing_creation_arguments(self):
        with self.assertRaises(ValueError):
            Template(context="Test context").create()

    def test_scenario_string_representation_after_remove(self):
        self.template = Template(context="Test context", name=self.template_name, prompt="Test prompt")
        with self.assertRaises(EvaluableAIError):
            self.template.create()

    def test_template_id_immutable(self):
        self.create_template()
        with self.assertRaises(AttributeError):
            self.template.id = "new-id"

    def test_update_template_success(self):
        created_id = self.create_template()
        updated_name = self.template_name
        try:
            updated_template = self.template.update(name=updated_name)
            logger.info(f"Template updated successfully. New Name: {updated_template['name']}")
            self.assertEqual(updated_template['name'], updated_name)
        except EvaluableAIError as e:
            if "Template with this name already exists" in str(e):
                updated_name = f"{updated_name}-{uuid.uuid4()}"
                updated_template = self.template.update(name=updated_name)
                logger.info(f"Template updated successfully with unique name: {updated_template['name']}")
                self.assertIn(self.template_name, updated_template['name'])
            else:
                self.fail(f"Error during template update: {e}")

    def test_prompt_generation(self):
        # Sample data
        message = "What is the only mammal that can fly?"
        ground_truth = "Bats"

        try:
            completion = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                ground_truth=ground_truth
            )
            result = completion.choices[0].message.content
            logger.info(f"Message: {message} -> Result: {result}")

            # Assertion: Check if response is not empty
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"Error generating prompt: {e}")

    def test_get_all_templates(self):
        try:
            response = self.template.get_all_templates()
            logger.info("Fetched all templates.")
            self.assertIn('templates', response['data'])
        except PermissionDeniedError as e:
            self.fail(f"Permission denied: {e}")
        except APIStatusError as e:
            self.fail(f"API status error: {e}")

    def test_create_templates_in_bulk(self):
        templates = [
            {"name": f"Test Bulk Template 1 {uuid.uuid4()}", "prompt": "Prompt 1", "context": "Context 1"},
            {"name": f"Test Bulk Template 2 {uuid.uuid4()}", "prompt": "Prompt 2", "context": "Context 2"}
        ]
        try:
            response = self.template.create_templates_in_bulk(templates)
            logger.info("Bulk template creation response.")
            self.assertEqual(response['message'], "Templates created successfully.")
        except PermissionDeniedError as e:
            self.fail(f"Permission denied: {e}")
        except APIStatusError as e:
            self.fail(f"API status error: {e}")

    def test_bulk_delete_templates(self):
        # Create templates to delete
        template_ids = []
        for i in range(2):
            created_id = self.create_template()
            self.assertIsNotNone(created_id)
            template_ids.append(created_id)

        try:
            response = self.template.bulk_delete(template_ids)
            logger.info("Bulk template deletion response.")
            self.assertEqual(response['message'], "Templates deleted successfully.")
        except PermissionDeniedError as e:
            self.fail(f"Permission denied: {e}")
        except APIStatusError as e:
            self.fail(f"API status error: {e}")


if __name__ == "__main__":
    unittest.main()
