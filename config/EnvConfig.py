import os

# 环境变量
env_config = {
    # 是否是本地调试模式，0为本地调试模式
    "DEBUG_MODE": os.environ.get("DEBUG_MODE", '1')
}