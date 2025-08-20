#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为数据库分类并添加中文翻译
"""
import json
import re

# 定义分类规则
CATEGORIES = {
    'protein': {
        'name': '蛋白质',
        'keywords': ['protein', 'structure', 'fold', 'domain', 'isoform', 'alphafold']
    },
    'genomics': {
        'name': '基因组学',
        'keywords': ['genome', 'genomic', 'gene', 'genetic', 'dna', 'sequence']
    },
    'plant': {
        'name': '植物生物学',
        'keywords': ['plant', 'arabidopsis', 'rice', 'asteraceae', 'botanical']
    },
    'medical': {
        'name': '医学生物学',
        'keywords': ['human', 'disease', 'clinical', 'medical', 'cancer', 'drug']
    },
    'microbiology': {
        'name': '微生物学',
        'keywords': ['bacteria', 'virus', 'viral', 'microbial', 'pathogen']
    },
    'evolution': {
        'name': '进化生物学',
        'keywords': ['evolution', 'phylogen', 'comparative', 'species']
    },
    'omics': {
        'name': '组学',
        'keywords': ['omics', 'transcriptome', 'proteome', 'metabolome']
    },
    'tools': {
        'name': '生物信息工具',
        'keywords': ['tool', 'analysis', 'resource', 'platform', 'service']
    }
}

# 简单的英中翻译字典
TRANSLATIONS = {
    'Asteraceae multi-omics information resource': '菊科多组学信息资源',
    'Structures of human protein isoforms': '人类蛋白质异构体结构',
    'Bio-Analytic Resource for Plant Biology': '植物生物学生物分析资源',
    'AlphaFold-predicted structures of viral proteins': 'AlphaFold预测的病毒蛋白结构',
    'Bacterial and Archaeal Gene Expression Database': '细菌和古菌基因表达数据库',
    'database': '数据库',
    'resource': '资源',
    'tool': '工具',
    'platform': '平台',
    'analysis': '分析',
    'information': '信息',
    'structure': '结构',
    'protein': '蛋白质',
    'gene': '基因',
    'genome': '基因组',
    'plant': '植物',
    'human': '人类',
    'biological': '生物学',
    'molecular': '分子',
    'cellular': '细胞',
    'genetic': '遗传',
    'genomic': '基因组',
    'transcriptomic': '转录组',
    'proteomic': '蛋白质组',
    'metabolomic': '代谢组'
}

def categorize_database(name, description):
    """根据名称和描述给数据库分类"""
    text = (name + ' ' + description).lower()
    
    for category_id, category_info in CATEGORIES.items():
        for keyword in category_info['keywords']:
            if keyword.lower() in text:
                return category_id
    
    return 'tools'  # 默认分类

def translate_description(description):
    """简单翻译描述"""
    # 先尝试直接翻译
    if description in TRANSLATIONS:
        return TRANSLATIONS[description]
    
    # 逐词翻译
    words = re.findall(r'\b\w+\b', description.lower())
    translated_words = []
    
    for word in words:
        if word in TRANSLATIONS:
            translated_words.append(TRANSLATIONS[word])
        else:
            translated_words.append(word)
    
    if translated_words and any(word in TRANSLATIONS for word in words):
        return ' '.join(translated_words)
    
    # 如果没有找到翻译，返回原文
    return description

def process_databases():
    """处理数据库数据，添加分类和翻译"""
    with open('databases.json', 'r', encoding='utf-8') as f:
        databases = json.load(f)
    
    for db in databases:
        # 添加分类
        category = categorize_database(db['name'], db['short_description'])
        db['category'] = category
        db['category_name'] = CATEGORIES[category]['name']
        
        # 添加中文翻译
        db['short_description_zh'] = translate_description(db['short_description'])
    
    # 保存处理后的数据
    with open('databases_processed.json', 'w', encoding='utf-8') as f:
        json.dump(databases, f, ensure_ascii=False, indent=2)
    
    # 统计分类
    category_stats = {}
    for db in databases:
        cat = db['category']
        if cat not in category_stats:
            category_stats[cat] = 0
        category_stats[cat] += 1
    
    print("数据库分类统计:")
    for cat, count in category_stats.items():
        print(f"  {CATEGORIES[cat]['name']}: {count}个")
    
    return databases

if __name__ == "__main__":
    databases = process_databases()
