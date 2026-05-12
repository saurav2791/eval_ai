import unittest
import uuid
import logging
from evaluableai.client import EvaluableAI
from evaluableai.exceptions import EvaluableAIError
from evaluableai.objects.tag import Tag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestTagIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the real EvaluableAI client with a valid token
        cls.client = EvaluableAI(token="your-valid-bearer-token")  # Replace with a valid token
        cls.tag_service = Tag(cls.client)
        cls.created_tags = []

    def create_unique_tag(self, base_name, color):
        unique_suffix = uuid.uuid4().hex[:6]
        unique_name = f"{base_name[:13]}_{unique_suffix}"  # Ensure the total length is <= 20
        try:
            response = self.tag_service.create_tag(unique_name, color)
            logger.info(f"Tag created: {response}")
            self.assertEqual(response['data']['tag']['tag_name'], unique_name)
            self.assertEqual(response['data']['tag']['color'], color)
            self.created_tags.append(unique_name)
            return response['data']['tag']['tag_id'], unique_name
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_create_tag_success(self):
        self.create_unique_tag("integration_test", "#ff5733")

    def test_create_tag_missing_tag_name(self):
        with self.assertRaises(ValueError):
            self.tag_service.create_tag("", "#ff5733")

    def test_create_tags_bulk_success(self):
        tags = [
            {"tag_name": f"bulk_test1_{uuid.uuid4().hex[:6]}"},
            {"tag_name": f"bulk_test2_{uuid.uuid4().hex[:6]}", "color": "#33ff57"}
        ]
        for tag in tags:
            self.created_tags.append(tag['tag_name'])
        try:
            response = self.tag_service.create_tags_bulk(tags)
            logger.info(f"Tags created in bulk: {response}")
            self.assertEqual(len(response['data']['tags']), 2)
        except EvaluableAIError as e:
            logger.error(f"Bulk tag creation failed: {e}")
            self.fail(f"API request failed: {e}")

    def test_create_tags_bulk_missing_tag_name(self):
        tags = [{"tag_name": f"integration_test_{uuid.uuid4().hex[:6]}", "color": "#ff5733"}, {"color": "#33ff57"}]
        with self.assertRaises(ValueError):
            self.tag_service.create_tags_bulk(tags)

    def test_update_tag_success(self):
        tag_id, tag_name = self.create_unique_tag("integration_test_update", "#ff5733")
        try:
            response = self.tag_service.update_tag(tag_id, tag_name="updated_test_tag")
            logger.info(f"Tag updated: {response}")
            self.assertEqual(response['data']['tag']['tag_name'], "updated_test_tag")
            # Revert the tag name for cleanup
            self.tag_service.update_tag(tag_id, tag_name=tag_name)
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_get_tag_by_name_success(self):
        _, tag_name = self.create_unique_tag("integration_test_get", "#ff5733")
        try:
            response = self.tag_service.get_tag_by_name(tag_name)
            logger.info(f"Tag fetched: {response}")
            self.assertEqual(response['data']['tag']['tag_name'], tag_name)
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_delete_tag_by_name_success(self):
        _, tag_name = self.create_unique_tag("integration_test_delete", "#ff5733")
        try:
            response = self.tag_service.delete_tag_by_name(tag_name)
            logger.info(f"Tag deleted: {response}")
            self.assertEqual(response['message'], '1 tag is successfully deleted.')
            self.created_tags.remove(tag_name)  # Remove from cleanup list
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_add_tags_to_responses_success(self):
        try:
            response = self.tag_service.add_tags_to_responses(
                [f"integration_test1_{uuid.uuid4().hex[:6]}", f"integration_test2_{uuid.uuid4().hex[:6]}"],
                ["response_id1", "response_id2"]
            )
            logger.info(f"Tags added to responses: {response}")
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_remove_tags_from_responses_success(self):
        try:
            response = self.tag_service.remove_tags_from_responses(
                [f"integration_test1_{uuid.uuid4().hex[:6]}", f"integration_test2_{uuid.uuid4().hex[:6]}"],
                ["response_id1", "response_id2"]
            )
            logger.info(f"Tags removed from responses: {response}")
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_add_tags_to_inputs_success(self):
        try:
            response = self.tag_service.add_tags_to_inputs(
                [f"integration_test1_{uuid.uuid4().hex[:6]}", f"integration_test2_{uuid.uuid4().hex[:6]}"],
                ["input_id1", "input_id2"]
            )
            logger.info(f"Tags added to inputs: {response}")
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_remove_tags_from_inputs_success(self):
        try:
            response = self.tag_service.remove_tags_from_inputs(
                [f"integration_test1_{uuid.uuid4().hex[:6]}", f"integration_test2_{uuid.uuid4().hex[:6]}"],
                ["input_id1", "input_id2"]
            )
            logger.info(f"Tags removed from inputs: {response}")
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_get_tags_by_type_success(self):
        try:
            response = self.tag_service.get_tags_by_type("GENERIC")
            logger.info(f"Generic tags fetched: {response}")
            self.assertIn('tags', response['data'])
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    def test_get_tag_associations_success(self):
        tag_id, _ = self.create_unique_tag("integration_test_assoc", "#ff5733")
        try:
            response = self.tag_service.get_tag_associations(tag_id)
            logger.info(f"Tag associations fetched: {response}")
            self.assertIn('tag_associations', response['data'])
        except EvaluableAIError as e:
            self.fail(f"API request failed: {e}")

    @classmethod
    def tearDownClass(cls):
        # Cleanup: delete all created tags
        for tag_name in cls.created_tags:
            try:
                response = cls.tag_service.delete_tag_by_name(tag_name)
                logger.info(f"Deleted tag {tag_name}: {response}")
            except EvaluableAIError as e:
                logger.warning(f"Failed to delete tag {tag_name}: {e}")

if __name__ == '__main__':
    unittest.main()
