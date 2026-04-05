#!/usr/bin/env node
/**
 * Memory Scorer - 记忆质量评分引擎
 * 
 * 基于 AutoAgent Loop 方法论：
 * - 使用频率
 * - 时效性
 * - 信息密度
 * - 噪音检测
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============================================================================
// 评估维度
// ============================================================================

const DIMENSIONS = {
  USAGE_FREQ: 'usage_frequency',      // 使用频率
  RECENCY: 'recency',                 // 最近使用
  INFO_DENSITY: 'info_density',       // 信息密度
  NOISE: 'noise',                     // 噪音检测
  RELEVANCE: 'relevance',             // 主题相关性
  EPHEMERAL: 'ephemeral'              // 临时性
};

// 权重配置
const WEIGHTS = {
  usage_frequency: 0.25,
  recency: 0.20,
  info_density: 0.15,
  noise: 0.20,
  relevance: 0.10,
  ephemeral: 0.10
};

// ============================================================================
// 评分函数
// ============================================================================

/**
 * 主评分函数
 */
export function scoreMemory(item, context = {}) {
  const scores = {};
  const reasons = {};
  
  // 1. 使用频率评分
  scores[DIMENSIONS.USAGE_FREQ] = scoreUsageFrequency(item.usage_count || 0);
  reasons[DIMENSIONS.USAGE_FREQ] = `使用次数: ${item.usage_count || 0}`;
  
  // 2. 最近使用评分
  scores[DIMENSIONS.RECENCY] = scoreRecency(item.last_used);
  reasons[DIMENSIONS.RECENCY] = item.last_used 
    ? `上次使用: ${daysAgo(item.last_used)} 天前`
    : '从未使用';
  
  // 3. 信息密度评分
  scores[DIMENSIONS.INFO_DENSITY] = scoreInfoDensity(item.content);
  reasons[DIMENSIONS.INFO_DENSITY] = `长度: ${(item.content || '').length} 字符`;
  
  // 4. 噪音检测
  scores[DIMENSIONS.NOISE] = scoreNoise(item.content);
  reasons[DIMENSIONS.NOISE] = detectNoiseReason(item.content);
  
  // 5. 主题相关性
  scores[DIMENSIONS.RELEVANCE] = scoreRelevance(item.content, context.topic || '');
  reasons[DIMENSIONS.RELEVANCE] = `相关性: ${context.topic || 'unknown'}`;
  
  // 6. 临时性检测
  scores[DIMENSIONS.EPHEMERAL] = scoreEphemeral(item.content);
  reasons[DIMENSIONS.EPHEMERAL] = detectEphemeralReason(item.content);
  
  // 计算加权总分
  const totalScore = Object.keys(scores).reduce((sum, dim) => {
    return sum + (scores[dim] * WEIGHTS[dim]);
  }, 0);
  
  return {
    total: totalScore,
    dimensions: scores,
    reasons,
    recommendation: getRecommendation(totalScore, scores)
  };
}

/**
 * 使用频率评分（0-1）
 */
function scoreUsageFrequency(usageCount) {
  if (usageCount === 0) return 0.2;
  if (usageCount === 1) return 0.4;
  if (usageCount <= 3) return 0.6;
  if (usageCount <= 5) return 0.8;
  return 1.0;
}

/**
 * 最近使用评分（0-1）
 */
function scoreRecency(lastUsed) {
  if (!lastUsed) return 0.3;
  
  const days = daysAgo(lastUsed);
  
  if (days === 0) return 1.0;
  if (days <= 7) return 0.9;
  if (days <= 30) return 0.7;
  if (days <= 60) return 0.5;
  if (days <= 180) return 0.3;
  return 0.1;
}

/**
 * 信息密度评分（0-1）
 */
function scoreInfoDensity(content) {
  const text = content || '';
  const length = text.length;
  
  // 太短 → 可能是噪音
  if (length < 20) return 0.2;
  // 正常长度
  if (length < 200) return 0.8;
  // 长但有价值
  if (length < 1000) return 0.9;
  // 超长可能需要压缩
  return 0.6;
}

/**
 * 噪音检测（0-1，越高越不是噪音）
 */
function scoreNoise(content) {
  const text = (content || '').toLowerCase();
  
  // 噪音关键词
  const noisePatterns = [
    { pattern: /^(test|测试|试试|测试一下)/, weight: 0.3 },
    { pattern: /^(ok|好的|嗯|收到)/, weight: 0.4 },
    { pattern: /^\s*$/, weight: 0.1 },
    { pattern: /^(no reply|n\/a|null|none)/i, weight: 0.3 }
  ];
  
  for (const { pattern, weight } of noisePatterns) {
    if (pattern.test(text)) return weight;
  }
  
  return 0.8;  // 默认不是噪音
}

/**
 * 主题相关性（0-1）
 */
function scoreRelevance(content, topic) {
  if (!topic) return 0.5;  // 无主题信息
  
  const text = (content || '').toLowerCase();
  const topicWords = topic.toLowerCase().split(/\s+/);
  
  const matches = topicWords.filter(word => text.includes(word)).length;
  const relevance = matches / topicWords.length;
  
  return relevance > 0 ? 0.5 + (relevance * 0.5) : 0.3;
}

/**
 * 临时性检测（0-1，越高越永久）
 */
function scoreEphemeral(content) {
  const text = (content || '').toLowerCase();
  
  // 临时性关键词
  const ephemeralPatterns = [
    { pattern: /^(临时|暂定|草稿|草案)/, weight: 0.2 },
    { pattern: /(待确认|待定|稍后再说)/, weight: 0.3 },
    { pattern: /(一次性的|用完就删|不需要保存)/, weight: 0.1 },
    { pattern: /(重要|必须记住|长期|永久)/, weight: 0.9 }
  ];
  
  for (const { pattern, weight } of ephemeralPatterns) {
    if (pattern.test(text)) return weight;
  }
  
  return 0.6;  // 默认中等永久性
}

// ============================================================================
// 辅助函数
// ============================================================================

function daysAgo(dateStr) {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

function detectNoiseReason(content) {
  const text = (content || '').toLowerCase();
  
  if (/^(test|测试|试试)/.test(text)) return '测试内容';
  if (/^(ok|好的|嗯|收到)/.test(text)) return '简单确认';
  if (/^\s*$/.test(text)) return '空白内容';
  if (/^(no reply|n\/a|null|none)/i.test(text)) return '无意义占位';
  
  return '正常内容';
}

function detectEphemeralReason(content) {
  const text = (content || '').toLowerCase();
  
  if (/临时|暂定/.test(text)) return '标记为临时';
  if (/待确认|待定/.test(text)) return '待确认内容';
  if (/重要|必须记住/.test(text)) return '标记为重要';
  
  return '普通内容';
}

function getRecommendation(totalScore, dimensionScores) {
  // 噪音检测触发
  if (dimensionScores[DIMENSIONS.NOISE] < 0.3) {
    return 'DISCARD';  // 噪音
  }
  
  // 临时性触发
  if (dimensionScores[DIMENSIONS.EPHEMERAL] < 0.3) {
    return 'DISCARD';  // 临时内容
  }
  
  // 长期未用 + 低频
  if (dimensionScores[DIMENSIONS.RECENCY] < 0.3 && 
      dimensionScores[DIMENSIONS.USAGE_FREQ] < 0.4) {
    return 'ARCHIVE';  // 归档
  }
  
  // 分数高
  if (totalScore >= 0.7) {
    return 'KEEP';
  }
  
  // 分数中
  if (totalScore >= 0.4) {
    return 'REVIEW';
  }
  
  // 分数低
  return 'DISCARD';
}

// ============================================================================
// 批量分析
// ============================================================================

export function analyzeMemories(memories, context = {}) {
  const results = {
    keep: [],
    discard: [],
    archive: [],
    review: [],
    summary: {
      total: memories.length,
      keep_count: 0,
      discard_count: 0,
      archive_count: 0,
      review_count: 0,
      avg_score: 0
    }
  };
  
  let totalScore = 0;
  
  for (const memory of memories) {
    const scored = {
      ...memory,
      ...scoreMemory(memory, context)
    };
    
    totalScore += scored.total;
    
    switch (scored.recommendation) {
      case 'KEEP':
        results.keep.push(scored);
        results.summary.keep_count++;
        break;
      case 'DISCARD':
        results.discard.push(scored);
        results.summary.discard_count++;
        break;
      case 'ARCHIVE':
        results.archive.push(scored);
        results.summary.archive_count++;
        break;
      case 'REVIEW':
        results.review.push(scored);
        results.summary.review_count++;
        break;
    }
  }
  
  results.summary.avg_score = memories.length > 0 
    ? (totalScore / memories.length).toFixed(3) 
    : 0;
  
  return results;
}

// ============================================================================
// CLI 入口
// ============================================================================

if (import.meta.url === `file://${process.argv[1]}`) {
  const content = process.argv[2] || '示例记忆内容';
  
  console.log('\n🧠 Memory Scorer - 记忆质量评分\n');
  console.log('='.repeat(50));
  console.log(`评估内容: ${content.substring(0, 50)}...`);
  console.log('');
  
  const result = scoreMemory({ content });
  
  console.log('📊 各项评分:');
  for (const [dim, score] of Object.entries(result.dimensions)) {
    const bar = '█'.repeat(Math.round(score * 10)) + '░'.repeat(10 - Math.round(score * 10));
    console.log(`   ${dim.padEnd(16)} ${bar} ${(score * 100).toFixed(0)}%`);
    console.log(`   ${' '.repeat(16)}   ${result.reasons[dim]}`);
  }
  
  console.log('');
  console.log(`🎯 总分: ${(result.total * 100).toFixed(1)}%`);
  console.log(`📋 建议: ${result.recommendation}`);
  console.log('='.repeat(50));
}

export default { scoreMemory, analyzeMemories };
