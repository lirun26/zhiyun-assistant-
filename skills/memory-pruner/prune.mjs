#!/usr/bin/env node
/**
 * Memory Pruner - 记忆整理执行器
 * 
 * 基于评分结果整理记忆：
 * - KEEP: 保留
 * - REVIEW: 待审核
 * - ARCHIVE: 归档到 history/
 * - DISCARD: 删除
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { analyzeMemories } from './scorer.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.join(__dirname, '../../..');

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run') || !args.includes('--confirm');
const target = args.find(a => a.startsWith('--target='))?.split('=')[1] || 'all';

console.log('\n🧹 Memory Pruner - 记忆整理\n');
console.log('='.repeat(50));
console.log(`模式: ${dryRun ? '🔍 预览（dry-run）' : '⚠️  执行（confirm）'}`);
console.log(`目标: ${target}`);
console.log('');

// ============================================================================
// 读取记忆
// ============================================================================

function readMemoryContent(filePath) {
  try {
    if (!fs.existsSync(filePath)) return { content: '', exists: false };
    return { content: fs.readFileSync(filePath, 'utf-8'), exists: true };
  } catch (e) {
    return { content: '', exists: false, error: e.message };
  }
}

function parseMemoryBlocks(content) {
  if (!content) return [];
  // 按标题分割
  return content.split(/\n(?=## )/).filter(s => s.trim());
}

function extractMemoryTitle(block) {
  const match = block.match(/^##?\s*(.+)/);
  return match ? match[1].trim().substring(0, 40) : '无标题';
}

// ============================================================================
// 记忆文件
// ============================================================================

const memoryFiles = {
  hot: {
    path: path.join(WORKSPACE, 'memory/hot/HOT_MEMORY.md'),
    blocks: []
  },
  warm: {
    path: path.join(WORKSPACE, 'memory/warm/WARM_MEMORY.md'),
    blocks: []
  },
  cold: {
    path: path.join(WORKSPACE, 'MEMORY.md'),
    blocks: []
  }
};

// 读取并分割
for (const [layer, data] of Object.entries(memoryFiles)) {
  const { content } = readMemoryContent(data.path);
  data.blocks = parseMemoryBlocks(content);
  console.log(`${layer === 'hot' ? '🔥' : layer === 'warm' ? '🌡️' : '❄️'} ${layer.toUpperCase()}: ${data.blocks.length} 个记忆块`);
}

console.log('');

// ============================================================================
// 评估每个记忆块
// ============================================================================

function evaluateBlock(block, layer) {
  const title = extractMemoryTitle(block);
  const content = block.trim();
  
  // 简单评分（简化版）
  let score = 0.5;
  let recommendation = 'REVIEW';
  
  // 检查关键词
  if (/重要|必须|永久|长期/.test(content)) {
    score += 0.2;
  }
  if (/临时|待定|草稿/.test(content)) {
    score -= 0.2;
  }
  if (/今天|昨日|现在|当前/.test(content)) {
    score += 0.1;  // 时效性强
  }
  if (content.length < 50) {
    score -= 0.1;  // 太短
  }
  
  // 噪音检测
  if (/^(test|测试|ok|好的)/.test(content)) {
    score = 0.2;
  }
  
  // 判定
  if (score >= 0.7) recommendation = 'KEEP';
  else if (score >= 0.4) recommendation = 'REVIEW';
  else if (score >= 0.2) recommendation = 'ARCHIVE';
  else recommendation = 'DISCARD';
  
  return { title, content, score, recommendation, layer };
}

// ============================================================================
// 分析 HOT_MEMORY
// ============================================================================

if (target === 'all' || target === 'hot') {
  console.log('🔥 分析 HOT_MEMORY...\n');
  
  const results = {
    keep: [],
    review: [],
    archive: [],
    discard: []
  };
  
  for (const block of memoryFiles.hot.blocks) {
    const evaluated = evaluateBlock(block, 'hot');
    results[evaluated.recommendation.toLowerCase()].push(evaluated);
  }
  
  console.log(`   ✅ KEEP:   ${results.keep.length}`);
  console.log(`   ⚠️  REVIEW: ${results.review.length}`);
  console.log(`   📦 ARCHIVE: ${results.archive.length}`);
  console.log(`   ❌ DISCARD: ${results.discard.length}`);
  
  // 显示可清理的
  if (results.discard.length > 0) {
    console.log('\n   🚮 噪音内容 (可删除):');
    results.discard.forEach(item => {
      console.log(`      - ${item.title}`);
    });
  }
  
  if (results.archive.length > 0) {
    console.log('\n   📦 可归档:');
    results.archive.forEach(item => {
      console.log(`      - ${item.title}`);
    });
  }
}

// ============================================================================
// 分析 WARM_MEMORY
// ============================================================================

if (target === 'all' || target === 'warm') {
  console.log('\n🌡️ 分析 WARM_MEMORY...\n');
  
  const results = {
    keep: [],
    review: [],
    archive: [],
    discard: []
  };
  
  for (const block of memoryFiles.warm.blocks) {
    const evaluated = evaluateBlock(block, 'warm');
    results[evaluated.recommendation.toLowerCase()].push(evaluated);
  }
  
  console.log(`   ✅ KEEP:   ${results.keep.length}`);
  console.log(`   ⚠️  REVIEW: ${results.review.length}`);
  console.log(`   📦 ARCHIVE: ${results.archive.length}`);
  console.log(`   ❌ DISCARD: ${results.discard.length}`);
  
  // WARM 太多时建议归档
  if (memoryFiles.warm.blocks.length > 50) {
    console.log('\n   💡 WARM_MEMORY 偏多，建议归档旧内容');
  }
}

// ============================================================================
// 分析 COLD_MEMORY
// ============================================================================

if (target === 'all' || target === 'cold') {
  console.log('\n❄️ 分析 COLD_MEMORY...\n');
  
  const results = {
    keep: [],
    review: [],
    archive: [],
    discard: []
  };
  
  for (const block of memoryFiles.cold.blocks) {
    const evaluated = evaluateBlock(block, 'cold');
    results[evaluated.recommendation.toLowerCase()].push(evaluated);
  }
  
  console.log(`   ✅ KEEP:   ${results.keep.length}`);
  console.log(`   ⚠️  REVIEW: ${results.review.length}`);
  console.log(`   📦 ARCHIVE: ${results.archive.length}`);
  console.log(`   ❌ DISCARD: ${results.discard.length}`);
}

// ============================================================================
// 执行整理
// ============================================================================

console.log('\n' + '='.repeat(50));

if (dryRun) {
  console.log('\n🔍 预览模式 - 仅显示，不执行\n');
  console.log('执行命令以实际清理:');
  console.log('   node memory-pruner/prune.mjs --confirm --target=hot');
  console.log('');
  console.log('或在 memory-tiering 脚本中集成自动清理');
} else {
  console.log('\n⚠️  执行模式 - 实际清理\n');
  
  // TODO: 实现实际清理逻辑
  console.log('   (需要实现归档/删除逻辑)');
  console.log('   当前为预览模式，需要完善后再执行');
}

// ============================================================================
// AutoAgent Loop 方法论总结
// ============================================================================

console.log('\n' + '='.repeat(50));
console.log('📚 AutoAgent Loop 记忆方法论:\n');
console.log('   Keep/Discard 规则:');
console.log('   ✅ KEEP: 分数 >= 0.7');
console.log('   ⚠️  REVIEW: 0.4 <= 分数 < 0.7');
console.log('   📦 ARCHIVE: 0.2 <= 分数 < 0.4');
console.log('   ❌ DISCARD: 分数 < 0.2\n');
console.log('   评分维度:');
console.log('   - 使用频率 (25%)');
console.log('   - 最近使用 (20%)');
console.log('   - 信息密度 (15%)');
console.log('   - 噪音检测 (20%)');
console.log('   - 主题相关 (10%)');
console.log('   - 临时性 (10%)');
console.log('='.repeat(50));
