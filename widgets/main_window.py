from PyQt5.QtWidgets import QMainWindow, QSplitter, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from widgets.control_panel import ControlPanel
from widgets.workspace_view import WorkspaceView


class MainWindow(QMainWindow):
    def __init__(self, calculator, coord_generator):
        super().__init__()
        self.calculator = calculator
        self.coord_generator = coord_generator
        
        self.setWindowTitle("DrugFilter 3D - 分子筛选与可视化系统")
        self.setGeometry(100, 100, 1920, 1080)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QSplitter::handle {
                background-color: #3e3e3e;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #61afef;
            }
        """)
        
        # 中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主水平布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 主分割器（左：控制面板，右：四视图）
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        
        # 左侧控制面板
        self.control_panel = ControlPanel()
        
        # 右侧四个3D视图
        self.workspace = WorkspaceView(self.calculator, self.coord_generator)
        
        self.main_splitter.addWidget(self.control_panel)
        self.main_splitter.addWidget(self.workspace)
        self.main_splitter.setSizes([280, 1640])  # 左窄右宽
        
        main_layout.addWidget(self.main_splitter)
        
        # 连接信号
        self.control_panel.molecules_submitted.connect(
            self.workspace.process_molecules
        )
        self.control_panel.structure_requested.connect(
            self.workspace.show_structure
        )
        
        # 状态栏
        self.statusBar().showMessage("就绪 - 输入SMILES并点击解析按钮开始")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #007acc;
                color: white;
                font-weight: bold;
                padding: 6px;
                font-size: 12px;
            }
        """)