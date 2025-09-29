#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试打包脚本
验证打包功能是否正常
"""

import os
import sys
import subprocess
import platform

def test_environment():
    """测试环境"""
    print("=" * 50)
    print("测试打包环境")
    print("=" * 50)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("❌ Python版本过低，需要3.7+")
        return False
    else:
        print("✅ Python版本符合要求")
    
    # 检查系统
    system = platform.system()
    print(f"操作系统: {system}")
    
    # 检查虚拟环境
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 运行在虚拟环境中")
    else:
        print("⚠️  未检测到虚拟环境，建议使用虚拟环境")
        print("   创建虚拟环境: python3 -m venv venv")
        print("   激活虚拟环境: source venv/bin/activate")
    
    return True

def test_dependencies():
    """测试依赖"""
    print("\n" + "=" * 50)
    print("测试项目依赖")
    print("=" * 50)
    
    required_modules = [
        'playwright',
        'yt_dlp', 
        'tqdm',
        'requests',
        'rich'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - 未安装")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n缺少模块: {', '.join(missing_modules)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def test_project_structure():
    """测试项目结构"""
    print("\n" + "=" * 50)
    print("测试项目结构")
    print("=" * 50)
    
    required_files = [
        '../main.py',
        '../requirements.txt',
        '../process/__init__.py',
        '../process/douyin.py',
        '../process/download.py',
        '../process/result.py',
        '../process/utils.py',
        '../process/xiaohongshu_playwright.py',
        '../process/douyin_downloader_playwright_v6.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n缺少文件: {', '.join(missing_files)}")
        return False
    
    return True

def test_build_scripts():
    """测试打包脚本"""
    print("\n" + "=" * 50)
    print("测试打包脚本")
    print("=" * 50)
    
    build_scripts = [
        'build_simple.py',
        'build_standalone.py',
        'build_windows.py',
        'build_macos.py'
    ]
    
    for script in build_scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - 脚本不存在")
    
    return True

def main():
    """主函数"""
    print("Link2Video 打包测试工具")
    print("=" * 50)
    
    tests = [
        ("环境测试", test_environment),
        ("依赖测试", test_dependencies),
        ("项目结构测试", test_project_structure),
        ("打包脚本测试", test_build_scripts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name} 通过")
            else:
                print(f"\n❌ {test_name} 失败")
        except Exception as e:
            print(f"\n❌ {test_name} 出错: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    print("=" * 50)
    
    if passed == total:
        print("🎉 所有测试通过！可以开始打包")
        print("\n推荐使用以下命令打包:")
        print("  python build_simple.py      # 简化版")
        print("  python build_standalone.py  # 完整版")
    else:
        print("⚠️  部分测试失败，请先解决问题再打包")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
