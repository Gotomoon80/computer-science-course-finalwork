"""
网络授时模块
实现NTP时间同步和离线降级策略
"""

import ntplib
import socket
import time
from datetime import datetime
import threading

class TimeSync:
    """时间同步管理类"""
    
    # NTP服务器列表（按优先级排序）
    NTP_SERVERS = [
        'ntp.ntsc.ac.cn',        # 中国科学院国家授时中心（首选）
        'ntp1.ntsc.ac.cn',       # 国家授时中心备用1
        'ntp2.ntsc.ac.cn',       # 国家授时中心备用2
        'cn.ntp.org.cn',         # 中国NTP服务器
        'ntp.aliyun.com',        # 阿里云NTP
        'time.windows.com'       # Windows时间服务器（兜底）
    ]
    
    def __init__(self, clock):
        """
        初始化时间同步
        参数: clock - HighPrecisionClock实例
        """
        self.clock = clock
        self.is_online_cache = None  # 网络状态缓存
        self.last_check_time = 0  # 上次检查网络时间
        self.sync_thread = None  # 同步线程
        self.auto_sync_enabled = False  # 自动同步开关
    
    def is_online(self, timeout=2):
        """
        检测网络连接状态
        参数: timeout - 超时时间（秒）
        返回: bool
        """
        # 缓存机制：30秒内不重复检查
        current_time = time.time()
        if self.is_online_cache is not None and \
           current_time - self.last_check_time < 30:
            return self.is_online_cache
        
        try:
            # 尝试连接Google DNS
            socket.create_connection(('8.8.8.8', 53), timeout=timeout)
            self.is_online_cache = True
            self.last_check_time = current_time
            return True
        except OSError:
            self.is_online_cache = False
            self.last_check_time = current_time
            return False
    
    def sync_from_ntp(self, server=None, timeout=3):
        """
        从NTP服务器同步时间
        参数: 
            server - 服务器地址（None则自动选择）
            timeout - 超时时间
        返回: dict, 同步结果
        """
        client = ntplib.NTPClient()
        
        servers = [server] if server else self.NTP_SERVERS
        
        for ntp_server in servers:
            try:
                print(f"尝试连接NTP服务器: {ntp_server}")
                response = client.request(ntp_server, version=3, timeout=timeout)
                
                # 获取NTP时间戳
                ntp_time = response.tx_time
                
                # 同步到高精度时钟
                self.clock.sync_offset(ntp_time)
                
                return {
                    'success': True,
                    'server': ntp_server,
                    'offset': response.offset,  # 时间偏移
                    'delay': response.delay,    # 网络延迟
                    'message': f'成功同步自 {ntp_server}'
                }
                
            except Exception as e:
                print(f"同步失败 ({ntp_server}): {e}")
                continue
        
        # 所有服务器都失败
        return {
            'success': False,
            'server': None,
            'message': '所有NTP服务器同步失败，使用本地时间'
        }
    
    def try_sync(self):
        """
        尝试同步时间（智能策略）
        返回: dict, 同步结果
        """
        # 1. 检查网络连接
        if not self.is_online():
            return {
                'success': False,
                'mode': 'offline',
                'message': '离线模式 - 使用系统时间'
            }
        
        # 2. 尝试NTP同步
        result = self.sync_from_ntp()
        
        if result['success']:
            result['mode'] = 'ntp'
            return result
        else:
            # 3. NTP失败，降级到系统时间
            system_time = time.time()
            self.clock.sync_offset(system_time)
            
            return {
                'success': True,
                'mode': 'system',
                'message': 'NTP失败，使用系统时间'
            }
    
    def auto_sync(self, interval=3600):
        """
        启动自动同步（后台线程）
        参数: interval - 同步间隔（秒），默认1小时
        """
        if self.auto_sync_enabled:
            print("自动同步已在运行")
            return
        
        self.auto_sync_enabled = True
        
        def sync_loop():
            while self.auto_sync_enabled:
                result = self.try_sync()
                print(f"[自动同步] {result['message']}")
                
                # 等待下次同步
                for _ in range(interval):
                    if not self.auto_sync_enabled:
                        break
                    time.sleep(1)
        
        self.sync_thread = threading.Thread(target=sync_loop, daemon=True)
        self.sync_thread.start()
        print(f"自动同步已启动，间隔{interval}秒")
    
    def stop_auto_sync(self):
        """停止自动同步"""
        self.auto_sync_enabled = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        print("自动同步已停止")
    
    def get_status(self):
        """
        获取当前状态
        返回: dict, 状态信息
        """
        online = self.is_online()
        sync_info = self.clock.get_sync_status()
        
        return {
            'online': online,
            'synced': sync_info['synced'],
            'last_sync': sync_info['message'],
            'mode': 'NTP' if sync_info['synced'] else '系统时间'
        }
