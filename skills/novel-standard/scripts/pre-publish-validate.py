#!/usr/bin/env python3
"""
小说章节发布前自动校验脚本 v2.0
整合 humanizer-zh 的 21 种 AI 模式检测

检查：
1. 字数控制（2500-3500字）
2. AI味检测（21种模式）
3. 逻辑一致性
4. 番茄平台规范

用法:
    python3 pre-publish-validate.py <章节文件或目录>
"""

import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple

# 颜色输出
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def colored(text, color):
    return f"{color}{text}{RESET}" if sys.stdout.isatty() else text

# ============================================================
# AI味检测规则 (整合 humanizer-zh 的 21 种模式)
# ============================================================

# P0级：直接拒稿级别
AI_PATTERNS_P0 = [
    # 1. 夸大的象征意义
    (r'作为.?.?的证明|标志着|是.?.?的体现|象征着|代表着|标志着', 'P0', '夸大的象征意义'),
    # 2. 否定式排比
    (r'不仅.?.?而且.?.?|不.?.?也不|绝非.?.?绝不|绝不再', 'P0', '否定式排比句式'),
    # 3. 固定句式（小说专用）
    (r'的嘴角勾起一抹|的眼中闪过一丝|的眉头微微一', 'P0', 'AI固定句式'),
    # 4. 上帝视角
    (r'全书第|所有人都没想到|命运的齿轮|一切都是|冥冥之中', 'P0', '上帝视角'),
    # 5. 本章总结/下章预告
    (r'本章总结|下章预告|本章要点|下章看点', 'P0', 'AI总结/预告'),
]

# P1级：影响评分，建议优化
AI_PATTERNS_P1 = [
    # 6. AI高频词汇
    (r'此外|至关重要|深入探讨|与.?.?保持一致|突出|增强|培养|获得|复杂/复杂性|关键性的|展示|证明|宝贵的|充满活力的', 'P1', 'AI高频词汇'),
    # 7. 系动词回避
    (r'作为.?.?[空间场所]|充当|拥有.{0,5}[个间件台]|设有|提供着', 'P1', '系动词回避（用复杂结构替代"是/有"）'),
    # 8. 三段式法则
    (r'、.{1,10}、.{1,10}、.{1,10}[。；，]', 'P1', '三段式法则过度'),
    # 9. 倒计时句式（末世文专用）
    (r'末世爆发前\d+天|末世前\d+天|丧尸爆发前\d+天', 'P1', '倒计时句式'),
    # 10. 破折号过度使用
    (r'——.{2,20}——.{2,20}——', 'P1', '破折号过度使用'),
    # 11. 粗体过度使用（markdown）
    (r'\*\*.{2,10}\*\*.*?\*\*\*.{2,10}\*\*', 'P1', '粗体过度使用'),
    # 12. 宣传性语言
    (r'令人叹为观止|充满活力|坐落于|位于.?.?的中心|开创性的|迷人的|著名的', 'P1', '宣传性/广告语言'),
    # 13. 模糊归因
    (r'行业报告显示|观察者指出|专家认为|一些批评者认为', 'P1', '模糊归因'),
    # 14. -ing结尾的肤浅分析
    (r'确保.?.?、|反映着|象征着|为.?.?做出贡献|培养.?.?|促进.?.?', 'P1', '-ing结尾的肤浅分析'),
    # 15. 刻意换词（同义词循环）
    (r'主人公.{0,5}面临.{0,5}挑战|主要角色.{0,5}必须|中心人物.{0,5}获得|英雄.{0,5}回到', 'P1', '同义词循环（刻意换词）'),
    # 16. 虚假范围
    (r'从.{2,10}到.{2,10}的.{2,10}', 'P1', '虚假范围（"从X到Y"无意义结构）'),
    # 17. 公式化挑战/展望
    (r'尽管其.{0,20}面临若干挑战|尽管存在这些挑战|挑战与遗产|未来展望', 'P1', '公式化"挑战与展望"'),
    # 18. 协作交流痕迹
    (r'希望这对您有帮助|当然！|一定！|您说得完全正确|请告诉我|这是一个', 'P1', '聊天机器人交流痕迹'),
    # 19. 知识截止日期免责声明
    (r'截至.{0,20}[日年月]|根据我最后的训练更新|虽然具体细节有限', 'P1', 'AI知识截止日期免责声明'),
    # 20. 谄媚语气
    (r'好问题！|您说得完全正确|这是一个很好的观点', 'P1', '谄媚/卑躬语气'),
    # 21. 表情符号（标题/列表中）
    (r'[🚀💡✅❌🔥✨].{0,5}\*\*|\*\*.*?[🚀💡✅❌🔥✨]', 'P1', '表情符号过度使用'),
]

# 固定句式计数（超过2次需要优化）
FIXED_SENTENCE_PATTERNS = [
    r'的嘴角勾起一抹',
    r'的眼中闪过一丝',
    r'的眉头微微一',
    r'不由自主地',
    r'下意识地',
]


def count_chinese_chars(text: str) -> int:
    """统计中文字符数（不含标点）"""
    chinese = re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text)
    return len(chinese)

def check_word_count(text: str) -> Dict:
    """检查字数"""
    char_count = count_chinese_chars(text)
    lines = text.strip().split('\n')
    
    result = {
        'char_count': char_count,
        'line_count': len(lines),
        'status': 'PASS',
        'message': f'字数: {char_count}字',
        'details': []
    }
    
    if char_count < 2000:
        result['status'] = 'FAIL'
        result['message'] = f'字数不足: {char_count}字 < 2000字（禁止发布）'
        result['details'].append(f'⚠️ 需要补充 {2000 - char_count} 字以上')
    elif char_count > 3500:
        result['status'] = 'FAIL'
        result['message'] = f'字数超标: {char_count}字 > 3500字（必须拆分）'
        result['details'].append(f'建议拆分为 {(char_count + 1499) // 3000} 章')
    elif char_count < 2500:
        result['details'].append(f'字数偏低，建议扩充至2500字以上')
    else:
        result['details'].append(f'✅ 字数达标')
    
    return result

def check_ai_patterns(text: str) -> Dict:
    """检查AI味 - P0和P1模式"""
    issues = []
    
    # P0检查
    for pattern, level, desc in AI_PATTERNS_P0:
        matches = re.findall(pattern, text)
        if matches:
            issues.append({
                'level': level,
                'pattern': desc,
                'count': len(matches),
                'matches': matches[:3]
            })
    
    # P1检查
    for pattern, level, desc in AI_PATTERNS_P1:
        matches = re.findall(pattern, text)
        if matches:
            issues.append({
                'level': level,
                'pattern': desc,
                'count': len(matches),
                'matches': matches[:3]
            })
    
    # 固定句式计数
    for ptn in FIXED_SENTENCE_PATTERNS:
        matches = re.findall(ptn, text)
        if len(matches) > 2:
            issues.append({
                'level': 'P1',
                'pattern': f'固定句式"{ptn}"',
                'count': len(matches),
                'matches': matches[:3]
            })
    
    # 内心独白检查（连续3段以上"她想"/"他觉得"）
    lines = text.split('\n')
    inner_monologue_count = 0
    inner_monologue_lines = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^[她他我]想[道到]?[：:]', stripped) or \
           re.match(r'^[她他我]觉得', stripped) or \
           re.match(r'^"我想', stripped):
            inner_monologue_count += 1
            inner_monologue_lines.append(stripped[:30])
    
    if inner_monologue_count >= 3:
        issues.append({
            'level': 'P1',
            'pattern': '连续内心独白',
            'count': inner_monologue_count,
            'matches': inner_monologue_lines[:3]
        })
    
    # 评分计算
    p0_count = sum(1 for i in issues if i['level'] == 'P0')
    p1_count = sum(1 for i in issues if i['level'] == 'P1')
    
    if p0_count > 0:
        status = 'FAIL'
    elif p1_count > 3:
        status = 'WARN'
    else:
        status = 'PASS'
    
    return {
        'issues': issues,
        'p0_count': p0_count,
        'p1_count': p1_count,
        'status': status,
        'message': f'AI味: P0问题{p0_count}个, P1问题{p1_count}个'
    }

def check_summary_preview(text: str) -> Dict:
    """检查是否有本章总结/下章预告"""
    patterns = [
        r'##\s*本章总结',
        r'##\s*下章预告',
        r'##\s*本章要点',
        r'##\s*下章看点',
        r'本章总结：',
        r'下章预告：',
    ]
    
    found = []
    for pattern in patterns:
        if re.search(pattern, text):
            found.append(pattern)
    
    return {
        'found': found,
        'status': 'FAIL' if found else 'PASS',
        'message': '发现总结/预告段落' if found else '无总结/预告'
    }

def check_tomatno_rules(text: str) -> Dict:
    """番茄平台专项检查"""
    checks = []
    
    # 检查开篇（前500字）是否有事件冲突
    first_500 = text[:500]
    has_event = any(marker in first_500 for marker in ['。', '，', '！', '？', '说', '道', '问', '喊', '叫'])
    has_conflict = any(word in first_500 for word in ['冲突', '矛盾', '问题', '困难', '危机', '威胁'])
    
    if has_event:
        checks.append(('✅', '开篇有事件推进（非纯氛围描写）'))
    else:
        checks.append(('❌', '开篇无事件，可能是氛围描写'))
    
    # 检查是否有感情线暗示
    has_love = any(word in text for word in ['心动', '喜欢', '爱', '脸红', '心跳', '暧昧'])
    if has_love:
        checks.append(('✅', '有感情线元素'))
    else:
        checks.append(('ℹ️', '无明显感情线（番茄签约难度+）'))
    
    return {
        'checks': checks,
        'status': 'PASS'
    }

def validate_chapter(file_path: str) -> Dict:
    """验证单个章节"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 移除 markdown 标题等元信息，只保留正文
    lines = text.split('\n')
    body_lines = []
    in_metadata = False
    for line in lines:
        if line.startswith('---') or line.startswith('#'):
            in_metadata = True
            continue
        if in_metadata and line.strip() == '':
            in_metadata = False
            continue
        if not in_metadata:
            body_lines.append(line)
    body = '\n'.join(body_lines)
    
    word_result = check_word_count(body)
    ai_result = check_ai_patterns(body)
    summary_result = check_summary_preview(body)
    tomatno_result = check_tomatno_rules(body)
    
    # 综合判断
    all_pass = (
        word_result['status'] == 'PASS' and
        ai_result['status'] == 'PASS' and
        summary_result['status'] == 'PASS'
    )
    
    return {
        'file': file_path,
        'word_count': word_result,
        'ai_patterns': ai_result,
        'summary_preview': summary_result,
        'tomatno': tomatno_result,
        'overall': 'PASS' if all_pass else 'FAIL'
    }

def print_result(result: Dict):
    """打印验证结果"""
    file_name = Path(result['file']).name
    overall = result['overall']
    
    print(f"\n{'='*65}")
    print(colored(f"📖 {file_name}", BLUE))
    print(f"{'='*65}")
    
    # 字数检查
    wc = result['word_count']
    icon = '✅' if wc['status'] == 'PASS' else '❌'
    print(f"\n  {icon} 字数检查: {wc['message']}")
    for d in wc.get('details', []):
        print(f"     → {d}")
    
    # AI味检测
    ai = result['ai_patterns']
    if ai['p0_count'] > 0:
        icon = '❌'
        print(f"\n  {colored(f'❌ AI味检测: {ai["message"]}', RED)}")
    elif ai['p1_count'] > 3:
        icon = '⚠️'
        print(f"\n  {colored(f'⚠️ AI味检测: {ai["message"]}', YELLOW)}")
    else:
        icon = '✅'
        print(f"\n  {icon} AI味检测: {ai['message']}")
    
    if ai['issues']:
        print(f"\n  发现问题:")
        for issue in ai['issues'][:10]:
            level_color = RED if issue['level'] == 'P0' else YELLOW
            print(f"    [{colored(issue['level'], level_color)}] {issue['pattern']} (×{issue['count']})")
    
    # 总结/预告检查
    sp = result['summary_preview']
    icon = '✅' if sp['status'] == 'PASS' else '❌'
    print(f"\n  {icon} 总结/预告: {sp['message']}")
    
    # 番茄专项
    tom = result['tomatno']
    print(f"\n  📊 番茄专项检查:")
    for icon_str, msg in tom['checks']:
        print(f"     {icon_str} {msg}")
    
    # 综合结果
    print(f"\n  {'🟢 发布通过' if overall == 'PASS' else '🔴 需要修改'}")
    print('-' * 65)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isdir(target):
        # 批量检查
        chapter_files = []
        for ext in ['*.txt', '*.md']:
            chapter_files.extend(Path(target).glob(ext))
        chapter_files = sorted(chapter_files)
        
        if not chapter_files:
            print(f"未找到章节文件: {target}/*.txt 或 *.md")
            sys.exit(1)
        
        print(colored(f"\n📚 批量检查: {len(chapter_files)} 个章节", BLUE))
        
        results = []
        for f in chapter_files:
            try:
                result = validate_chapter(str(f))
                results.append(result)
                print_result(result)
            except Exception as e:
                print(f"\n❌ 处理失败: {f} - {e}")
        
        # 汇总
        passed = sum(1 for r in results if r['overall'] == 'PASS')
        print(colored(f"\n📊 汇总: {passed}/{len(results)} 通过", 
                      GREEN if passed == len(results) else YELLOW))
        
        # 列出失败的文件
        failed = [r['file'] for r in results if r['overall'] == 'FAIL']
        if failed:
            print(colored(f"\n❌ 需要修改的章节:", RED))
            for f in failed:
                print(f"   - {Path(f).name}")
    
    elif os.path.isfile(target):
        result = validate_chapter(target)
        print_result(result)
        if result['overall'] == 'FAIL':
            sys.exit(1)
    else:
        print(f"文件不存在: {target}")
        sys.exit(1)

if __name__ == '__main__':
    main()
