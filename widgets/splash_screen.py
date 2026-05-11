from PyQt5.QtWidgets import QSplashScreen, QProgressBar, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont


class LoadingSplash(QSplashScreen):
    def __init__(self):
        self.pixmap = QPixmap(600, 400)
        self.pixmap.fill(QColor(40, 44, 52))
        super().__init__(self.pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # 标题
        self.title_label = QLabel("DrugFilter 3D", self)
        self.title_label.setStyleSheet("color: #61afef; font-size: 32px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(0, 100, 600, 50)
        
        self.subtitle_label = QLabel("Molecular Screening System", self)
        self.subtitle_label.setStyleSheet("color: #abb2bf; font-size: 16px;")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setGeometry(0, 150, 600, 30)
        
        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 280, 400, 8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #3e4452;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #528bff, stop:1 #61afef);
                border-radius: 4px;
            }
        """)
        
        # 状态
        self.status_label = QLabel("Starting...", self)
        self.status_label.setStyleSheet("color: #abb2bf; font-size: 13px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setGeometry(0, 300, 600, 30)
        
        self.version_label = QLabel("v2.0.0", self)
        self.version_label.setStyleSheet("color: #5c6370; font-size: 12px;")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setGeometry(0, 360, 600, 20)
    
    def update_progress(self, value, message=""):
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)