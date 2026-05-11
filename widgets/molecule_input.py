from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont


class MoleculeInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("SMILES Input")
        label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        label.setStyleSheet("color: #cccccc;")
        layout.addWidget(label)
        
        self.smiles_display = QTextEdit()
        self.smiles_display.setReadOnly(True)
        self.smiles_display.setMaximumHeight(60)
        self.smiles_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #61afef;
                border: 1px solid #3e3e42;
                border-radius: 3px;
                padding: 4px;
                font-family: 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.smiles_display)