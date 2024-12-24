import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api import HeroBot
import unittest
from unittest.mock import patch

class TestHeroBot(unittest.TestCase):
    @patch('backend.api.model.generate_content')
    def test_herobot_successful_response(self, mock_generate):
        mock_generate.return_value.text = "Test response"
        response = HeroBot("Test message")
        self.assertEqual(response, "Test response")

if __name__ == '__main__':
    unittest.main()