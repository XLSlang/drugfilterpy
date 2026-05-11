from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math


class MolViewerWidget(QOpenGLWidget):
    """3D分子查看器"""
    def __init__(self):
        super().__init__()
        
        # 设置OpenGL格式
        fmt = QSurfaceFormat()
        fmt.setSamples(4)  # 抗锯齿
        fmt.setDepthBufferSize(24)
        self.setFormat(fmt)
        
        self.structure = None
        self.rotation_x = 30
        self.rotation_y = 45
        self.zoom = -15
        self.last_pos = None
        
        # 原子颜色映射
        self.atom_colors = {
            'C': (0.4, 0.4, 0.4),  # 灰色
            'H': (1.0, 1.0, 1.0),  # 白色
            'O': (1.0, 0.0, 0.0),  # 红色
            'N': (0.0, 0.0, 1.0),  # 蓝色
            'S': (1.0, 1.0, 0.0),  # 黄色
            'P': (1.0, 0.5, 0.0),  # 橙色
            'F': (0.0, 1.0, 0.0),  # 绿色
            'Cl': (0.0, 1.0, 0.0), # 绿色
            'Br': (0.5, 0.2, 0.0), # 棕色
            'I': (0.5, 0.0, 0.5),  # 紫色
        }
        
        # 动画定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS
        
        self.auto_rotate = False
        self.auto_rotate_angle = 0
    
    def display_structure(self, structure):
        """显示分子结构"""
        self.structure = structure
        self.update()
    
    def initializeGL(self):
        """初始化OpenGL"""
        glClearColor(0.12, 0.12, 0.12, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_MULTISAMPLE)
        
        # 设置光照
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    
    def resizeGL(self, w, h):
        """调整视图"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h if h > 0 else 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """渲染场景"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # 相机位置
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        if self.auto_rotate:
            self.auto_rotate_angle += 0.5
            glRotatef(self.auto_rotate_angle, 0, 1, 0)
        
        # 绘制网格
        self.draw_grid()
        
        # 绘制分子
        if self.structure:
            self.draw_molecule()
    
    def draw_grid(self):
        """绘制参考网格"""
        glDisable(GL_LIGHTING)
        glColor4f(0.2, 0.2, 0.2, 0.5)
        glLineWidth(1)
        
        glBegin(GL_LINES)
        for i in range(-5, 6):
            glVertex3f(i, 0, -5)
            glVertex3f(i, 0, 5)
            glVertex3f(-5, 0, i)
            glVertex3f(5, 0, i)
        glEnd()
        
        glEnable(GL_LIGHTING)
    
    def draw_molecule(self):
        """绘制分子结构"""
        coords = self.structure.coords
        atoms = self.structure.atoms
        bonds = self.structure.bonds
        
        # 绘制化学键
        glDisable(GL_LIGHTING)
        glColor3f(0.6, 0.6, 0.6)
        glLineWidth(2)
        
        glBegin(GL_LINES)
        for begin_idx, end_idx in bonds:
            begin = coords[begin_idx]
            end = coords[end_idx]
            glVertex3fv(begin)
            glVertex3fv(end)
        glEnd()
        
        glEnable(GL_LIGHTING)
        
        # 绘制原子
        for i, atom in enumerate(atoms):
            color = self.atom_colors.get(atom.element, (0.5, 0.5, 0.5))
            glColor3f(*color)
            
            glPushMatrix()
            pos = coords[i]
            glTranslatef(pos[0], pos[1], pos[2])
            
            # 根据原子大小缩放
            radius = 0.3 if atom.element == 'H' else 0.4
            
            # 绘制球体（使用GLU quadric）
            quad = gluNewQuadric()
            gluSphere(quad, radius, 16, 16)
            gluDeleteQuadric(quad)
            
            glPopMatrix()
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        self.last_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        """鼠标移动"""
        if self.last_pos is None:
            return
        
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:
            self.rotation_y += dx * 0.5
            self.rotation_x += dy * 0.5
        
        elif event.buttons() & Qt.RightButton:
            self.zoom += dy * 0.1
        
        self.last_pos = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        self.last_pos = None
    
    def wheelEvent(self, event):
        """滚轮缩放"""
        self.zoom += event.angleDelta().y() * 0.01
        self.update()