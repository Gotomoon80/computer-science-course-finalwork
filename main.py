"""
学习助手小程序 - 主程序入口
作者: [Mikelawyer]
日期: 2025-10-27
版本: 1.0.0

功能:
- 🍅 倒计时钟（高精度CPU时钟）
- 🌐 网络授时（中国授时中心NTP）
- 💾 可离线运行
"""

import tkinter as tk
from gui.main_window import MainWindow
import sys

def main():
    """主函数"""
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 创建应用
        app = MainWindow(root)
        
        # 运行主循环
        root.mainloop()
        
    except Exception as e:
        print(f"程序运行错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
