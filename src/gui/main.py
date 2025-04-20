import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QTextEdit, QLabel,
                           QComboBox, QTabWidget, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from ..api.main import app
from ..models.sentiment_analyzer import SentimentAnalyzer
from ..models.event_detector import EventDetector
from ..models.rumor_detector import RumorDetector

class AnalysisThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, analyzer, text, analysis_type):
        super().__init__()
        self.analyzer = analyzer
        self.text = text
        self.analysis_type = analysis_type

    def run(self):
        try:
            if self.analysis_type == "sentiment":
                result = self.analyzer.analyze(self.text)
            elif self.analysis_type == "events":
                result = self.analyzer.analyze_with_events(self.text)
            elif self.analysis_type == "rumors":
                result = self.analyzer.detect_rumors([{"text": self.text}])
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class FinSentrixGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.analyzer = SentimentAnalyzer()
        self.event_detector = EventDetector()
        self.rumor_detector = RumorDetector()

    def init_ui(self):
        self.setWindowTitle("FinSentrix - Financial Market Sentiment Analysis")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Sentiment Analysis Tab
        sentiment_tab = QWidget()
        sentiment_layout = QVBoxLayout(sentiment_tab)
        
        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter text to analyze...")
        sentiment_layout.addWidget(self.text_input)

        # Analysis type selection
        analysis_type_layout = QHBoxLayout()
        self.analysis_type = QComboBox()
        self.analysis_type.addItems(["Sentiment Analysis", "Event Detection", "Rumor Analysis"])
        analysis_type_layout.addWidget(QLabel("Analysis Type:"))
        analysis_type_layout.addWidget(self.analysis_type)
        sentiment_layout.addLayout(analysis_type_layout)

        # Analyze button
        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self.analyze_text)
        sentiment_layout.addWidget(analyze_btn)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        sentiment_layout.addWidget(self.results_display)

        tabs.addTab(sentiment_tab, "Analysis")

        # Settings Tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        
        # API Settings
        api_group = QWidget()
        api_layout = QVBoxLayout(api_group)
        api_layout.addWidget(QLabel("API Settings"))
        # Add API settings widgets here
        
        settings_layout.addWidget(api_group)
        tabs.addTab(settings_tab, "Settings")

    def analyze_text(self):
        text = self.text_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter text to analyze")
            return

        analysis_type = self.analysis_type.currentText().lower().replace(" ", "_")
        self.analysis_thread = AnalysisThread(self.analyzer, text, analysis_type)
        self.analysis_thread.finished.connect(self.display_results)
        self.analysis_thread.error.connect(self.display_error)
        self.analysis_thread.start()

    def display_results(self, results):
        self.results_display.clear()
        self.results_display.append("Analysis Results:")
        self.results_display.append("----------------")
        
        if isinstance(results, dict):
            for key, value in results.items():
                self.results_display.append(f"{key}: {value}")
        else:
            self.results_display.append(str(results))

    def display_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = FinSentrixGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 