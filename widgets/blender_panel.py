from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


class PanelHeader(QWidget):
    """面板标题栏"""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFixedHeight(35)
        self.setCursor(Qt.SplitHCursor)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(45, 45, 48))
        painter.setPen(QPen(QColor(62, 62, 66), 1))
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)


class BlenderPanel(QFrame):
    """Blender风格面板"""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            BlenderPanel {
                background-color: #2d2d30;
                border: 1px solid #3e3e42;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # 标题栏
        self.header = QWidget()
        self.header.setFixedHeight(30)
        self.header.setStyleSheet("""
            QWidget {
                background-color: #2d2d30;
                border-bottom: 1px solid #3e3e42;
            }
        """)
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(12, 0, 12, 0)
        
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.title_label.setStyleSheet("color: #cccccc; border: none;")
        header_layout.addWidget(self.title_label)
        
        self.layout.addWidget(self.header)
        
        # 内容区域
        self.content = QWidget()
        self.content.setStyleSheet("background-color: #1e1e1e;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(8, 8, 8, 8)
        self.content_layout.setSpacing(4)
        self.layout.addWidget(self.content)
    
    def add_widget(self, widget):
        """添加widget"""
        self.content_layout.addWidget(widget)