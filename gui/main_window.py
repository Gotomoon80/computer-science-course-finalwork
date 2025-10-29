"""主窗口界面"""
import tkinter as tk
from tkinter import ttk, messagebox
from modules.timer import PrecisionTimer
import threading
import time
import winsound  # Windows音效
from tkinter import font as tkfont

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("学习助手 - Study Assistant")
        self.master.geometry("550x550")
        self.master.resizable(False, False)
        
        # 配色方案（清新蓝）
        self.color_themes = {
            '蓝色': {
                'primary': '#4A90E2',
                'secondary': '#50C9CE',
                'accent': '#F5A623',
                'background': '#E8F4F8',
                'text': '#333333'
            },
            '绿色': {
                'primary': '#27AE60',
                'secondary': '#2ECC71',
                'accent': '#F39C12',
                'background': '#E8F8F0',
                'text': '#333333'
            },
            '紫色': {
                'primary': '#8E44AD',
                'secondary': '#9B59B6',
                'accent': '#E67E22',
                'background': '#F4ECF7',
                'text': '#333333'
            },
            '粉色': {
                'primary': '#E91E63',
                'secondary': '#F06292',
                'accent': '#FF9800',
                'background': '#FCE4EC',
                'text': '#333333'
            },
            '橙色': {
                'primary': '#FF5722',
                'secondary': '#FF7043',
                'accent': '#FFC107',
                'background': '#FFF3E0',
                'text': '#333333'
            },
            '灰色': {
                'primary': '#607D8B',
                'secondary': '#78909C',
                'accent': '#FF9800',
                'background': '#ECEFF1',
                'text': '#333333'
            }
        }
        
        self.current_theme = '蓝色'
        self.colors = self.color_themes[self.current_theme]
        
        self.master.configure(bg=self.colors['background'])
        
        # 全屏模式标志
        self.is_fullscreen = False
        
        # 创建定时器（25分钟）
        self.duration_minutes = 25  # 初始时长（分钟）
        self.timer = PrecisionTimer(self.duration_minutes * 60)
        self.update_running = False
        self.realtime_running = False
        
        # 创建界面
        self.create_widgets()
        
        # 绑定全屏快捷键
        self.master.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.master.bind('<Escape>', lambda e: self.exit_fullscreen())
        
        # 启动时尝试同步时间
        self.sync_time_on_start()
        
        # 设置messagebox字体大小
        self.setup_messagebox_font()
        
        # 播放启动音效
        self.play_startup_sound()
    
    def setup_messagebox_font(self):
        """设置messagebox字体大小"""
        try:
            # 设置默认对话框字体
            default_font = tkfont.nametofont("TkDefaultFont")
            default_font.configure(size=12)  # 调大字体
            
            text_font = tkfont.nametofont("TkTextFont")
            text_font.configure(size=12)
            
            caption_font = tkfont.nametofont("TkCaptionFont")
            caption_font.configure(size=11)
        except:
            pass
    
    def toggle_fullscreen(self):
        """切换全屏模式（F11）"""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # 进入全屏聚焦模式
            self.master.attributes('-fullscreen', True)
            self.master.configure(bg='#2C3E50')  # 深色背景
            
            # 计算屏幕中心位置
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            
            # 添加提示标签（屏幕顶部）
            self.fullscreen_hint = tk.Label(
                self.master,
                text="聚焦模式 | 按 ESC 或 F11 退出",
                font=("Consolas", 10),
                bg='#2C3E50',
                fg='#95A5A6'
            )
            self.fullscreen_hint.place(relx=0.5, rely=0.02, anchor='n')
            
        else:
            # 退出全屏
            self.master.attributes('-fullscreen', False)
            self.master.configure(bg=self.colors['background'])
            
            # 移除提示标签
            if hasattr(self, 'fullscreen_hint'):
                self.fullscreen_hint.destroy()
    
    def exit_fullscreen(self):
        """退出全屏模式（ESC）"""
        if self.is_fullscreen:
            self.toggle_fullscreen()
    
    def play_startup_sound(self):
        """播放启动音效 - 4音节和弦（流畅无卡顿）"""
        def play():
            try:
                # 4音节和弦: C - E - G - C (八度)
                winsound.Beep(523, 80)   # C (中音Do)
                winsound.Beep(659, 80)   # E (中音Mi)
                winsound.Beep(784, 80)   # G (中音Sol)
                winsound.Beep(1047, 100) # C (高音Do) - 略长
            except:
                pass  # 如果播放失败则静默忽略
        
        threading.Thread(target=play, daemon=True).start()
    
    def play_pause_sound(self):
        """播放暂停音效 - 2音节高低配和弦"""
        def play():
            try:
                winsound.Beep(880, 100)  # A (高音La)
                winsound.Beep(523, 100)  # C (中音Do) - 高低配
            except:
                pass
        
        threading.Thread(target=play, daemon=True).start()
    
    def play_reset_sound(self):
        """播放重置音效 - 3音节低到高和弦"""
        def play():
            try:
                # 3音节低到高: G - C - E
                winsound.Beep(392, 90)   # G (低音Sol)
                winsound.Beep(523, 90)   # C (中音Do)
                winsound.Beep(659, 100)  # E (中音Mi) - 略长
            except:
                pass
        
        threading.Thread(target=play, daemon=True).start()
    
    def play_click_sound(self):
        """播放按钮点击音效 - Ka"""
        def play():
            try:
                winsound.Beep(800, 80)  # 800Hz, 80ms
            except:
                pass
        
        threading.Thread(target=play, daemon=True).start()
    
    def play_complete_sound(self):
        """播放完成音效 - 5音节重复4遍"""
        def play():
            try:
                # 5音节和弦: C - E - G - A - C (高八度)
                melody = [
                    (523, 90),   # C (中音Do)
                    (659, 90),   # E (中音Mi)
                    (784, 90),   # G (中音Sol)
                    (880, 90),   # A (中音La)
                    (1047, 100)  # C (高音Do) - 略长
                ]
                
                # 重复4遍
                for _ in range(4):
                    for freq, duration in melody:
                        winsound.Beep(freq, duration)
                    time.sleep(0.15)  # 每遍之间略停顿
            except:
                pass
        
        threading.Thread(target=play, daemon=True).start()
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        self.title_frame = tk.Frame(self.master, bg=self.colors['primary'], height=85)
        self.title_frame.pack(fill='x')
        self.title_frame.pack_propagate(False)
        
        # 标题文字（居中）
        self.title_label = tk.Label(
            self.title_frame,
            text="🎯 张弛有度",
            font=("SimHei", 20, "bold"),  # 16⇒20
            bg=self.colors['primary'],
            fg='white'
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # 实时时间显示（标题栏右侧）
        self.header_time_label = tk.Label(
            self.title_frame,
            text="",
            font=("Consolas", 16, "bold"),  # 14⇒16
            bg=self.colors['primary'],
            fg='white'
        )
        self.header_time_label.pack(side='right', padx=20, pady=25)
        
        # 作者信息（右下角）
        self.author_label = tk.Label(
            self.title_frame,
            text="Mikelawyer",
            font=("Consolas", 9),  # 8⇒9
            bg=self.colors['primary'],
            fg='#E8F4F8'
        )
        self.author_label.place(relx=1.0, rely=1.0, anchor='se', x=-12, y=-6)
        
        # 主内容区
        self.content_frame = tk.Frame(self.master, bg=self.colors['background'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=12)
        
        # 番茄钟定时器
        self.create_timer_section(self.content_frame)
        
        # 颜色主题切换按钮
        self.create_theme_buttons(self.content_frame)
        
        # 同步状态
        self.create_sync_status(self.content_frame)
        
        # 启动实时时钟更新
        self.realtime_running = True
        self.update_realtime_clock()
    
    def create_timer_section(self, parent):
        """创建定时器区域"""
        self.timer_frame = tk.LabelFrame(
            parent,
            text="⏱ 专注计时器",
            font=("SimHei", 12, "bold"),  # 10⇒12
            bg=self.colors['background'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        self.timer_frame.pack(fill='x', pady=6)
        
        # 时长调节区（+/- 按钮）
        duration_control = tk.Frame(self.timer_frame, bg=self.colors['background'])
        duration_control.pack(pady=6)
        
        minus_btn = tk.Button(
            duration_control,
            text="− 1分钟",
            command=self.decrease_duration,
            width=10,
            font=("SimHei", 10),  # 9⇒10
            bg='#E74C3C',
            fg='white',
            relief='flat',
            cursor='hand2'
        )
        minus_btn.grid(row=0, column=0, padx=5)
        
        self.duration_label = tk.Label(
            duration_control,
            text=f"{self.duration_minutes} 分钟",
            font=("SimHei", 12, "bold"),  # 10⇒12
            bg=self.colors['background'],
            fg=self.colors['text'],
            width=10
        )
        self.duration_label.grid(row=0, column=1, padx=8)
        
        plus_btn = tk.Button(
            duration_control,
            text="+ 1分钟",
            command=self.increase_duration,
            width=10,
            font=("SimHei", 10),  # 9⇒10
            bg='#27AE60',
            fg='white',
            relief='flat',
            cursor='hand2'
        )
        plus_btn.grid(row=0, column=2, padx=5)
        
        # 时间显示
        self.time_label = tk.Label(
            self.timer_frame,
            text="25:00",
            font=("Arial", 40, "bold"),  # 32⇒40
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        self.time_label.pack(pady=10)
        
        # 按钮区
        button_frame = tk.Frame(self.timer_frame, bg=self.colors['background'])
        button_frame.pack(pady=8)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶ 开始",
            command=self.start_timer,
            width=9,
            height=1,
            font=("SimHei", 11),  # 10⇒11
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            cursor='hand2'
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = tk.Button(
            button_frame,
            text="⏸ 暂停",
            command=self.pause_timer,
            width=9,
            height=1,
            font=("SimHei", 11),  # 10⇒11
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            cursor='hand2',
            state='disabled'
        )
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.reset_btn = tk.Button(
            button_frame,
            text="↻ 重置",
            command=self.reset_timer,
            width=9,
            height=1,
            font=("SimHei", 11),  # 10⇒11
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2'
        )
        self.reset_btn.grid(row=0, column=2, padx=5)
    
    def create_theme_buttons(self, parent):
        """创建颜色主题切换按钮"""
        theme_frame = tk.Frame(parent, bg=self.colors['background'])
        theme_frame.pack(fill='x', pady=8)
        
        theme_label = tk.Label(
            theme_frame,
            text="🎨",
            font=("SimHei", 11),  # 10⇒11
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        theme_label.pack(side='left', padx=5)
        
        # 6个颜色主题按钮
        theme_colors = [
            ('蓝色', '#4A90E2'),
            ('绿色', '#27AE60'),
            ('紫色', '#8E44AD'),
            ('粉色', '#E91E63'),
            ('橙色', '#FF5722'),
            ('灰色', '#607D8B')
        ]
        
        for theme_name, color in theme_colors:
            btn = tk.Button(
                theme_frame,
                text=theme_name,
                command=lambda t=theme_name: self.change_theme(t),
                width=5,
                font=("SimHei", 9),  # 8⇒9
                bg=color,
                fg='white',
                relief='flat',
                cursor='hand2',
                activebackground=color
            )
            btn.pack(side='left', padx=3)
    
    def create_sync_status(self, parent):
        """创建同步状态区"""
        self.sync_frame = tk.LabelFrame(
            parent,
            text="⏱ 同步",
            font=("SimHei", 10),  # 9⇒10
            bg=self.colors['background'],
            padx=10,
            pady=5
        )
        self.sync_frame.pack(fill='x', pady=6)
        
        # 同步状态和按钮放在同一行
        sync_container = tk.Frame(self.sync_frame, bg=self.colors['background'])
        sync_container.pack(fill='x')
        
        self.sync_label = tk.Label(
            sync_container,
            text="检测中...",
            font=("SimHei", 9),  # 8⇒9
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        self.sync_label.pack(side='left', padx=5)
        
        self.sync_btn = tk.Button(
            sync_container,
            text="立即同步",
            command=self.manual_sync,
            font=("SimHei", 9),  # 8⇒9
            bg=self.colors['accent'],
            fg='white',
            relief='flat',
            cursor='hand2',
            width=8
        )
        self.sync_btn.pack(side='right', padx=5)
    
    def start_timer(self):
        """启动定时器"""
        if self.timer.start():
            self.play_click_sound()  # 播放点击音
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
            self.update_running = True
            self.update_timer_display()
    
    def pause_timer(self):
        """暂停定时器"""
        if self.timer.pause():
            self.play_pause_sound()  # 播放clic声
            self.start_btn.config(text="▶ 继续", state='normal', command=self.resume_timer)
            self.pause_btn.config(state='disabled')
            self.update_running = False
    
    def resume_timer(self):
        """继续定时器"""
        if self.timer.resume():
            self.play_click_sound()  # 播放点击音
            self.start_btn.config(state='disabled')
            self.pause_btn.config(state='normal')
            self.update_running = True
            self.update_timer_display()
    
    def reset_timer(self):
        """重置定时器"""
        self.play_reset_sound()  # 播放3音节低到高和弦
        self.update_running = False
        self.timer.reset()
        self.update_time_display()
        self.start_btn.config(text="▶ 开始", state='normal', command=self.start_timer)
        self.pause_btn.config(state='disabled')
    
    def increase_duration(self):
        """增加时长（上限40分钟）"""
        if self.timer.is_running or self.update_running:
            self.show_custom_message("提示", "请先停止计时器再调整时长", "warning")
            return
        
        if self.duration_minutes < 40:
            self.play_click_sound()
            self.duration_minutes += 1
            self.duration_label.config(text=f"{self.duration_minutes} 分钟")
            self.timer = PrecisionTimer(self.duration_minutes * 60)
            self.update_time_display()
        else:
            self.show_custom_message("提示", "已达到最大时长（40分钟）", "info")
    
    def decrease_duration(self):
        """减少时长（下限14分钟）"""
        if self.timer.is_running or self.update_running:
            self.show_custom_message("提示", "请先停止计时器再调整时长", "warning")
            return
        
        if self.duration_minutes > 14:  # 15→14
            self.play_click_sound()
            self.duration_minutes -= 1
            self.duration_label.config(text=f"{self.duration_minutes} 分钟")
            self.timer = PrecisionTimer(self.duration_minutes * 60)
            self.update_time_display()
        else:
            self.show_custom_message("提示", "已达到最小时长（14分钟）", "info")  # 15→14
    
    def update_time_display(self):
        """更新时间显示"""
        minutes = self.duration_minutes
        self.time_label.config(text=f"{minutes:02d}:00")
    
    def update_timer_display(self):
        """更新定时器显示"""
        if self.update_running:
            time_str = self.timer.format_time()
            self.time_label.config(text=time_str)
            
            if self.timer.is_finished():
                self.update_running = False
                self.play_complete_sound()  # 播放完成音效
                self.show_custom_message("完成", "🎉 专注时段完成！", "info")
                self.reset_timer()
            else:
                self.master.after(100, self.update_timer_display)
    
    def show_custom_message(self, title, message, msg_type="info"):
        """显示自定义大字体消息框"""
        # 创建自定义对话框
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(self.master)
        dialog.grab_set()
        
        # 设置窗口居中
        dialog.geometry("400x180")
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (180 // 2)
        dialog.geometry(f"400x180+{x}+{y}")
        
        # 设置背景色
        dialog.configure(bg='#F8F9FA')
        
        # 图标和消息区域
        content_frame = tk.Frame(dialog, bg='#F8F9FA')
        content_frame.pack(expand=True, fill='both', padx=30, pady=25)
        
        # 图标
        icon_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌"
        }
        icon = icon_map.get(msg_type, "ℹ️")
        
        icon_label = tk.Label(
            content_frame,
            text=icon,
            font=("Segoe UI Emoji", 32),
            bg='#F8F9FA'
        )
        icon_label.pack(pady=(0, 15))
        
        # 消息文本
        msg_label = tk.Label(
            content_frame,
            text=message,
            font=("SimHei", 14),  # 大字体
            bg='#F8F9FA',
            fg='#333333',
            wraplength=340
        )
        msg_label.pack()
        
        # 按钮区域
        button_frame = tk.Frame(dialog, bg='#F8F9FA')
        button_frame.pack(side='bottom', pady=15)
        
        ok_btn = tk.Button(
            button_frame,
            text="确定",
            command=dialog.destroy,
            width=12,
            height=1,
            font=("SimHei", 11),
            bg='#4A90E2',
            fg='white',
            relief='flat',
            cursor='hand2',
            activebackground='#357ABD'
        )
        ok_btn.pack()
        
        # 绑定Enter键
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        
        # 等待窗口关闭
        dialog.wait_window()
    
    def sync_time_on_start(self):
        """程序启动时同步时间"""
        def sync():
            result = self.timer.sync_time()
            status = self.timer.get_sync_status()
            
            if status['online']:
                if result['success']:
                    self.sync_label.config(
                        text=f"✅ {result['message']}",
                        fg='green'
                    )
                else:
                    self.sync_label.config(
                        text=f"⚠ {result['message']}",
                        fg='orange'
                    )
            else:
                self.sync_label.config(
                    text="🔴 离线模式 - 使用CPU时钟",
                    fg='gray'
                )
        
        threading.Thread(target=sync, daemon=True).start()
    
    def manual_sync(self):
        """手动同步"""
        self.play_click_sound()  # 播放点击音
        self.sync_label.config(text="同步中...", fg='blue')
        self.master.update()
        threading.Thread(target=self.sync_time_on_start, daemon=True).start()
    
    def change_theme(self, theme_name):
        """切换颜色主题"""
        self.play_click_sound()
        self.current_theme = theme_name
        self.colors = self.color_themes[theme_name]
        
        # 更新所有组件颜色
        self.master.configure(bg=self.colors['background'])
        self.title_frame.config(bg=self.colors['primary'])
        self.title_label.config(bg=self.colors['primary'])
        self.header_time_label.config(bg=self.colors['primary'])
        self.author_label.config(bg=self.colors['primary'])
        self.content_frame.config(bg=self.colors['background'])
        self.timer_frame.config(bg=self.colors['background'], fg=self.colors['text'])
        self.time_label.config(bg=self.colors['background'], fg=self.colors['primary'])
        self.duration_label.config(bg=self.colors['background'], fg=self.colors['text'])
        self.start_btn.config(bg=self.colors['primary'])
        self.pause_btn.config(bg=self.colors['secondary'])
        self.sync_frame.config(bg=self.colors['background'])
        self.sync_label.config(bg=self.colors['background'], fg=self.colors['text'])
        self.sync_btn.config(bg=self.colors['accent'])
    
    def update_realtime_clock(self):
        """更新实时时间（标题栏右侧）"""
        if self.realtime_running:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            self.header_time_label.config(text=current_time)
            self.master.after(1000, self.update_realtime_clock)
