#!/usr/bin/env node
/**
 * 自我评估模块 v2 - 融入 AutoAgent Loop 方法论
 * 
 * 评估维度：
 * 1. 能力清单
 * 2. 性能指标（passed/score）
 * 3. 根因分析（7类失败）
 * 4. 知识缺口
 */

import fs from 'fs';
import path from 'path';

const WORKSPACE = '../../..';

console.log('🧬 AI Evolution Engine v2 - 自我评估\n');
console.log('='.repeat(50));

// ============================================================================
// 1. 能力清单
// ============================================================================
console.log('\n📊 能力清单:');

const skills = fs.readdirSync(path.join(WORKSPACE, 'skills'))
  .filter(f => {
    try {
      return fs.statSync(path.join(WORKSPACE, 'skills', f)).isDirectory();
    } catch { return false; }
  });
console.log(`  ✅ 技能: ${skills.length} 个`);
console.log('     ' + skills.slice(0, 5).join(', ') + (skills.length > 5 ? '...' : ''));

const tools = ['exec', 'read', 'write', 'edit', 'web_fetch', 'web_search', 'image'];
console.log(`  ✅ 工具: ${tools.length} 种`);
console.log('     ' + tools.join(', '));

// ============================================================================
// 2. 性能指标（从 results.tsv 读取）
// ============================================================================
console.log('\n📈 性能指标:');

const resultsFile = path.join(WORKSPACE, 'skills', 'autoagent-loop', 'results.tsv');
if (fs.existsSync(resultsFile)) {
  const content = fs.readFileSync(resultsFile, 'utf-8');
  const lines = content.trim().split('\n');
  
  if (lines.length > 1) {
    // 取最新一条
    const latest = lines[lines.length - 1].split('\t');
    console.log(`  📁 最新实验:`);
    console.log(`     Commit: ${latest[0]}`);
    console.log(`     Passed: ${latest[2]}`);
    console.log(`     Score: ${latest[1]}`);
    console.log(`     Status: ${latest[5]}`);
    console.log(`     Cost: $${latest[4] || 0}`);
  }
  
  // 历史统计
  const records = lines.slice(1).map(l => {
    const parts = l.split('\t');
    return {
      commit: parts[0],
      score: parseFloat(parts[1]) || 0,
      passed: parts[2] || '0/0',
      status: parts[5] || 'unknown'
    };
  });
  
  if (records.length > 0) {
    const keep = records.filter(r => r.status === 'keep').length;
    const discard = records.filter(r => r.status === 'discard').length;
    console.log(`  📜 历史统计:`);
    console.log(`     总实验: ${records.length}`);
    console.log(`     Keep: ${keep} (${(keep/records.length*100).toFixed(1)}%)`);
    console.log(`     Discard: ${discard} (${(discard/records.length*100).toFixed(1)}%)`);
  }
} else {
  console.log('  ⚠️ 暂无实验记录 (results.tsv)');
  console.log('     运行 evolve-v2.mjs 开始实验循环');
}

// ============================================================================
// 3. 根因分析 - 检查最近的错误
// ============================================================================
console.log('\n🔍 根因分析:');

const errorsFile = path.join(WORKSPACE, '.learnings', 'ERRORS.md');
const learningsFile = path.join(WORKSPACE, '.learnings', 'LEARNINGS.md');

const errorCategories = {
  '误解任务': 0,
  '缺少能力或工具': 0,
  '信息收集不足': 0,
  '执行策略不当': 0,
  '缺少验证': 0,
  '环境/依赖问题': 0,
  '静默失败': 0
};

if (fs.existsSync(errorsFile)) {
  const errors = fs.readFileSync(errorsFile, 'utf-8');
  
  // 简单统计错误类型（从错误日志中）
  const errorLines = errors.split('\n');
  errorLines.forEach(line => {
    Object.keys(errorCategories).forEach(cat => {
      if (line.includes(cat)) errorCategories[cat]++;
    });
  });
  
  console.log('  📋 错误分类统计:');
  Object.entries(errorCategories)
    .filter(([_, count]) => count > 0)
    .sort((a, b) => b[1] - a[1])
    .forEach(([cat, count]) => {
      console.log(`     - ${cat}: ${count} 次`);
    });
  
  if (Object.values(errorCategories).every(c => c === 0)) {
    console.log('     (暂无分类错误)');
  }
} else {
  console.log('  ⚠️ 暂无错误记录 (.learnings/ERRORS.md)');
}

// ============================================================================
// 4. 知识缺口
// ============================================================================
console.log('\n💡 知识缺口:');

const gaps = [];

// 检查 skills 覆盖
const coreSkills = ['autoagent-loop', 'ai-evolution-engine-v2', 'self-review'];
const missingCore = coreSkills.filter(s => !skills.includes(s));
if (missingCore.length > 0) {
  gaps.push(`核心技能: ${missingCore.join(', ')} 未安装`);
}

// 检查记忆系统
const hotMemory = path.join(WORKSPACE, 'memory', 'hot', 'HOT_MEMORY.md');
const warmMemory = path.join(WORKSPACE, 'memory', 'warm', 'WARM_MEMORY.md');
if (!fs.existsSync(hotMemory)) gaps.push('HOT_MEMORY.md 未配置');
if (!fs.existsSync(warmMemory)) gaps.push('WARM_MEMORY.md 未配置');

// 检查 autoagent-loop 集成
if (!fs.existsSync(resultsFile)) {
  gaps.push('AutoAgent Loop 实验循环未开始');
}

if (gaps.length > 0) {
  gaps.forEach(q => console.log(`  ⚠️ ${q}`));
} else {
  console.log('  ✅ 无明显缺口');
}

// ============================================================================
// 5. 改进建议（基于 AutoAgent Loop 方法论）
// ============================================================================
console.log('\n🎯 改进建议:');

const suggestions = [];

// 基于错误分析
const topError = Object.entries(errorCategories)
  .filter(([_, count]) => count > 0)
  .sort((a, b) => b[1] - a[1])[0];

if (topError) {
  const [cat, count] = topError;
  if (cat === '缺少能力或工具') {
    suggestions.push('【高优先级】考虑添加专用工具，减少 prompt 调优');
  } else if (cat === '误解任务') {
    suggestions.push('【高优先级】改进 SYSTEM_PROMPT，增加任务澄清步骤');
  } else if (cat === '缺少验证') {
    suggestions.push('【高优先级】增加输出验证步骤');
  }
}

// 基于实验统计
if (fs.existsSync(resultsFile)) {
  const records = lines.slice(1).map(l => l.split('\t'));
  const recent = records.slice(-5);
  const recentKeepRate = recent.filter(r => r[5] === 'keep').length / recent.length;
  
  if (recentKeepRate < 0.3) {
    suggestions.push('【中优先级】近期 Keep 率偏低，考虑保守改进策略');
  } else if (recentKeepRate > 0.7) {
    suggestions.push('【中优先级】实验环境良好，可以尝试激进改进');
  }
}

// 基于知识缺口
if (!fs.existsSync(resultsFile)) {
  suggestions.push('【建议】运行 evolve-v2.mjs 开始 AutoAgent 实验循环');
}

if (suggestions.length > 0) {
  suggestions.forEach(s => console.log(`  ${s}`));
} else {
  console.log('  ✅ 系统状态良好');
}

console.log('\n' + '='.repeat(50));
console.log('✅ 评估完成');
console.log('💡 下一步: 运行 evolve-v2.mjs 开始进化');
