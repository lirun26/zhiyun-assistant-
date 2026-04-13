#!/usr/bin/env python3
"""配置加载器"""
import os

def load_config():
    """从 config.env 加载配置"""
    config = {}
    env_path = os.path.join(os.path.dirname(__file__), 'config.env')
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and ':' in line:
                    key, value = line.split(':', 1)
                    config[key.strip()] = value.strip()
    
    return config

if __name__ == '__main__':
    config = load_config()
    print(config)
