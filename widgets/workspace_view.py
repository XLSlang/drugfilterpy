from PyQt5.QtWidgets import QWidget, QSplitter
from PyQt5.QtCore import Qt
from widgets.blender_panel import BlenderPanel


# 尝试导入OpenGL查看器
try:
    from widgets.mol_viewer import MolViewerWidget
    HAS_OPENGL = True
except ImportError:
    HAS_OPENGL = False


class WorkspaceView(QWidget):
    """四面板3D分子视图工作区 - 支持拖动缩放"""
    def __init__(self, calculator, coord_generator):
        super().__init__()
        self.calculator = calculator
        self.coord_generator = coord_generator
        self.mol_views = {}
        self.viewer_panels = {}
        self.setup_ui()
    
    def setup_ui(self):
        # 主垂直分割器
        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #3e3e42;
                height: 3px;
            }
            QSplitter::handle:hover {
                background-color: #61afef;
                height: 4px;
            }
        """)
        
        # 上半部分水平分割器（视图1和2）
        self.top_splitter = QSplitter(Qt.Horizontal)
        self.top_splitter.setChildrenCollapsible(False)
        
        # 下半部分水平分割器（视图3和4）
        self.bottom_splitter = QSplitter(Qt.Horizontal)
        self.bottom_splitter.setChildrenCollapsible(False)
        
        # 创建四个视图
        view_configs = [
            ("3D视图1 - 主视图", (30, 45)),
            ("3D视图2 - 对比视图", (30, 135)),
            ("3D视图3 - 分析视图", (60, 45)),
            ("3D视图4 - 参考视图", (60, 135))
        ]
        
        for i, (name, (rot_x, rot_y)) in enumerate(view_configs, 1):
            panel = BlenderPanel(name)
            
            if HAS_OPENGL:
                viewer = MolViewerWidget()
                viewer.rotation_x = rot_x
                viewer.rotation_y = rot_y
                viewer.setMinimumSize(200, 200)
                panel.add_widget(viewer)
                self.mol_views[i] = viewer
            else:
                # OpenGL不可用时的占位符
                from PyQt5.QtWidgets import QLabel
                placeholder = QLabel(f"3D视图 {i}\n需要安装PyOpenGL")
                placeholder.setStyleSheet("color: #888; font-size: 16px;")
                placeholder.setAlignment(Qt.AlignCenter)
                panel.add_widget(placeholder)
            
            self.viewer_panels[i] = panel
            
            # 添加到对应的分割器
            if i <= 2:
                self.top_splitter.addWidget(panel)
            else:
                self.bottom_splitter.addWidget(panel)
        
        # 组装布局
        self.main_splitter.addWidget(self.top_splitter)
        self.main_splitter.addWidget(self.bottom_splitter)
        self.main_splitter.setSizes([500, 500])  # 上下各占一半
        
        # 设置主布局
        from PyQt5.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(self.main_splitter)
    
    def process_molecules(self, smiles_list):
        """解析并分配分子到四个视图"""
        for i, smiles in enumerate(smiles_list[:4], 1):
            try:
                structure = self.coord_generator.generate_3d(smiles)
                if i in self.mol_views:
                    self.mol_views[i].display_structure(structure)
            except Exception as e:
                print(f"视图{i}加载失败: {e}")
    
    def show_structure(self, data):
        """显示单个结构到指定视图"""
        if ':' in data:
            view_id_str, smiles = data.split(':', 1)
            view_id = int(view_id_str)
        else:
            view_id = 1
            smiles = data
        
        try:
            structure = self.coord_generator.generate_3d(smiles)
            if view_id in self.mol_views:
                self.mol_views[view_id].display_structure(structure)
        except Exception as e:
            print(f"视图{view_id}加载失败: {e}")