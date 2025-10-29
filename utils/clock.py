"""高精度时钟模块
使用CPU性能计数器实现微秒级精度计时
"""

import time
from datetime import datetime, timedelta

class HighPrecisionClock:
    """高精度时钟类"""
    
    def __init__(self):
        """初始化时钟"""
        self.start_time = time.perf_counter()  # CPU时钟起始点
        self.offset = 0  # 时间偏移量（NTP校正用）
        self.last_sync = None  # 上次同步时间
    
    def get_precise_time(self):
        """
        获取高精度当前时间（秒）
        返回: float, 精确到微秒的时间戳
        """
        return time.perf_counter() - self.start_time + self.offset
    
    def elapsed(self, from_time):
        """
        计算从指定时间点经过的时长
        参数: from_time - 起始时间点
        返回: float, 经过的秒数
        """
        current = self.get_precise_time()
        return current - from_time
    
    def format_elapsed(self, seconds):
        """
        格式化时间显示
        参数: seconds - 秒数
        返回: str, 格式化字符串 "HH:MM:SS.mmm"
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
    
    def sync_offset(self, true_time):
        """
        同步时间偏移（NTP校正）
        参数: true_time - NTP获取的真实时间戳
        """
        current_clock = time.perf_counter() - self.start_time
        self.offset = true_time - current_clock
        self.last_sync = datetime.now()
    
    def get_sync_status(self):
        """
        获取同步状态
        返回: dict, 包含同步信息
        """
        if self.last_sync is None:
            return {
                'synced': False,
                'message': '未同步',
                'time_since_sync': None
            }
        
        time_since = datetime.now() - self.last_sync
        return {
            'synced': True,
            'message': f'{int(time_since.total_seconds() / 60)}分钟前同步',
            'time_since_sync': time_since.total_seconds()
        }

# 全局时钟实例
_global_clock = HighPrecisionClock()

def get_clock():
    """获取全局时钟实例"""
    return _global_clock
