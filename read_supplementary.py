#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取nar2025databases_sup.xlsx补充数据库并与原数据合并
"""
import pandas as pd
import json
import re

# 补充翻译词典
ADDITIONAL_TRANSLATIONS = {
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
    'metabolomic': '代谢组',
    'bioinformatics': '生物信息学',
    'computational': '计算',
    'sequence': '序列',
    'annotation': '注释',
    'prediction': '预测',
    'classification': '分类',
    'functional': '功能',
    'structural': '结构',
    'evolutionary': '进化',
    'comparative': '比较',
    'cancer': '癌症',
    'disease': '疾病',
    'drug': '药物',
    'therapeutic': '治疗',
    'clinical': '临床',
    'biomarker': '生物标记物',
    'pathway': '通路',
    'network': '网络',
    'interaction': '相互作用',
    'expression': '表达',
    'regulation': '调控',
    'epigenetic': '表观遗传',
    'mutation': '突变',
    'variant': '变异',
    'polymorphism': '多态性',
    'microarray': '芯片',
    'sequencing': '测序',
    'RNA-seq': 'RNA测序',
    'ChIP-seq': 'ChIP测序',
    'single-cell': '单细胞',
    'multi-omics': '多组学',
    'systems biology': '系统生物学',
    'machine learning': '机器学习',
    'artificial intelligence': '人工智能',
    'deep learning': '深度学习'
}

# 分类规则
CATEGORIES = {
    'protein': {
        'name': '蛋白质',
        'keywords': ['protein', 'structure', 'fold', 'domain', 'isoform', 'alphafold', 'structural', 'amino acid']
    },
    'genomics': {
        'name': '基因组学',
        'keywords': ['genome', 'genomic', 'gene', 'genetic', 'dna', 'sequence', 'chromosome', 'variant', 'mutation']
    },
    'plant': {
        'name': '植物生物学',
        'keywords': ['plant', 'arabidopsis', 'rice', 'asteraceae', 'botanical', 'crop', 'agriculture']
    },
    'medical': {
        'name': '医学生物学',
        'keywords': ['human', 'disease', 'clinical', 'medical', 'cancer', 'drug', 'therapeutic', 'biomarker', 'patient']
    },
    'microbiology': {
        'name': '微生物学',
        'keywords': ['bacteria', 'virus', 'viral', 'microbial', 'pathogen', 'microbe', 'prokaryotic']
    },
    'evolution': {
        'name': '进化生物学',
        'keywords': ['evolution', 'phylogen', 'comparative', 'species', 'evolutionary', 'taxonomy']
    },
    'omics': {
        'name': '组学',
        'keywords': ['omics', 'transcriptome', 'proteome', 'metabolome', 'multi-omics', 'rna-seq', 'chip-seq']
    },
    'tools': {
        'name': '生物信息工具',
        'keywords': ['tool', 'analysis', 'resource', 'platform', 'service', 'computational', 'bioinformatics']
    }
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
    """翻译描述"""
    if not description or description == 'nan':
        return description
    
    # 逐词翻译
    words = re.findall(r'\b\w+\b', description.lower())
    translated_parts = []
    
    original_words = description.split()
    for word in original_words:
        word_lower = word.lower().strip('.,!?;:')
        if word_lower in ADDITIONAL_TRANSLATIONS:
            translated_parts.append(ADDITIONAL_TRANSLATIONS[word_lower])
        else:
            # 保持原词
            translated_parts.append(word)
    
    # 如果有翻译内容，返回翻译结果
    translated_text = ' '.join(translated_parts)
    if translated_text != description:
        return translated_text
    
    # 否则返回原文
    return description

def read_supplementary_databases():
    """读取补充的数据库信息"""
    try:
        # 读取补充Excel文件
        df_sup = pd.read_excel('nar2025databases_sup.xlsx')
        
        print("补充Excel文件的列名:")
        print(df_sup.columns.tolist())
        print(f"\n补充数据形状: {df_sup.shape}")
        
        # 显示前几行数据
        print("\n前5行补充数据:")
        print(df_sup.head())
        
        # 读取原始数据
        with open('databases_processed.json', 'r', encoding='utf-8') as f:
            original_databases = json.load(f)
        
        print(f"\n原始数据库数量: {len(original_databases)}")
        
        # 处理补充数据
        supplementary_databases = []
        start_id = len(original_databases) + 1
        
        for index, row in df_sup.iterrows():
            db_info = {
                'id': start_id + index,
                'name': str(row.get('Database name', '')),
                'url': str(row.get('URL', '')),
                'short_description': str(row.get('Short description', '')),
                'description': str(row.get('Short description', '')),
                'last_update': '',
                'access': 'Free',
                'data_type': ''
            }
            
            # 添加分类
            category = categorize_database(db_info['name'], db_info['short_description'])
            db_info['category'] = category
            db_info['category_name'] = CATEGORIES[category]['name']
            
            # 添加中文翻译
            db_info['short_description_zh'] = translate_description(db_info['short_description'])
            
            supplementary_databases.append(db_info)
        
        # 合并数据
        all_databases = original_databases + supplementary_databases
        
        # 保存合并后的数据
        with open('databases_processed.json', 'w', encoding='utf-8') as f:
            json.dump(all_databases, f, ensure_ascii=False, indent=2)
        
        print(f"\n成功添加了 {len(supplementary_databases)} 个补充数据库")
        print(f"总数据库数量: {len(all_databases)}")
        
        # 统计新的分类
        category_stats = {}
        for db in all_databases:
            cat = db['category']
            if cat not in category_stats:
                category_stats[cat] = 0
            category_stats[cat] += 1
        
        print("\n更新后的数据库分类统计:")
        for cat, count in category_stats.items():
            print(f"  {CATEGORIES[cat]['name']}: {count}个")
        
        return all_databases
        
    except Exception as e:
        print(f"处理补充数据时出错: {e}")
        return []

if __name__ == "__main__":
    databases = read_supplementary_databases()
