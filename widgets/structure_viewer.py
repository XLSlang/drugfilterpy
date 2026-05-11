from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont


class StructureViewer3D(QWidget):
    def __init__(self, coord_generator):
        super().__init__()
        self.coord_generator = coord_generator
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Structure Info")
        label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        label.setStyleSheet("color: #cccccc;")
        layout.addWidget(label)
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 3px;
                padding: 4px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.info_text)
    
    def update_structure(self, structure):
        """更新结构信息"""
        info = f"Atoms: {len(structure.atoms)}\n"
        info += f"Bonds: {len(structure.bonds)}\n"
        info += f"Elements: {set(a.element for a in structure.atoms)}"
        self.info_text.setText(info)