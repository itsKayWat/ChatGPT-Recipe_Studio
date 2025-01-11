import unittest
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QMessageBox
from ChatGPT_Recipe_Toolkit import SettingsDialog

class TestSettingsDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.dialog = SettingsDialog()

    def test_initialization(self):
        self.assertEqual(self.dialog.windowTitle(), "Settings")
        self.assertEqual(self.dialog.width(), 400)

    def test_ui_components(self):
        self.assertIsNotNone(self.dialog.api_key_input)
        self.assertIsNotNone(self.dialog.findChild(QDialogButtonBox))

    def test_toggle_api_key_visibility(self):
        initial_mode = self.dialog.api_key_input.echoMode()
        self.dialog.toggle_api_key_visibility()
        self.assertNotEqual(self.dialog.api_key_input.echoMode(), initial_mode)

    def test_save_settings(self):
        self.dialog.api_key_input.setText("sk-testkey")
        self.dialog.save_settings()
        self.assertEqual(self.dialog.parent.openai_api_key, "sk-testkey")

    def test_test_api_key(self):
        self.dialog.api_key_input.setText("sk-testkey")
        self.dialog.test_api_key()
        # Assuming the test_api_key method shows a QMessageBox on success
        self.assertTrue(self.dialog.findChild(QMessageBox).isVisible())

if __name__ == '__main__':
    unittest.main()
