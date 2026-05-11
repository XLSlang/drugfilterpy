from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class ResultsTable(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Screening Results")
        label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        label.setStyleSheet("color: #cccccc;")
        layout.addWidget(label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "SMILES", "MW", "LogP", "HBD", "HBA", "RotB", "Pass"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                gridline-color: #3e3e42;
                selection-background-color: #264f78;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 4px;
                border: 1px solid #3e3e42;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)
    
    def update_results(self, results):
        """更新结果"""
        self.table.setRowCount(len(results))
        for i, mol in enumerate(results):
            self.table.setItem(i, 0, QTableWidgetItem(mol.smiles[:30]))
            self.table.setItem(i, 1, QTableWidgetItem(f"{mol.mw:.1f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{mol.logp:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(str(mol.hbd)))
            self.table.setItem(i, 4, QTableWidgetItem(str(mol.hba)))
            self.table.setItem(i, 5, QTableWidgetItem(str(mol.rot_bonds)))
            
            pass_item = QTableWidgetItem("✓" if mol.pass_rules else "✗")
            pass_item.setForeground(Qt.green if mol.pass_rules else Qt.red)
            self.table.setItem(i, 6, pass_item)