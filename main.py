import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont  # 添加这行导入
from widgets.splash_screen import LoadingSplash
from widgets.main_window import MainWindow
from service.calculator import Calculator
from service.coordinates import CoordinateGenerator


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 设置中文字体
    font = QFont("Microsoft YaHei", 9)  # 微软雅黑
    app.setFont(font)
    
    # 启动画面
    splash = LoadingSplash()
    splash.show()
    app.processEvents()
    
    splash.update_progress(20, "正在初始化计算服务...")
    calculator = Calculator()
    
    splash.update_progress(50, "正在加载坐标生成器...")
    coord_generator = CoordinateGenerator()
    
    splash.update_progress(80, "正在构建用户界面...")
    
    window = MainWindow(calculator, coord_generator)
    
    splash.update_progress(100, "准备就绪!")
    time.sleep(0.3)
    
    splash.close()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()