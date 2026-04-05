#!/usr/bin/env python3
import sys
import json
import traceback
from datetime import datetime

class ErrorCatcher:
    def __init__(self, log_file='/tmp/errors.jsonl'):
        self.log_file = log_file
    
    def capture(self, error, context=None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        return entry

if __name__ == '__main__':
    catcher = ErrorCatcher()
    try:
        import non_existent_module
    except Exception as e:
        entry = catcher.capture(e)
        print(f"✅ Error captured:")
        print(f"   Type: {entry['error_type']}")
        print(f"   Message: {entry['error_message']}")
        print(f"   Log: {entry['timestamp']}")
