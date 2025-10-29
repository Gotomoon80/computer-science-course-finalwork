"""
项目结构自动生成脚本
运行此脚本将创建完整的项目目录结构和文件框架
"""

import os

# 项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("  学习助手小程序 - 项目结构生成器")
print("=" * 60)
print(f"\n📁 项目路径: {project_root}\n")

# 目录结构
dirs = [
    "modules",
    "gui",
    "utils",
    "data",
    "data/logs",
    "resources",
    "resources/icons",
    "resources/images"
]

# 创建目录
print("📂 创建目录结构...")
for d in dirs:
    path = os.path.join(project_root, d)
    os.makedirs(path, exist_ok=True)
    print(f"  ✓ {d}")
    
    # 为Python包创建__init__.py
    if d in ["modules", "gui", "utils"]:
        init_file = os.path.join(path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('"""{}模块"""\n'.format(d))
            print(f"    + __init__.py")

# 创建主要文件（仅创建空文件，不覆盖已存在的）
files = {
    "main.py": '''"""
学习助手小程序 - 主程序入口
作者: [你的名字]
日期: 2025-10-27
"""

import tkinter as tk
from gui.main_window import MainWindow

def main():
    """主函数"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
''',
    "config.json": '''{
  "app": {
    "name": "学习助手",
    "version": "1.0.0",
    "author": "你的名字"
  },
  "pomodoro": {
    "work_duration": 1500,
    "break_duration": 300,
    "long_break_duration": 900,
    "sessions_before_long_break": 4
  },
  "time_sync": {
    "auto_sync": true,
    "sync_interval": 3600,
    "ntp_servers": [
      "time.windows.com",
      "ntp.aliyun.com",
      "cn.ntp.org.cn",
      "pool.ntp.org"
    ],
    "timeout": 3
  },
  "appearance": {
    "theme": "light",
    "primary_color": "#4A90E2",
    "secondary_color": "#50C9CE",
    "accent_color": "#F5A623",
    "background_color": "#F8F9FA",
    "font_family": "Microsoft YaHei",
    "font_size": 12
  },
  "database": {
    "path": "data/study.db"
  }
}
''',
    "modules/timer.py": '''"""定时器模块"""
# 待实现
''',
    "modules/calculator.py": '''"""计算器模块"""
# 待实现
''',
    "modules/todo.py": '''"""待办事项模块"""
# 待实现
''',
    "modules/statistics.py": '''"""数据统计模块"""
# 待实现
''',
    "gui/main_window.py": '''"""主窗口界面"""
import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("学习助手 - Study Assistant")
        self.master.geometry("800x600")
        
        # 待实现
        label = tk.Label(master, text="学习助手", font=("Microsoft YaHei", 24))
        label.pack(pady=100)
''',
    "gui/timer_window.py": '''"""定时器窗口界面"""
# 待实现
''',
    "gui/calc_window.py": '''"""计算器窗口界面"""
# 待实现
''',
    "gui/todo_window.py": '''"""待办事项窗口界面"""
# 待实现
''',
    "utils/database.py": '''"""数据库管理模块"""
# 待实现
''',
    "utils/time_sync.py": '''"""网络授时模块"""
# 待实现
''',
    "utils/clock.py": '''"""高精度时钟模块"""
# 待实现
''',
    "utils/validator.py": '''"""输入验证模块"""
# 待实现
''',
    ".gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/
*.spec

# IDE
.vscode/
.idea/
*.swp
*.swo

# 数据库
*.db
*.sqlite3

# 日志
*.log
data/logs/

# OS
.DS_Store
Thumbs.db
'''
}

print("\n📄 创建文件...")
for filename, content in files.items():
    filepath = os.path.join(project_root, filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {filename}")
    else:
        print(f"  ⊙ {filename} (已存在，跳过)")

print("\n" + "=" * 60)
print("  ✅ 项目结构创建完成！")
print("=" * 60)
print("\n📋 下一步操作：")
print("  1. 安装依赖: pip install -r requirements.txt")
print("  2. 查看文档: README.md")
print("  3. 开始编码: 从 utils/clock.py 开始")
print("\n🚀 祝开发顺利！\n")
