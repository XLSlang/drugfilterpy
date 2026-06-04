# DrugFilter 3D - 分子筛选与可视化系统

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

DrugFilter 3D 是一款基于 PyQt5 和 RDKit 的分子筛选与三维可视化工具，旨在帮助药物化学和制药工程领域的研究人员快速评估候选化合物的理化性质和类药性。

## ✨ 功能特点

- **🧬 多视图三维分子显示** — 支持同时查看 4 个分子的 3D 结构，每个视图独立操控
- **🔍 SMILES 解析** — 输入标准 SMILES 表达式，自动生成三维构象并进行力场优化
- **📊 类药性评估** — 自动计算 Lipinski 五规则参数（分子量、LogP、氢键供/受体、可旋转键）
- **⚠️ 警示结构检测** — 识别分子中潜在的毒性/不稳定官能团
- **🎨 Blender 风格深色界面** — 现代化暗色主题，适配长时间研究工作
- **🖱️ 交互式操作** — 鼠标旋转、缩放分子模型，自动旋转动画



## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenGL 支持（大多数现代操作系统已内置）

### 安装

1. **克隆仓库**

```bash
git clone https://github.com/XLSlang/DrugFilter-3D.git
cd DrugFilter-3D
创建虚拟环境（推荐）

bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
安装依赖

bash
pip install -r requirements.txt
运行程序

bash
python main.py
依赖项说明
包名	版本	用途
PyQt5	≥5.15.9	图形界面框架
PyOpenGL	≥3.1.6	三维分子渲染
rdkit	≥2023.9.3	化学信息学计算与构象生成
pydantic	≥2.5.0	数据模型验证
numpy	≥1.24.0	数值计算
📖 使用指南
基本操作
解析分子：在左侧面板的 "SMILES 输入" 区域输入 1-4 个 SMILES 表达式（每行一个），点击 "解析并显示" 按钮

加载单个分子：在 "加载到选中视图" 区域输入 SMILES，选择目标视图后点击 "加载到当前视图"

切换活动视图：点击 "选择视图" 区域的按钮选择当前操作视图

分子操控
操作	方式
旋转分子	鼠标左键拖拽
缩放分子	鼠标右键拖拽 或 滚轮
自动旋转	（可在代码中启用 auto_rotate）
SMILES 示例
text
CC(=O)OC1=CC=CC=C1C(=O)O          # 阿司匹林
CN1C=NC2=C1C(=O)N(C(=O)N2C)C      # 咖啡因
CC(C)CC1=CC=C(C=C1)C(C)C(=O)O     # 布洛芬
C1=CC=C(C=C1)C=O                   # 苯甲醛
🏗️ 项目结构
text
DrugFilter-3D/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖清单
├── service/
│   ├── calculator.py       # 分子性质计算（Lipinski规则）
│   └── coordinates.py      # 3D坐标生成（RDKit构象优化）
└── widgets/
    ├── main_window.py      # 主窗口
    ├── control_panel.py    # 左侧控制面板
    ├── workspace_view.py   # 四视图工作区
    ├── mol_viewer.py       # OpenGL 分子渲染器
    ├── blender_panel.py    # Blender风格面板组件
    ├── splash_screen.py    # 启动画面
    ├── molecule_input.py   # 分子输入组件
    ├── properties_panel.py # 性质显示面板
    ├── results_table.py    # 筛选结果表格
    └── structure_viewer.py # 结构信息展示
🔬 制药应用场景
药物设计课程：直观展示分子的三维结构，帮助学生理解立体化学概念

先导化合物优化：快速评估候选分子的类药性，辅助决策优先合成哪些衍生物

虚拟筛选前处理：对大规模筛选结果进行 Lipinski 规则初筛

学术汇报展示：生成高质量的分子三维截图用于论文或答辩演示

📝 计算指标说明
Lipinski 五规则（Rule of Five）
指标	判定标准	说明
分子量 (MW)	≤ 500 Da	影响膜通透性
LogP	≤ 5	脂水分配系数，反映亲脂性
氢键供体 (HBD)	≤ 5	主要为 NH 和 OH 数量
氢键受体 (HBA)	≤ 10	主要为 N 和 O 数量
可旋转键 (RotB)	≤ 10	影响分子柔性和口服生物利用度
⚠️ 满足全部五项规则为 "Pass"，否则为 "Fail"

🤝 贡献
欢迎提交 Issue 和 Pull Request！如果你有任何改进建议或发现了 Bug，请随时联系我。

贡献流程：

Fork 本仓库

创建特性分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

打开 Pull Request

👨‍🔬 关于作者
我是一名制药专业的学生，对计算化学和药物设计充满热情。这个项目是我在学习药物化学和Python编程过程中的实践作品。

邮箱：d3434434@163.com

研究方向：计算机辅助药物设计 / 化学信息学

如果你对这个项目感兴趣，请给个 ⭐ Star 支持一下
