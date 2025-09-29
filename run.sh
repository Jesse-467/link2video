#!/bin/bash
# 启动脚本 - 自动激活虚拟环境并运行程序

cd "$(dirname "$0")"
source venv/bin/activate

if [ $# -eq 0 ]; then
    echo "用法: ./run.sh <视频链接>"
    echo "示例: ./run.sh 'https://v.douyin.com/xxxxx/'"
    exit 1
fi

python main.py "$1"
