#!/usr/bin/env python3
import subprocess
import json
import sys

class AutoFixer:
    def apply_fix(self, fix_type, details=None):
        fixes = {
            'install_dependency': self._install_dep,
            'restart_service': self._restart_service,
            'clear_cache': self._clear_cache,
        }
        if fix_type in fixes:
            return fixes[fix_type](details or {})
        return {'success': False, 'error': 'Unknown fix type'}
    
    def _install_dep(self, details):
        pkg = details.get('package')
        if pkg:
            r = subprocess.run(['pip3', 'install', '--break-system-packages', pkg], capture_output=True, text=True)
            return {'success': r.returncode == 0, 'message': f'Installed {pkg}'}
        return {'success': False}
    
    def _restart_service(self, details):
        subprocess.run(['openclaw', 'gateway', 'restart'])
        return {'success': True, 'message': 'Service restarted'}
    
    def _clear_cache(self, details):
        subprocess.run(['rm', '-rf', '/tmp/errors.jsonl'], capture_output=True)
        return {'success': True, 'message': 'Cache cleared'}

if __name__ == '__main__':
    fixer = AutoFixer()
    data = json.load(sys.stdin)
    result = fixer.apply_fix(data['type'], data.get('details', {}))
    print(json.dumps(result))
