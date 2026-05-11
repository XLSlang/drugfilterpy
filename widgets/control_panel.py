from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                            QTextEdit, QScrollArea, QHBoxLayout,
                            QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class ControlPanel(QScrollArea):
    """左侧控制面板 - 极简设计"""
    molecules_submitted = pyqtSignal(list)
    structure_requested = pyqtSignal(str)  # 发送 "view_id:smiles"
    
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(250)
        self.setMaximumWidth(300)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setStyleSheet("""
            QScrollArea {
                background-color: #252526;
                border-right: 2px solid #3e3e42;
                border: none;
            }
            QLabel {
                color: #cccccc;
            }
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #094771;
            }
            QPushButton.view-btn {
                background-color: #3a3a3d;
                font-size: 12px;
                padding: 8px;
            }
            QPushButton.view-btn:hover {
                background-color: #4a4a4d;
            }
            QPushButton.view-btn:checked {
                background-color: #0e639c;
                border: 2px solid #61afef;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.5;
            }
            QGroupBox {
                color: #61afef;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 20px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
        """)
        
        self.content_widget = QWidget()
        self.setWidget(self.content_widget)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        title = QLabel("🧬 分子筛选器")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title.setStyleSheet("color: #61afef; padding: 8px 0;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # SMILES输入
        input_group = QGroupBox("SMILES 输入")
        input_layout = QVBoxLayout()
        
        self.smiles_input = QTextEdit()
        self.smiles_input.setPlaceholderText(
            "输入SMILES表达式...\n\n"
            "每行一个分子，最多4个\n\n"
            "示例:\n"
            "CC(=O)OC1=CC=CC=C1C(=O)O\n"
            "CN1C=NC2=C1C(=O)N(C(=O)N2C)C\n"
            "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O\n"
            "C1=CC=C(C=C1)C=O"
        )
        self.smiles_input.setMinimumHeight(150)
        input_layout.addWidget(self.smiles_input)
        
        # 解析按钮
        self.parse_btn = QPushButton("🔍 解析并显示")
        self.parse_btn.clicked.connect(self.on_parse)
        input_layout.addWidget(self.parse_btn)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # 视图选择
        view_group = QGroupBox("选择视图")
        view_layout = QVBoxLayout()
        view_layout.setSpacing(6)
        
        view_names = ["主视图", "对比视图", "分析视图", "参考视图"]
        self.view_btns = {}
        
        for i, name in enumerate(view_names, 1):
            btn = QPushButton(f"📌 视图{i}: {name}")
            btn.setCheckable(True)
            btn.setProperty("class", "view-btn")
            
            # 默认选中视图1
            if i == 1:
                btn.setChecked(True)
                self.current_view = 1
            
            btn.clicked.connect(lambda checked, vid=i: self.on_view_selected(vid))
            self.view_btns[i] = btn
            view_layout.addWidget(btn)
        
        view_group.setLayout(view_layout)
        layout.addWidget(view_group)
        
        # 单分子输入（用于单独加载到选中视图）
        single_group = QGroupBox("加载到选中视图")
        single_layout = QVBoxLayout()
        
        self.single_smiles = QTextEdit()
        self.single_smiles.setPlaceholderText("输入单个SMILES...")
        self.single_smiles.setMaximumHeight(80)
        single_layout.addWidget(self.single_smiles)
        
        self.load_btn = QPushButton("📤 加载到当前视图")
        self.load_btn.clicked.connect(self.on_load_to_view)
        single_layout.addWidget(self.load_btn)
        
        single_group.setLayout(single_layout)
        layout.addWidget(single_group)
        
        # 统计信息
        self.stats_label = QLabel("就绪")
        self.stats_label.setStyleSheet("""
            QLabel {
                color: #61afef;
                font-size: 12px;
                padding: 8px;
                background-color: #1e1e1e;
                border-radius: 4px;
            }
        """)
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
    
    def on_view_selected(self, view_id):
        """选择当前活动视图"""
        self.current_view = view_id
        # 取消其他按钮的选中状态
        for vid, btn in self.view_btns.items():
            if vid != view_id:
                btn.setChecked(False)
        self.view_btns[view_id].setChecked(True)
    
    def on_parse(self):
        """解析所有SMILES并分配到四个视图"""
        text = self.smiles_input.toPlainText().strip()
        if text:
            smiles_list = [s.strip() for s in text.split('\n') if s.strip()]
            # 发送完整列表，workspace会自动分配到四个视图
            self.molecules_submitted.emit(smiles_list[:4])  # 最多4个
            self.stats_label.setText(f"✅ 已解析 {len(smiles_list[:4])} 个分子")
    
    def on_load_to_view(self):
        """加载单个分子到当前选中视图"""
        smiles = self.single_smiles.toPlainText().strip()
        if smiles:
            view_id = getattr(self, 'current_view', 1)
            self.structure_requested.emit(f"{view_id}:{smiles}")
            self.stats_label.setText(f"✅ 已加载到视图{view_id}")