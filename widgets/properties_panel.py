from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class PropertiesPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Molecular Properties")
        label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        label.setStyleSheet("color: #cccccc;")
        layout.addWidget(label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Property", "Value"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                gridline-color: #3e3e42;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 4px;
                border: 1px solid #3e3e42;
            }
        """)
        layout.addWidget(self.table)
    
    def show_properties(self, molecule):
        """显示分子性质"""
        props = [
            ("Molecular Weight", f"{molecule.mw:.1f}"),
            ("LogP", f"{molecule.logp:.2f}"),
            ("H-Bond Donors", str(molecule.hbd)),
            ("H-Bond Acceptors", str(molecule.hba)),
            ("Rotatable Bonds", str(molecule.rot_bonds)),
            ("Lipinski Rule", "✓ Pass" if molecule.pass_rules else "✗ Fail"),
            ("Alerts", str(molecule.alert_count))
        ]
        
        self.table.setRowCount(len(props))
        for i, (name, value) in enumerate(props):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            item = QTableWidgetItem(value)
            if "Pass" in value:
                item.setForeground(Qt.green)
            elif "Fail" in value:
                item.setForeground(Qt.red)
            self.table.setItem(i, 1, item)