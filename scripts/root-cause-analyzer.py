#!/usr/bin/env python3
import json
import sys

ERROR_PATTERNS = {
    'FileNotFoundError': {'cause': '文件路径错误或文件不存在', 'fix': '检查文件路径'},
    'PermissionError': {'cause': '权限不足', 'fix': '检查文件权限'},
    'TimeoutError': {'cause': '操作超时', 'fix': '增加超时时间'},
    'ConnectionError': {'cause': '网络连接失败', 'fix': '检查网络连接'},
    'MemoryError': {'cause': '内存不足', 'fix': '减少数据量'},
    'ModuleNotFoundError': {'cause': '缺少依赖包', 'fix': 'pip install <package>'},
    'JSONDecodeError': {'cause': 'JSON格式错误', 'fix': '检查JSON语法'},
}

def analyze(error_type, error_msg=''):
    if error_type in ERROR_PATTERNS:
        p = ERROR_PATTERNS[error_type]
        return {'root_cause': p['cause'], 'suggested_fix': p['fix'], 'confidence': 0.9}
    return {'root_cause': '未知错误', 'suggested_fix': '查看详细日志', 'confidence': 0.3}

if __name__ == '__main__':
    err_type = sys.argv[1] if len(sys.argv) > 1 else 'UnknownError'
    err_msg = sys.argv[2] if len(sys.argv) > 2 else ''
    result = analyze(err_type, err_msg)
    print(json.dumps(result, indent=2, ensure_ascii=False))
