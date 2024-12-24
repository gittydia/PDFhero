import unittest
from unittest.mock import patch, MagicMock
from backend.api import HeroBot

class TestHeroBot(unittest.TestCase):
    @patch('api.model')
    def test_herobot_successful_response(self, mock_model):
        # Mock the generate_content method
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model.generate_content.return_value = mock_response

        # Call HeroBot
        result = HeroBot()

        # Assert generate_content was called
        mock_model.generate_content.assert_called_once()
        
        # Assert response is returned
        self.assertEqual(result, mock_response)

    @patch('api.model') 
    def test_herobot_handles_exception(self, mock_model):
        # Mock generate_content to raise an exception
        mock_model.generate_content.side_effect = Exception("Test error")

        # Call HeroBot
        result = HeroBot()

        # Assert error string is returned
        self.assertEqual(result, "Test error")

if __name__ == '__main__':
    unittest.main()