import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QComboBox, 
                            QLabel, QStackedWidget, QLineEdit, QDialog, 
                            QFormLayout, QMessageBox, QProgressBar, QSpinBox, 
                            QToolTip, QFileDialog, QStatusBar)
from PyQt6.QtCore import Qt, QSettings, QTimer
from PyQt6.QtGui import QIcon, QColor, QTextCursor
import keyboard
import json
import openai

class ChatGPTRecipes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatGPT Recipes")
        self.setFixedSize(900, 600)
        
        # Add test mode flag
        self.test_mode = True  # Set to True to bypass API calls
        
        # Initialize instance variables
        self.message_history = []
        self.api_calls_count = 0
        self.is_processing = False
        self.recipes = {}
        self.shortcuts = {}
        self.openai_api_key = ''
        
        # Initialize status bar first
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: white;
            }
            QPushButton {
                background-color: #2D2D2D;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
            }
            QTextEdit {
                background-color: #2D2D2D;
                color: white;
                border: 1px solid #00FFE0;
                border-radius: 5px;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: #2D2D2D;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 5px;
            }
            QProgressBar {
                border: 2px solid #00FFE0;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00FFE0;
            }
        """)
        
        # Initialize UI components
        self.init_ui()
        self.load_settings()
        self.setup_shortcuts()
        
    def init_ui(self):
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create sidebar
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        self.sidebar_layout.setSpacing(10)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)

        # Add recipe buttons
        self.rephrase_btn = self.add_sidebar_button("Rephrase", "🔄")
        self.summarize_btn = self.add_sidebar_button("Summarize", "📝")
        self.reply_btn = self.add_sidebar_button("Reply", "💬")
        self.email_btn = self.add_sidebar_button("Create Email", "✉️")
        
        # Connect buttons to functions
        self.rephrase_btn.clicked.connect(lambda: self.process_text("rephrase"))
        self.summarize_btn.clicked.connect(lambda: self.process_text("summarize"))
        self.reply_btn.clicked.connect(lambda: self.process_text("reply"))
        self.email_btn.clicked.connect(lambda: self.process_text("email"))
        
        # Add spacer
        self.sidebar_layout.addStretch()

        # Bottom buttons
        bottom_layout = QHBoxLayout()
        chat_btn = QPushButton("💭")
        settings_btn = QPushButton("⚙️")
        export_btn = QPushButton("📤 Export")
        import_btn = QPushButton("📥 Import")
        
        for btn in [chat_btn, settings_btn]:
            btn.setFixedSize(40, 40)
        
        chat_btn.clicked.connect(self.open_chat)
        settings_btn.clicked.connect(self.open_settings)
        export_btn.clicked.connect(self.export_settings)
        import_btn.clicked.connect(self.import_settings)
        
        bottom_layout.addWidget(chat_btn)
        bottom_layout.addWidget(settings_btn)
        bottom_layout.addWidget(export_btn)
        bottom_layout.addWidget(import_btn)
        self.sidebar_layout.addLayout(bottom_layout)

        # Add test mode toggle button
        self.test_mode_btn = QPushButton("🔄 Toggle Test Mode")
        self.test_mode_btn.clicked.connect(self.toggle_test_mode)
        self.sidebar_layout.addWidget(self.test_mode_btn)

        # Add API test button
        self.test_api_btn = QPushButton("🔑 Test API")
        self.test_api_btn.clicked.connect(self.test_api_connection)
        self.sidebar_layout.addWidget(self.test_api_btn)

        # Main content area
        content = QWidget()
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Instructions header
        header = QLabel("Instructions")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        content_layout.addWidget(header)

        # Text input area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Add text or keywords here...")
        self.text_input.setMinimumHeight(200)
        self.text_input.textChanged.connect(self.update_char_count)
        content_layout.addWidget(self.text_input)

        # Character counter
        self.char_counter = QLabel("Characters: 0")
        content_layout.addWidget(self.char_counter)

        # Length and Tone controls
        self.length_combo = QComboBox()
        self.length_combo.addItems(["Select Length", "Concise", "Moderate", "Detailed"])
        
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(["Select Tone", "Professional", "Casual", "Friendly", 
                                "Formal", "Technical", "Enthusiastic"])

        for control, combo in [("Length", self.length_combo), ("Tone", self.tone_combo)]:
            control_widget = QWidget()
            control_layout = QHBoxLayout(control_widget)
            control_layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel(control)
            combo.setFixedWidth(200)
            
            control_layout.addWidget(label)
            control_layout.addWidget(combo)
            control_layout.addStretch()
            
            content_layout.addWidget(control_widget)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        content_layout.addWidget(self.progress_bar)

        # Add the sidebar and content to main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(content)

        # Make sure the window is visible
        self.show()

    def add_sidebar_button(self, text, icon=""):
        btn = QPushButton(f"{icon} {text}")
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px;
                font-size: 14px;
            }
        """)
        self.sidebar_layout.addWidget(btn)
        return btn

    def load_settings(self):
        try:
            self.settings = QSettings('ChatGPTRecipes', 'Recipes')
            self.recipes = json.loads(self.settings.value('recipes', '{}'))
            self.shortcuts = json.loads(self.settings.value('shortcuts', '{}'))
            self.openai_api_key = self.settings.value('openai_api_key', '')
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.recipes = {}
            self.shortcuts = {}
            self.openai_api_key = ''

    def setup_shortcuts(self):
        try:
            for recipe_name, shortcut in self.shortcuts.items():
                keyboard.add_hotkey(shortcut, lambda n=recipe_name: self.activate_recipe(n))
        except Exception as e:
            print(f"Error setting up shortcuts: {e}")

    def activate_recipe(self, recipe_name):
        try:
            if recipe_name in self.recipes:
                self.text_input.setText(self.recipes[recipe_name])
        except Exception as e:
            print(f"Error activating recipe: {e}")

    def process_text(self, action_type):
        if self.is_processing:
            QMessageBox.warning(
                self, 
                "Processing", 
                "Please wait for the current process to complete."
            )
            return
            
        text = self.text_input.toPlainText()
        if not text:
            QMessageBox.warning(
                self, 
                "Empty Text", 
                "Please enter some text before processing."
            )
            return

        # Validate settings
        tone = self.tone_combo.currentText()
        length = self.length_combo.currentText()
        
        if tone == "Select Tone" or length == "Select Length":
            QMessageBox.warning(
                self, 
                "Missing Settings", 
                "Please select both tone and length options."
            )
            return

        try:
            self.is_processing = True
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            if self.test_mode:
                # Local test processing
                responses = {
                    "rephrase": "This is a test rephrasing of your text.",
                    "summarize": "This is a test summary of your text.",
                    "reply": "This is a test reply to your text.",
                    "email": "This is a test email based on your text."
                }
                
                test_response = (
                    f"{responses[action_type]}\n\n"
                    f"Original text: {text}\n"
                    f"Using {tone} tone and {length} length."
                )
                
                # Simulate processing delay
                def complete_test_processing():
                    try:
                        self.text_input.setText(test_response)
                        self.status_bar.showMessage("Test processing completed!", 3000)
                    finally:
                        self.is_processing = False
                        self.progress_bar.setVisible(False)
                
                QTimer.singleShot(1000, complete_test_processing)
                
            else:
                # Real API processing
                if not hasattr(self, 'openai_api_key') or not self.openai_api_key:
                    QMessageBox.warning(
                        self, 
                        "API Key Missing", 
                        "Please set your OpenAI API key in settings."
                    )
                    self.open_settings()
                    return
                
                # Your existing API processing code here
                # ...

        except Exception as e:
            self.handle_error(f"Processing error: {str(e)}")
        finally:
            if not self.test_mode:  # Only reset if not in test mode
                self.is_processing = False
                self.progress_bar.setVisible(False)

    def export_settings(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Settings", "", "JSON Files (*.json)")
            if file_path:
                settings_data = {
                    'recipes': self.recipes,
                    'shortcuts': self.shortcuts,
                    'message_history': self.message_history
                }
                with open(file_path, 'w') as f:
                    json.dump(settings_data, f, indent=4)
                QMessageBox.information(self, "Success", "Settings exported successfully!")
        except Exception as e:
            self.handle_error(f"Export error: {str(e)}")

    def import_settings(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Import Settings", "", "JSON Files (*.json)")
            if file_path:
                with open(file_path, 'r') as f:
                    settings_data = json.load(f)
                self.recipes = settings_data.get('recipes', {})
                self.shortcuts = settings_data.get('shortcuts', {})
                self.message_history = settings_data.get('message_history', [])
                self.settings.setValue('recipes', json.dumps(self.recipes))
                self.settings.setValue('shortcuts', json.dumps(self.shortcuts))
                QMessageBox.information(self, "Success", "Settings imported successfully!")
        except Exception as e:
            self.handle_error(f"Import error: {str(e)}")

    def open_chat(self):
        try:
            import webbrowser
            webbrowser.open('https://chat.openai.com')
        except Exception as e:
            self.handle_error(f"Could not open ChatGPT: {str(e)}")

    def open_settings(self):
        if self.test_mode:
            QMessageBox.information(
                self,
                "Test Mode",
                "Application is running in test mode. API key not required."
            )
            return
            
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_settings()

    def handle_error(self, error_message):
        print(f"Error: {error_message}")  # Debug print
        QMessageBox.critical(
            self, 
            "Error", 
            error_message
        )
        self.status_bar.showMessage(f"Error: {error_message}", 5000)

    def update_char_count(self):
        count = len(self.text_input.toPlainText())
        self.char_counter.setText(f"Characters: {count}")
        if count > 4000:  # OpenAI's typical limit
            self.char_counter.setStyleSheet("color: red;")
        else:
            self.char_counter.setStyleSheet("color: white;")

    def toggle_test_mode(self):
        self.test_mode = not self.test_mode
        mode = "Test Mode" if self.test_mode else "API Mode"
        self.status_bar.showMessage(f"Switched to {mode}", 3000)
        self.test_mode_btn.setText(f"🔄 {'Disable' if self.test_mode else 'Enable'} Test Mode")
        self.test_api_btn.setEnabled(not self.test_mode)

    def test_api_connection(self):
        try:
            if not hasattr(self, 'openai_api_key') or not self.openai_api_key:
                QMessageBox.warning(
                    self, 
                    "API Key Required", 
                    "Please set your OpenAI API key in settings first."
                )
                self.open_settings()
                return

            self.status_bar.showMessage("Testing API connection...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)

            def perform_api_test():
                try:
                    openai.api_key = self.openai_api_key
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": "Test"}
                        ],
                        max_tokens=1
                    )
                    QMessageBox.information(
                        self,
                        "Success",
                        "API connection successful! You can now use the application."
                    )
                except openai.RateLimitError:
                    QMessageBox.warning(
                        self,
                        "Rate Limit",
                        "API key is valid but you've hit the rate limit.\n"
                        "Please wait a few moments before trying again."
                    )
                except openai.AuthenticationError:
                    QMessageBox.critical(
                        self,
                        "Authentication Error",
                        "Invalid API key. Please check your settings."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"API test failed: {str(e)}"
                    )
                finally:
                    self.progress_bar.setVisible(False)
                    self.status_bar.clearMessage()

            # Add slight delay before API call
            QTimer.singleShot(500, perform_api_test)

        except Exception as e:
            self.handle_error(f"API test error: {str(e)}")
            self.progress_bar.setVisible(False)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Settings")
        self.setFixedWidth(400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # API Key input
        form_layout = QFormLayout()
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setText(self.parent.openai_api_key)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("OpenAI API Key:", self.api_key_input)
        
        # Show/Hide API key button
        show_key_btn = QPushButton("Show/Hide API Key")
        show_key_btn.clicked.connect(self.toggle_api_key_visibility)
        
        # Test API key button
        test_key_btn = QPushButton("Test API Key")
        test_key_btn.clicked.connect(self.test_api_key)
        
        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addLayout(form_layout)
        layout.addWidget(show_key_btn)
        layout.addWidget(test_key_btn)
        layout.addWidget(save_btn)

    def toggle_api_key_visibility(self):
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def test_api_key(self):
        try:
            api_key = self.api_key_input.text().strip()
            if not api_key:
                QMessageBox.warning(
                    self, 
                    "Invalid API Key", 
                    "Please enter an API key before testing."
                )
                return

            if not api_key.startswith('sk-'):
                QMessageBox.warning(
                    self,
                    "Invalid API Key Format",
                    "API key should start with 'sk-'. Please check your API key."
                )
                return

            try:
                import openai
            except ImportError:
                QMessageBox.critical(
                    self,
                    "Import Error",
                    "Failed to import OpenAI library. Please ensure it's installed."
                )
                return

            # Set the API key
            openai.api_key = api_key
            
            print("Starting API test...")  # Debug print
            
            try:
                # Minimal API test with lowest possible tokens
                completion = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "."}
                    ],
                    max_tokens=1,
                    temperature=0
                )
                
                print("API test completed successfully")
                
                QMessageBox.information(
                    self,
                    "Success",
                    "API key is valid! You can now use the application."
                )
                
            except openai.RateLimitError:
                print("Rate limit error")
                QMessageBox.warning(
                    self,
                    "Rate Limit",
                    "API key is valid, but you've hit the rate limit.\n\n"
                    "This usually means:\n"
                    "1. You're making too many requests\n"
                    "2. You need to add billing information\n"
                    "3. You've exceeded your current quota\n\n"
                    "The key should still work for the application."
                )
                # Still save the key since it's valid
                self.save_settings()
                
            except openai.AuthenticationError:
                print("Authentication error")
                QMessageBox.critical(
                    self,
                    "Authentication Error",
                    "Invalid API key. Please check your API key and try again."
                )
            except Exception as e:
                print(f"API call error: {str(e)}")
                QMessageBox.critical(
                    self,
                    "API Error",
                    f"Error testing API key: {str(e)}"
                )
                
        except Exception as e:
            print(f"General error: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred: {str(e)}"
            )

    def save_settings(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key.")
            return
            
        self.parent.openai_api_key = api_key
        self.parent.settings.setValue('openai_api_key', api_key)
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.accept()

def main():
    try:
        app = QApplication(sys.argv)
        window = ChatGPTRecipes()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == '__main__':
    main()