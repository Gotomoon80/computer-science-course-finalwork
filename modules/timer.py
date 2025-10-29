"""
集成高精度时钟和网络授时的定时器
"""

import time
from utils.clock import get_clock
from utils.time_sync import TimeSync

class PrecisionTimer:
    """精准定时器类"""
    
    def __init__(self, duration_seconds):
        """
        初始化定时器
        参数: duration_seconds - 倒计时时长（秒）
        """
        self.duration = duration_seconds
        self.remaining = duration_seconds
        self.is_running = False
        self.is_paused = False
        
        # 使用全局高精度时钟
        self.clock = get_clock()
        self.start_mark = None  # 开始时刻
        self.pause_mark = None  # 暂停时刻
        
        # 时间同步
        self.time_sync = TimeSync(self.clock)
    
    def start(self):
        """启动定时器"""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.start_mark = self.clock.get_precise_time()
            return True
        return False
    
    def pause(self):
        """暂停定时器"""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_mark = self.clock.get_precise_time()
            
            # 计算已用时间
            elapsed = self.pause_mark - self.start_mark
            self.remaining = max(0, self.duration - elapsed)
            return True
        return False
    
    def resume(self):
        """继续定时器"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            # 重新设置起点
            self.duration = self.remaining
            self.start_mark = self.clock.get_precise_time()
            return True
        return False
    
    def reset(self):
        """重置定时器"""
        self.is_running = False
        self.is_paused = False
        self.remaining = self.duration
        self.start_mark = None
        self.pause_mark = None
        return True
    
    def get_remaining(self):
        """
        获取剩余时间（秒）
        返回: float, 精确到毫秒
        """
        if not self.is_running:
            return self.remaining
        
        if self.is_paused:
            return self.remaining
        
        # 计算剩余时间
        current = self.clock.get_precise_time()
        elapsed = current - self.start_mark
        remaining = self.duration - elapsed
        
        return max(0, remaining)
    
    def is_finished(self):
        """是否已完成"""
        return self.get_remaining() <= 0
    
    def format_time(self, include_milliseconds=False):
        """
        格式化时间显示
        参数: include_milliseconds - 是否显示毫秒
        返回: str
        """
        seconds = self.get_remaining()
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if include_milliseconds:
            millisecs = int((seconds % 1) * 1000)
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def sync_time(self):
        """
        同步网络时间
        返回: dict, 同步结果
        """
        return self.time_sync.try_sync()
    
    def get_sync_status(self):
        """获取同步状态"""
        return self.time_sync.get_status()
