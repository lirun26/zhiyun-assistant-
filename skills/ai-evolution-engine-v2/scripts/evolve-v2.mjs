#!/usr/bin/env node
/**
 * 进化机制 v2 - 融入 AutoAgent Loop 方法论
 * 
 * 核心流程（借鉴 autoagent）：
 * 1. 检查当前状态（baseline）
 * 2. 诊断失败（根因分析）
 * 3. 生成改进提案
 * 4. 过度拟合检测
 * 5. 应用改进
 * 6. Keep/Discard 判定
 * 7. 记录到 results.tsv
 * 8. NEVER STOP（除非达到目标）
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const WORKSPACE = '../../..';
const AUTOAGENT_LOOP = path.join(WORKSPACE, 'skills', 'autoagent-loop');
const RESULTS_FILE = path.join(AUTOAGENT_LOOP, 'results.tsv');

console.log('🚀 AI Evolution Engine v2 - 进化\n');
console.log('='.repeat(50));
console.log('AutoAgent Loop 方法论:\n');
console.log('  1. 诊断失败（根因分析）');
console.log('  2. 生成改进提案');
console.log('  3. 过度拟合检测');
console.log('  4. 应用改进');
console.log('  5. Keep/Discard 判定');
console.log('  6. 记录到 results.tsv');
console.log('='.repeat(50));

// ============================================================================
// 1. 检查当前 baseline
// ============================================================================
console.log('\n[1/6] 检查 baseline...\n');

let baseline = null;
if (fs.existsSync(RESULTS_FILE)) {
  const content = fs.readFileSync(RESULTS_FILE, 'utf-8');
  const lines = content.trim().split('\n');
  if (lines.length > 1) {
    const latest = lines[lines.length - 1].split('\t');
    baseline = {
      commit: latest[0],
      score: parseFloat(latest[1]) || 0,
      passed: latest[2] || '0/0',
      status: latest[5] || 'unknown',
      complexity: 3  // 简化处理
    };
    console.log(`  📁 最新 baseline:`);
    console.log(`     Commit: ${baseline.commit}`);
    console.log(`     Score: ${baseline.score}`);
    console.log(`     Passed: ${baseline.passed}`);
    console.log(`     Status: ${baseline.status}`);
  }
}

if (!baseline) {
  console.log('  ⚠️ 暂无 baseline');
  console.log('  💡 建议先进行首次实验建立 baseline');
}

// ============================================================================
// 2. 根因分析
// ============================================================================
console.log('\n[2/6] 根因分析...\n');

const errorsFile = path.join(WORKSPACE, '.learnings', 'ERRORS.md');
const errorCategories = {
  '误解任务': [],
  '缺少能力或工具': [],
  '信息收集不足': [],
  '执行策略不当': [],
  '缺少验证': [],
  '环境/依赖问题': [],
  '静默失败': []
};

if (fs.existsSync(errorsFile)) {
  const errors = fs.readFileSync(errorsFile, 'utf-8');
  const entries = errors.split('\n## ');
  
  entries.forEach(entry => {
    if (!entry.trim()) return;
    const lines = entry.split('\n');
    const title = lines[0].replace(/^#+\s*/, '').trim();
    
    Object.keys(errorCategories).forEach(cat => {
      if (title.includes(cat) || entry.includes(cat)) {
        errorCategories[cat].push(title);
      }
    });
  });
  
  const categoriesWithErrors = Object.entries(errorCategories)
    .filter(([_, items]) => items.length > 0);
  
  if (categoriesWithErrors.length > 0) {
    console.log('  📋 错误分类:');
    categoriesWithErrors.forEach(([cat, items]) => {
      console.log(`\n     🔴 ${cat} (${items.length}):`);
      items.slice(0, 3).forEach(item => {
        console.log(`        - ${item.substring(0, 50)}...`);
      });
      if (items.length > 3) {
        console.log(`        ... 还有 ${items.length - 3} 项`);
      }
    });
  } else {
    console.log('  ✅ 无分类错误');
  }
} else {
  console.log('  ⚠️ 暂无错误记录');
}

// ============================================================================
// 3. 生成改进提案
// ============================================================================
console.log('\n[3/6] 生成改进提案...\n');

const proposals = [];

// 基于根因分析的提案
const categoriesWithErrors = Object.entries(errorCategories)
  .filter(([_, items]) => items.length > 0);

if (categoriesWithErrors.length > 0) {
  categoriesWithErrors.forEach(([cat, items]) => {
    if (cat === '误解任务') {
      proposals.push({
        type: 'prompt',
        priority: 'high',
        title: '改进 SYSTEM_PROMPT',
        description: '增加任务澄清步骤，减少误解',
        target: 'SOUL.md, AGENTS.md',
        taskSpecific: false
      });
    } else if (cat === '缺少能力或工具') {
      proposals.push({
        type: 'tool',
        priority: 'high',
        title: '添加专用工具',
        description: `为 ${items[0].substring(0, 30)}... 等场景添加专用工具`,
        target: 'skills/',
        taskSpecific: false
      });
    } else if (cat === '缺少验证') {
      proposals.push({
        type: 'verification',
        priority: 'high',
        title: '增加验证步骤',
        description: '在关键操作后增加输出验证',
        target: '工作流程',
        taskSpecific: false
      });
    } else if (cat === '环境/依赖问题') {
      proposals.push({
        type: 'env',
        priority: 'medium',
        title: '修复环境/依赖',
        description: '检查并修复依赖问题',
        target: '环境配置',
        taskSpecific: false
      });
    } else if (cat === '静默失败') {
      proposals.push({
        type: 'verification',
        priority: 'high',
        title: '增加结果检查',
        description: '增加结果验证机制，避免静默失败',
        target: '工作流程',
        taskSpecific: false
      });
    }
  });
}

// 检查是否需要技能扩展
const skills = fs.readdirSync(path.join(WORKSPACE, 'skills'))
  .filter(f => {
    try { return fs.statSync(path.join(WORKSPACE, 'skills', f)).isDirectory(); }
    catch { return false; }
  });

const coreSkills = ['autoagent-loop', 'ai-evolution-engine-v2', 'self-review'];
const missingCore = coreSkills.filter(s => !skills.includes(s));
if (missingCore.length > 0) {
  proposals.push({
    type: 'skill',
    priority: 'medium',
    title: '安装核心技能',
    description: `缺失: ${missingCore.join(', ')}`,
    target: 'skills/',
    taskSpecific: false
  });
}

// 检查记忆系统
const hotMemory = path.join(WORKSPACE, 'memory', 'hot', 'HOT_MEMORY.md');
const warmMemory = path.join(WORKSPACE, 'memory', 'warm', 'WARM_MEMORY.md');
if (!fs.existsSync(hotMemory) || !fs.existsSync(warmMemory)) {
  proposals.push({
    type: 'memory',
    priority: 'high',
    title: '完善记忆系统',
    description: '三层记忆架构未完全配置',
    target: 'memory/',
    taskSpecific: false
  });
}

if (proposals.length > 0) {
  console.log('  📋 改进提案:');
  proposals.forEach((p, i) => {
    const priorityIcon = p.priority === 'high' ? '🔴' : '🟡';
    console.log(`\n     ${i + 1}. ${priorityIcon} [${p.type}] ${p.title}`);
    console.log(`        ${p.description}`);
    console.log(`        目标: ${p.target}`);
  });
} else {
  console.log('  ✅ 暂无改进提案');
}

// ============================================================================
// 4. 过度拟合检测
// ============================================================================
console.log('\n[4/6] 过度拟合检测...\n');

// 红旗模式检测
const redFlags = [
  { pattern: /task.*specific.*hardcode/i, name: '任务特定硬编码' },
  { pattern: /only.*work.*for.*\w+/i, name: '只对特定任务有效' },
  { pattern: /keyword.*exact.*match/i, name: '关键词精确匹配' },
  { pattern: /if.*task.*==.*["']/i, name: '任务名称硬编码' }
];

let overfitCount = 0;
proposals.forEach(p => {
  redFlags.forEach(flag => {
    if (flag.pattern.test(p.description) || flag.pattern.test(p.title)) {
      console.log(`  ⚠️ 红旗: "${p.title}" - ${flag.name}`);
      overfitCount++;
    }
  });
});

if (overfitCount === 0) {
  console.log('  ✅ 无过度拟合红旗');
}

// 泛化检查
const genericProposals = proposals.filter(p => !p.taskSpecific);
console.log(`\n  📊 泛化评估:`);
console.log(`     总提案: ${proposals.length}`);
console.log(`     泛化良好: ${genericProposals.length}`);
console.log(`     任务特定: ${proposals.length - genericProposals.length}`);

// ============================================================================
// 5. 应用改进（模拟）
// ============================================================================
console.log('\n[5/6] 应用改进...\n');

// 这里应该是实际的代码修改逻辑
// 目前是模拟演示
console.log('  ⚠️ 实际应用需要:');
console.log('     1. 读取当前 harness');
console.log('     2. 应用选中的提案');
console.log('     3. 提交 git');
console.log('     4. 重新运行 benchmark');
console.log('');
console.log('  💡 要实际运行实验循环，请使用:');
console.log('     python3 skills/autoagent-loop/demo.py');

// ============================================================================
// 6. Keep/Discard 判定
// ============================================================================
console.log('\n[6/6] Keep/Discard 判定规则:\n');

console.log('  📜 判定规则（来自 AutoAgent Loop）:');
console.log('');
console.log('     ✅ KEEP 如果:');
console.log('        - passed 提升了');
console.log('        - passed 相同 + harness 更简单');
console.log('');
console.log('     ❌ DISCARD 如果:');
console.log('        - 无提升且更复杂');
console.log('        - 过度拟合（只对特定 task 有效）');
console.log('');

// 模拟判定
if (baseline) {
  console.log('  📊 当前状态:');
  console.log(`     Baseline Score: ${baseline.score}`);
  console.log(`     Baseline Passed: ${baseline.passed}`);
  console.log('');
  console.log('  🎯 实验设计:');
  console.log('     1. 选择一个改进提案');
  console.log('     2. 应用改动');
  console.log('     3. 运行 benchmark');
  console.log('     4. 比较分数变化');
  console.log('     5. 决定 Keep 或 Discard');
} else {
  console.log('  💡 建议:');
  console.log('     1. 先运行 assess-v2.mjs 建立 baseline');
  console.log('     2. 应用第一个改进提案');
  console.log('     3. 记录结果');
  console.log('     4. 开始迭代');
}

// ============================================================================
// 记录到 results.tsv
// ============================================================================
console.log('\n' + '='.repeat(50));
console.log('📝 记录机制:\n');

console.log('  实验结果记录到: skills/autoagent-loop/results.tsv');
console.log('');
console.log('  格式:');
console.log('  commit | avg_score | passed | task_scores | cost_usd | status | description');
console.log('');
console.log('  示例:');
console.log('  abc123 | 0.7234 | 15/50 | {"task1": 1.0} | 0.5234 | keep | improved prompt');
console.log('');
console.log('  💡 每次实验后自动记录，用于追踪进化历史');

// ============================================================================
// NEVER STOP 提醒
// ============================================================================
console.log('\n' + '='.repeat(50));
console.log('⏰ NEVER STOP 规则:\n');

console.log('  一旦开始实验循环，不要停下来问"要不要继续"。');
console.log('  不要停在"好的停止点"。');
console.log('  继续迭代直到达到目标或被打断。');
console.log('');
console.log('  🚀 持续进化，持续改进！');

console.log('\n' + '='.repeat(50));
console.log('✅ 进化规划完成');
console.log('💡 下一步: 选择一个提案开始实验');
