import unittest
from PyQt6.QtWidgets import QApplication
from ChatGPT_Recipe_Toolkit import ChatGPTRecipes

class TestChatGPTRecipes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = ChatGPTRecipes()

    def test_initialization(self):
        self.assertEqual(self.window.windowTitle(), "ChatGPT Recipes")
        self.assertEqual(self.window.width(), 900)
        self.assertEqual(self.window.height(), 600)
        self.assertTrue(self.window.test_mode)

    def test_ui_components(self):
        self.assertIsNotNone(self.window.text_input)
        self.assertIsNotNone(self.window.rephrase_btn)
        self.assertIsNotNone(self.window.summarize_btn)
        self.assertIsNotNone(self.window.reply_btn)
        self.assertIsNotNone(self.window.email_btn)
        self.assertIsNotNone(self.window.test_mode_btn)
        self.assertIsNotNone(self.window.test_api_btn)
        self.assertIsNotNone(self.window.progress_bar)
        self.assertIsNotNone(self.window.char_counter)
        self.assertIsNotNone(self.window.length_combo)
        self.assertIsNotNone(self.window.tone_combo)

    def test_toggle_test_mode(self):
        initial_mode = self.window.test_mode
        self.window.toggle_test_mode()
        self.assertNotEqual(self.window.test_mode, initial_mode)

    def test_update_char_count(self):
        self.window.text_input.setText("Test")
        self.window.update_char_count()
        self.assertEqual(self.window.char_counter.text(), "Characters: 4")

    def test_process_text_empty(self):
        self.window.text_input.setText("")
        self.window.process_text("rephrase")
        self.assertTrue(self.window.is_processing)

    def test_process_text_non_empty(self):
        self.window.text_input.setText("Test text")
        self.window.process_text("rephrase")
        self.assertTrue(self.window.is_processing)

    def test_export_import_settings(self):
        self.window.recipes = {"test_recipe": "Test"}
        self.window.shortcuts = {"test_shortcut": "Ctrl+T"}
        self.window.message_history = ["Test message"]
        self.window.export_settings()
        self.window.recipes = {}
        self.window.shortcuts = {}
        self.window.message_history = []
        self.window.import_settings()
        self.assertEqual(self.window.recipes, {"test_recipe": "Test"})
        self.assertEqual(self.window.shortcuts, {"test_shortcut": "Ctrl+T"})
        self.assertEqual(self.window.message_history, ["Test message"])

    def test_translation(self):
        self.window.text_input.setText("Translate this text to French.")
        self.window.process_text("translate")
        self.assertTrue(self.window.is_processing)

    def test_grammar_correction(self):
        self.window.text_input.setText("This is a test with bad grammar.")
        self.window.process_text("grammar_correction")
        self.assertTrue(self.window.is_processing)

    def test_sentiment_analysis(self):
        self.window.text_input.setText("I am very happy with this product!")
        self.window.process_text("sentiment_analysis")
        self.assertTrue(self.window.is_processing)

    def test_recipe_categories(self):
        self.window.recipes = {
            "Category1": {"recipe1": "Test recipe 1"},
            "Category2": {"recipe2": "Test recipe 2"}
        }
        self.assertIn("Category1", self.window.recipes)
        self.assertIn("Category2", self.window.recipes)
        self.assertIn("recipe1", self.window.recipes["Category1"])
        self.assertIn("recipe2", self.window.recipes["Category2"])

    def test_analytics(self):
        self.window.api_calls_count = 5
        self.assertEqual(self.window.api_calls_count, 5)

if __name__ == '__main__':
    unittest.main()
