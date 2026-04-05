#!/usr/bin/env node
/**
 * Memory Analyzer - 分析记忆质量
 * 
 * 分析三层记忆，输出质量报告
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { analyzeMemories } from './scorer.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.resolve(__dirname, '../..');

console.log('\n🧹 Memory Pruner - 记忆质量分析\n');
console.log('='.repeat(50));

// ============================================================================
// 读取记忆
// ============================================================================

function readMemoryFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) return [];
    const content = fs.readFileSync(filePath, 'utf-8');
    // 简单解析，每行一段
    return content
      .split(/\n(?=##|\#)/)
      .filter(s => s.trim())
      .map((block, i) => {
        const lines = block.split('\n');
        const firstLine = lines[0].replace(/^#+\s*/, '').trim();
        return {
          id: `${path.basename(filePath)}-${i}`,
          path: filePath,
          title: firstLine.substring(0, 50),
          content: block.trim(),
          last_used: getLastUsedFromContent(block),
          usage_count: countUsageInContent(block)
        };
      });
  } catch (e) {
    console.error(`Error reading ${filePath}: ${e.message}`);
    return [];
  }
}

function getLastUsedFromContent(content) {
  // 尝试从内容中提取时间
  const timeMatch = content.match(/(\d{4}-\d{2}-\d{2})/);
  return timeMatch ? timeMatch[1] : null;
}

function countUsageInContent(content) {
  // 简单统计：计算关键词出现次数
  const patterns = ['更新', '修改', '使用', '引用', '参考'];
  let count = 0;
  for (const p of patterns) {
    const matches = content.match(new RegExp(p, 'g'));
    if (matches) count += matches.length;
  }
  return count;
}

// ============================================================================
// 分析三层记忆
// ============================================================================

const memories = {
  hot: readMemoryFile(path.join(WORKSPACE, 'memory/hot/HOT_MEMORY.md')),
  warm: readMemoryFile(path.join(WORKSPACE, 'memory/warm/WARM_MEMORY.md')),
  cold: readMemoryFile(path.join(WORKSPACE, 'MEMORY.md'))
};

console.log(`📚 记忆统计:`);
console.log(`   🔥 HOT:  ${memories.hot.length} 条`);
console.log(`   🌡️  WARM: ${memories.warm.length} 条`);
console.log(`   ❄️  COLD: ${memories.cold.length} 条`);
console.log('');

// ============================================================================
// 分析 HOT_MEMORY
// ============================================================================

console.log('🔥 HOT_MEMORY 分析:');
if (memories.hot.length > 0) {
  const hotResults = analyzeMemories(memories.hot);
  
  console.log(`   📊 总分: ${hotResults.summary.avg_score}`);
  console.log(`   ✅ KEEP:   ${hotResults.summary.keep_count}`);
  console.log(`   ⚠️  REVIEW: ${hotResults.summary.review_count}`);
  console.log(`   📦 ARCHIVE: ${hotResults.summary.archive_count}`);
  console.log(`   ❌ DISCARD: ${hotResults.summary.discard_count}`);
  
  if (hotResults.discard.length > 0) {
    console.log('\n   🚮 可清理 (DISCARD):');
    hotResults.discard.slice(0, 3).forEach(item => {
      console.log(`      - ${item.title}`);
    });
    if (hotResults.discard.length > 3) {
      console.log(`      ... 还有 ${hotResults.discard.length - 3} 条`);
    }
  }
} else {
  console.log('   (空)');
}

// ============================================================================
// 分析 WARM_MEMORY
// ============================================================================

console.log('\n🌡️ WARM_MEMORY 分析:');
if (memories.warm.length > 0) {
  const warmResults = analyzeMemories(memories.warm);
  
  console.log(`   📊 总分: ${warmResults.summary.avg_score}`);
  console.log(`   ✅ KEEP:   ${warmResults.summary.keep_count}`);
  console.log(`   ⚠️  REVIEW: ${warmResults.summary.review_count}`);
  console.log(`   📦 ARCHIVE: ${warmResults.summary.archive_count}`);
  console.log(`   ❌ DISCARD: ${warmResults.summary.discard_count}`);
  
  if (warmResults.archive.length > 0) {
    console.log('\n   📦 可归档 (ARCHIVE):');
    warmResults.archive.slice(0, 3).forEach(item => {
      console.log(`      - ${item.title}`);
    });
  }
} else {
  console.log('   (空)');
}

// ============================================================================
// 分析 COLD_MEMORY
// ============================================================================

console.log('\n❄️ COLD_MEMORY 分析:');
if (memories.cold.length > 0) {
  const coldResults = analyzeMemories(memories.cold);
  
  console.log(`   📊 总分: ${coldResults.summary.avg_score}`);
  console.log(`   ✅ KEEP:   ${coldResults.summary.keep_count}`);
  console.log(`   ⚠️  REVIEW: ${coldResults.summary.review_count}`);
  console.log(`   📦 ARCHIVE: ${coldResults.summary.archive_count}`);
  console.log(`   ❌ DISCARD: ${coldResults.summary.discard_count}`);
  
  // 检查是否有旧 secrets
  const content = fs.readFileSync(path.join(WORKSPACE, 'MEMORY.md'), 'utf-8');
  if (content.includes('***MASKED***')) {
    console.log('\n   🔒 已脱敏: Secrets 已替换为 ***MASKED***');
  }
} else {
  console.log('   (空)');
}

// ============================================================================
// 总结建议
// ============================================================================

console.log('\n' + '='.repeat(50));
console.log('💡 整理建议:\n');

const totalItems = memories.hot.length + memories.warm.length + memories.cold.length;
const totalDiscard = (memories.hot.length > 0 ? 1 : 0) + 
                     (memories.warm.length > 30 ? 1 : 0) + 
                     (memories.cold.length > 200 ? 1 : 0);

if (totalItems > 100) {
  console.log('   📌 记忆总量偏多，建议清理');
} else if (totalItems < 10) {
  console.log('   📌 记忆较少，可以适当补充');
} else {
  console.log('   📌 记忆量适中');
}

console.log('\n🗑️  可执行清理:');
console.log('   node memory-pruner/prune.mjs --dry-run  # 预览');
console.log('   node memory-pruner/prune.mjs --confirm  # 确认执行');
console.log('\n' + '='.repeat(50));
