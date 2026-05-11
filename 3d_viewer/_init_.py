# 3d_viewer/__init__.py

# 尝试导入OpenGL
try:
    from .mol_viewer import MolViewerWidget
except ImportError:
    MolViewerWidget = None