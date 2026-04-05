#!/usr/bin/env python3
"""
每日自我复盘脚本 v2 - 整合进化引擎
分析对话记录，评估质量，生成优化提案，对接进化系统
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SKILL_PATH = f"{WORKSPACE}/skills/self-review/SKILL.md"
EVOLUTION_DIR = f"{WORKSPACE}/memory/evolution"
LOGS_DIR = f"{WORKSPACE}/skills/self-review/logs"
LEARNINGS_DIR = f"{WORKSPACE}/.learnings"

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def run_ai_evolution_assess():
    """运行 AI Evolution Engine 评估"""
    print("\n🧬 运行 AI Evolution Engine 评估...")
    assess_script = f"{WORKSPACE}/skills/ai-evolution-engine-v2/scripts/assess.mjs"
    if os.path.exists(assess_script):
        os.system(f"cd {WORKSPACE}/skills/ai-evolution-engine-v2 && node scripts/assess.mjs > {LOGS_DIR}/assess.log 2>&1")
        with open(f"{LOGS_DIR}/assess.log", 'r') as f:
            print(f.read())
    else:
        print("⚠️ ai-evolution-engine-v2 未安装")

def run_ai_evolution_evolve():
    """运行 AI Evolution Engine 进化"""
    print("\n🚀 运行 AI Evolution Engine 进化...")
    evolve_script = f"{WORKSPACE}/skills/ai-evolution-engine-v2/scripts/evolve.mjs"
    if os.path.exists(evolve_script):
        os.system(f"cd {WORKSPACE}/skills/ai-evolution-engine-v2 && node scripts/evolve.mjs > {LOGS_DIR}/evolve.log 2>&1")
        with open(f"{LOGS_DIR}/evolve.log", 'r') as f:
            print(f.read())
    else:
        print("⚠️ ai-evolution-engine-v2 未安装")

def run_evolution_state_analyzer():
    """运行 Evolution State Analyzer - 检测进化停滞"""
    print("\n📊 运行 Evolution State Analyzer...")
    analyzer_script = f"{WORKSPACE}/skills/evolution-state-analyzer/index.js"
    if os.path.exists(analyzer_script):
        import subprocess
        result = subprocess.run(
            ["node", analyzer_script],
            capture_output=True, text=True,
            cwd=WORKSPACE
        )
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                stagnation = data.get('stagnation_detected', False)
                success_rate = data.get('overall_success_rate', 0)
                print(f"   进化周期: {data.get('total_cycles', 0)}")
                print(f"   成功率: {success_rate*100:.0f}%")
                print(f"   停滞检测: {'⚠️ 是' if stagnation else '✅ 否'}")
                if data.get('recommendations'):
                    print(f"   建议: {data['recommendations'][0]}")
                return data
            except:
                print(result.stdout[:500])
        if result.stderr:
            print(f"   错误: {result.stderr[:200]}")
    else:
        print("⚠️ evolution-state-analyzer 未安装")
    return None

def run_evolution_drift_detector():
    """运行 Evolution Drift Detector - 检测技能漂移"""
    print("\n🔍 运行 Evolution Drift Detector...")
    detector_file = f"{WORKSPACE}/skills/evolution-drift-detector/SKILL.md"
    if os.path.exists(detector_file):
        print("   技能漂移检测已就绪（需要人工审核）")
        print(f"   位置: {detector_file}")
        # 可以扩展为自动检测 skill 文件变化
    else:
        print("⚠️ evolution-drift-detector 未安装")
    return None

def run_memory_pruner():
    """运行 Memory Pruner - 记忆断舍离"""
    print("\n🧹 运行 Memory Pruner...")
    pruner_script = f"{WORKSPACE}/skills/memory-pruner/analyze.mjs"
    if os.path.exists(pruner_script):
        import subprocess
        result = subprocess.run(
            ["node", pruner_script],
            capture_output=True, text=True,
            cwd=WORKSPACE
        )
        if result.stdout:
            # 只显示关键行
            lines = result.stdout.split('\n')
            for line in lines:
                if any(x in line for x in ['KEEP', 'DISCARD', 'ARCHIVE', '建议', '记忆统计']):
                    print(f"   {line.strip()}")
    else:
        print("⚠️ memory-pruner 未安装")

def get_conversation_count():
    """获取今日对话数"""
    sessions_dir = os.path.expanduser("~/.openclaw/sessions")
    count = 0
    if os.path.exists(sessions_dir):
        for f in os.listdir(sessions_dir):
            if f.endswith('.json'):
                count += 1
    return count

def analyze_errors():
    """分析错误记录"""
    errors_file = f"{LEARNINGS_DIR}/ERRORS.md"
    if os.path.exists(errors_file):
        with open(errors_file, 'r') as f:
            content = f.read()
            # 简单统计错误数量
            error_count = content.count('- **')
            return error_count
    return 0

def analyze_learnings():
    """分析学习记录"""
    learnings_file = f"{LEARNINGS_DIR}/LEARNINGS.md"
    count = 0
    if os.path.exists(learnings_file):
        with open(learnings_file, 'r') as f:
            content = f.read()
            count = content.count('- **')
    return count

def get_quality_score():
    """计算质量评分"""
    # 基础分
    score = 75
    
    # 对话越多，分数可能越高（说明越活跃）
    conv_count = get_conversation_count()
    if conv_count > 20:
        score += 5
    elif conv_count > 10:
        score += 3
    
    # 有学习记录，加分
    learnings_count = analyze_learnings()
    if learnings_count > 0:
        score += learnings_count * 2
    
    # 有错误记录，减分
    error_count = analyze_errors()
    if error_count > 5:
        score -= 10
    elif error_count > 0:
        score -= error_count * 2
    
    # 限制范围
    return max(50, min(100, score))

def generate_improvements():
    """生成改进建议"""
    improvements = []
    
    # 基于质量评分
    score = get_quality_score()
    if score < 80:
        improvements.append({
            "type": "optimization",
            "target": "回答质量",
            "issue": f"质量评分偏低 ({score}/100)",
            "proposal": "增加回答的具体性和实用性"
        })
    
    # 基于错误分析
    error_count = analyze_errors()
    if error_count > 0:
        improvements.append({
            "type": "fix",
            "target": "错误处理",
            "issue": f"历史错误 {error_count} 个未解决",
            "proposal": "检查错误日志，修复常见问题"
        })
    
    # 基于对话数量
    conv_count = get_conversation_count()
    if conv_count < 5:
        improvements.append({
            "type": "optimization",
            "target": "活跃度",
            "issue": "对话数量偏少",
            "proposal": "增加与老大的互动频率"
        })
    
    # 通用建议
    improvements.extend([
        {
            "type": "optimization",
            "target": "记忆更新",
            "issue": "有时候没有主动检查记忆",
            "proposal": "收到重要信息后立即更新 memory 文件"
        },
        {
            "type": "learning",
            "target": "技能扩展",
            "issue": "部分任务缺少合适工具",
            "proposal": "定期扫描 ClawHub 新技能"
        }
    ])
    
    return improvements

def log_learning(lesson: str, priority: str = "medium"):
    """记录学到的东西"""
    learnings_file = f"{LEARNINGS_DIR}/LEARNINGS.md"
    today = get_today()
    
    entry = f"""
- **{today}** [{priority.upper()}] {lesson}"""
    
    with open(learnings_file, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    print(f"📝 记录学习: {lesson}")

def log_error(error: str, context: str = ""):
    """记录错误"""
    errors_file = f"{LEARNINGS_DIR}/ERRORS.md"
    today = get_today()
    
    entry = f"""
- **{today}** {error}
  - Context: {context if context else 'Unknown'}"""
    
    with open(errors_file, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    print(f"❌ 记录错误: {error}")

def save_evolution_log(date, analysis, improvements):
    """保存进化日志"""
    os.makedirs(EVOLUTION_DIR, exist_ok=True)
    
    log_file = f"{EVOLUTION_DIR}/{date}.md"
    
    content = f"""# 进化日志 {date}

## 📊 分析结果

- 对话数量: {get_conversation_count()}
- 质量评分: {analysis['quality_score']}/100
- 错误记录: {analyze_errors()} 个
- 学习记录: {analyze_learnings()} 条

## 🔍 改进建议

"""
    for i, imp in enumerate(improvements, 1):
        content += f"""
### {i}. [{imp['type']}] {imp['target']}
- 问题: {imp['issue']}
- 方案: {imp['proposal']}
"""

    # 添加 Evolution Engine 输出
    assess_log = f"{LOGS_DIR}/assess.log"
    if os.path.exists(assess_log):
        content += "\n## 🧬 Evolution Engine 评估\n\n"
        with open(assess_log, 'r') as f:
            content += f.read()

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 进化日志已保存: {log_file}")
    return log_file

def run_self_review():
    """执行完整自我复盘"""
    today = get_today()
    print(f"\n{'='*60}")
    print(f"🧠 每日自我复盘 v2 - {today}")
    print(f"{'='*60}\n")
    
    # 1. 运行 Evolution Engine 评估
    run_ai_evolution_assess()
    
    # 2. 分析数据
    print("\n📊 分析数据...")
    conv_count = get_conversation_count()
    error_count = analyze_errors()
    learnings_count = analyze_learnings()
    quality_score = get_quality_score()
    
    print(f"   对话数量: {conv_count}")
    print(f"   错误记录: {error_count}")
    print(f"   学习记录: {learnings_count}")
    print(f"   质量评分: {quality_score}/100")
    
    analysis = {
        "conversations": conv_count,
        "quality_score": quality_score,
        "errors": error_count,
        "learnings": learnings_count
    }
    
    # 3. 生成改进建议
    print("\n💡 生成改进建议...")
    improvements = generate_improvements()
    print(f"   生成 {len(improvements)} 条改进建议")
    
    for imp in improvements:
        print(f"   - [{imp['type']}] {imp['target']}: {imp['issue']}")
    
    # 4. 记录学到的东西
    print("\n📝 记录学习...")
    log_learning(f"完成每日复盘，质量评分 {quality_score}/100", "low")
    
    # 5. 运行 Evolution Engine 进化
    run_ai_evolution_evolve()
    
    # 6. 运行 Evolution State Analyzer
    run_evolution_state_analyzer()
    
    # 7. 运行 Evolution Drift Detector
    run_evolution_drift_detector()
    
    # 8. 运行 Memory Pruner
    run_memory_pruner()
    
    # 9. 保存日志
    print("\n💾 保存进化日志...")
    log_file = save_evolution_log(today, analysis, improvements)
    
    # 7. 输出总结
    print(f"\n{'='*60}")
    print(f"📋 复盘完成")
    print(f"{'='*60}")
    print(f"日期: {today}")
    print(f"质量评分: {quality_score}/100")
    print(f"改进建议: {len(improvements)} 条")
    print(f"日志文件: {log_file}")
    print()
    
    return {
        "date": today,
        "analysis": analysis,
        "improvements": improvements,
        "log_file": log_file
    }

if __name__ == "__main__":
    result = run_self_review()
    
    if "--json" in sys.argv:
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))
