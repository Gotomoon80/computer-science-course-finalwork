"""
打包脚本 - 生成.exe可执行文件
使用PyInstaller将Python项目打包成单个可执行文件
"""
import os
import shutil
import subprocess
import sys

def clean_build():
    """清理之前的打包文件"""
    print("🧹 清理旧的打包文件...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   ✓ 删除 {dir_name}")
    
    # 删除.spec文件
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)
            print(f"   ✓ 删除 {file}")

def build_exe():
    """使用PyInstaller打包"""
    print("\n📦 开始打包...")
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个exe
        '--windowed',                   # 无控制台窗口
        '--name=张弛有度',               # exe文件名
        '--icon=NONE',                  # 暂不添加图标
        '--clean',                      # 清理临时文件
        '--noconfirm',                  # 不询问确认
        
        # 排除不需要的模块（减小体积）
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=PIL',
        '--exclude-module=cv2',
        
        # 添加数据文件（如果有）
        # '--add-data=assets;assets',
        
        # 主程序入口
        'main.py'
    ]
    
    print(f"   执行命令: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        print(e.stderr)
        return False

def check_result():
    """检查打包结果"""
    print("\n📊 检查打包结果...")
    
    exe_path = os.path.join('dist', '张弛有度.exe')
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"   ✅ 打包成功！")
        print(f"   📁 文件位置: {os.path.abspath(exe_path)}")
        print(f"   📏 文件大小: {size_mb:.2f} MB")
        
        if size_mb > 32:
            print(f"   ⚠️  警告: 文件大小超过32MB目标")
        elif size_mb <= 8:
            print(f"   🎯 优秀: 达到8MB以内优化目标！")
        else:
            print(f"   ✓  良好: 文件大小在合理范围内")
        
        return True
    else:
        print(f"   ❌ 未找到exe文件")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("   张弛有度 v1.0 - 打包工具")
    print("=" * 60)
    
    # 确认当前目录
    if not os.path.exists('main.py'):
        print("❌ 错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 步骤1: 清理
    clean_build()
    
    # 步骤2: 打包
    if not build_exe():
        print("\n❌ 打包失败，请检查错误信息")
        sys.exit(1)
    
    # 步骤3: 验证
    if check_result():
        print("\n" + "=" * 60)
        print("   🎉 打包完成！")
        print("   💡 提示: 可执行文件在 dist 文件夹中")
        print("   🚀 双击运行: dist\\张弛有度.exe")
        print("=" * 60)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
