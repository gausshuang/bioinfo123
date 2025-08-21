#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取nar2024web.xlsx中的74个web网站并与现有数据合并
特殊处理Database name列的{A}:{B}格式
"""
import pandas as pd
import json
import re

# 扩展的翻译词典
EXTENDED_TRANSLATIONS = {
    # 基础词汇
    'database': '数据库', 'resource': '资源', 'tool': '工具', 'platform': '平台',
    'analysis': '分析', 'information': '信息', 'structure': '结构', 'protein': '蛋白质',
    'gene': '基因', 'genome': '基因组', 'plant': '植物', 'human': '人类',
    'biological': '生物学', 'molecular': '分子', 'cellular': '细胞', 'genetic': '遗传',
    'genomic': '基因组', 'transcriptomic': '转录组', 'proteomic': '蛋白质组',
    'metabolomic': '代谢组', 'bioinformatics': '生物信息学', 'computational': '计算',
    'sequence': '序列', 'annotation': '注释', 'prediction': '预测', 'classification': '分类',
    'functional': '功能', 'structural': '结构', 'evolutionary': '进化', 'comparative': '比较',
    'cancer': '癌症', 'disease': '疾病', 'drug': '药物', 'therapeutic': '治疗',
    'clinical': '临床', 'biomarker': '生物标记物', 'pathway': '通路', 'network': '网络',
    'interaction': '相互作用', 'expression': '表达', 'regulation': '调控',
    'epigenetic': '表观遗传', 'mutation': '突变', 'variant': '变异',
    'polymorphism': '多态性', 'microarray': '芯片', 'sequencing': '测序',
    'RNA-seq': 'RNA测序', 'ChIP-seq': 'ChIP测序', 'single-cell': '单细胞',
    'multi-omics': '多组学', 'systems biology': '系统生物学',
    'machine learning': '机器学习', 'artificial intelligence': '人工智能',
    'deep learning': '深度学习', 'visualization': '可视化', 'browser': '浏览器',
    'viewer': '查看器', 'explorer': '探索器', 'portal': '门户', 'server': '服务器',
    'service': '服务', 'web': '网络', 'online': '在线', 'interface': '界面',
    'application': '应用', 'software': '软件', 'pipeline': '流水线',
    'workflow': '工作流', 'framework': '框架', 'library': '库', 'package': '包',
    'suite': '套件', 'collection': '集合', 'repository': '仓库', 'archive': '档案',
    'hub': '中心', 'center': '中心', 'institute': '研究所', 'laboratory': '实验室',
    'consortium': '联盟', 'project': '项目', 'initiative': '倡议', 'program': '程序',
    'search': '搜索', 'query': '查询', 'browse': '浏览', 'download': '下载',
    'upload': '上传', 'submit': '提交', 'access': '访问', 'retrieve': '检索',
    'filter': '过滤', 'sort': '排序', 'compare': '比较', 'align': '比对',
    'alignment': '比对', 'blast': 'BLAST比对', 'similarity': '相似性',
    'homology': '同源性', 'phylogeny': '系统发育', 'tree': '进化树',
    'cluster': '聚类', 'clustering': '聚类', 'motif': '模式', 'domain': '功能域',
    'family': '家族', 'ortholog': '直系同源', 'paralog': '旁系同源',
    'synteny': '共线性', 'conservation': '保守性', 'diversity': '多样性',
    'variation': '变异', 'association': '关联', 'correlation': '相关',
    'enrichment': '富集', 'ontology': '本体', 'taxonomy': '分类学',
    'nomenclature': '命名法', 'standard': '标准', 'format': '格式',
    'protocol': '协议', 'guideline': '指南', 'tutorial': '教程',
    'documentation': '文档', 'manual': '手册', 'help': '帮助', 'support': '支持',
    'community': '社区', 'forum': '论坛', 'wiki': '维基', 'blog': '博客',
    'news': '新闻', 'update': '更新', 'release': '发布', 'version': '版本',
    'beta': '测试版', 'stable': '稳定版', 'development': '开发',
    'maintenance': '维护', 'deprecated': '已弃用', 'legacy': '遗留',
    'migration': '迁移', 'integration': '整合', 'api': 'API接口',
    'rest': 'REST接口', 'json': 'JSON格式', 'xml': 'XML格式',
    'csv': 'CSV格式', 'tsv': 'TSV格式', 'excel': 'Excel格式',
    'pdf': 'PDF格式', 'image': '图像', 'figure': '图表', 'chart': '图表',
    'graph': '图形', 'plot': '绘图', 'histogram': '直方图', 'heatmap': '热图',
    'scatter': '散点图', 'barplot': '条形图', 'boxplot': '箱线图',
    'network diagram': '网络图', 'pathway map': '通路图',
    'genome browser': '基因组浏览器', 'gene expression': '基因表达',
    'protein structure': '蛋白质结构', 'molecular dynamics': '分子动力学',
    'docking': '分子对接', 'virtual screening': '虚拟筛选',
    'drug design': '药物设计', 'bioactivity': '生物活性', 'toxicity': '毒性',
    'pharmacology': '药理学', 'clinical trial': '临床试验',
    'epidemiology': '流行病学', 'public health': '公共卫生',
    'personalized medicine': '个性化医疗', 'precision medicine': '精准医疗'
}

# 分类规则
UPDATED_CATEGORIES = {
    'protein': {
        'name': '蛋白质',
        'keywords': ['protein', 'structure', 'fold', 'domain', 'isoform', 'alphafold', 'structural', 'amino acid', 'peptide', 'enzyme', 'kinase', 'phosphatase', 'protease']
    },
    'genomics': {
        'name': '基因组学',
        'keywords': ['genome', 'genomic', 'gene', 'genetic', 'dna', 'sequence', 'chromosome', 'variant', 'mutation', 'gwas', 'snp', 'indel', 'cnv', 'structural variant']
    },
    'plant': {
        'name': '植物生物学',
        'keywords': ['plant', 'arabidopsis', 'rice', 'asteraceae', 'botanical', 'crop', 'agriculture', 'photosynthesis', 'chloroplast', 'wheat', 'maize', 'soybean']
    },
    'medical': {
        'name': '医学生物学',
        'keywords': ['human', 'disease', 'clinical', 'medical', 'cancer', 'drug', 'therapeutic', 'biomarker', 'patient', 'health', 'tumor', 'oncology', 'pharmacology']
    },
    'microbiology': {
        'name': '微生物学',
        'keywords': ['bacteria', 'virus', 'viral', 'microbial', 'pathogen', 'microbe', 'prokaryotic', 'archaea', 'fungal', 'yeast', 'microbiome']
    },
    'evolution': {
        'name': '进化生物学',
        'keywords': ['evolution', 'phylogen', 'comparative', 'species', 'evolutionary', 'taxonomy', 'tree', 'ancestral', 'divergence', 'selection']
    },
    'omics': {
        'name': '组学',
        'keywords': ['omics', 'transcriptome', 'proteome', 'metabolome', 'multi-omics', 'rna-seq', 'chip-seq', 'single-cell', 'epigenome', 'spatial', 'lipidomics']
    },
    'tools': {
        'name': '生物信息工具',
        'keywords': ['tool', 'analysis', 'resource', 'platform', 'service', 'computational', 'bioinformatics', 'software', 'web', 'online', 'server', 'portal', 'browser', 'viewer', 'pipeline', 'workflow']
    }
}

def process_database_name(name_str):
    """处理Database name列的{A}:{B}格式"""
    name_str = str(name_str)
    
    # 检查是否包含冒号
    if ':' in name_str:
        # 分割字符串
        parts = name_str.split(':', 1)  # 只分割第一个冒号
        if len(parts) == 2:
            database_name = parts[0].strip()
            short_description = parts[1].strip()
            return database_name, short_description
    
    # 如果没有冒号或格式不符合，返回原名称和空描述
    return name_str, ''

def categorize_database(name, description):
    """根据名称和描述给数据库分类"""
    text = (name + ' ' + description).lower()
    
    for category_id, category_info in UPDATED_CATEGORIES.items():
        for keyword in category_info['keywords']:
            if keyword.lower() in text:
                return category_id
    
    return 'tools'  # 默认分类

def translate_description(description):
    """翻译描述"""
    if not description or description == 'nan' or str(description) == 'nan':
        return description
    
    description = str(description)
    original_desc = description
    
    # 直接查找完整短语的翻译
    desc_lower = description.lower()
    
    # 按长度排序，优先匹配长短语
    sorted_translations = sorted(EXTENDED_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    translated_desc = description
    for eng, chn in sorted_translations:
        if eng.lower() in desc_lower:
            # 使用正则表达式进行词边界匹配
            pattern = r'\b' + re.escape(eng) + r'\b'
            translated_desc = re.sub(pattern, chn, translated_desc, flags=re.IGNORECASE)
    
    # 如果翻译后与原文差异较大，返回翻译结果
    if translated_desc != original_desc:
        return translated_desc
    
    # 否则返回原文
    return description

def read_2024_web_sites():
    """读取2024年web网站信息并与现有数据合并"""
    try:
        # 读取2024年web网站Excel文件
        df_web = pd.read_excel('nar2024web.xlsx')
        
        print("2024年web网站Excel文件的列名:")
        print(df_web.columns.tolist())
        print(f"\n2024年web网站数据形状: {df_web.shape}")
        
        # 显示前几行数据
        print("\n前5行2024年web网站数据:")
        print(df_web.head())
        
        # 读取现有数据
        with open('databases_processed.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        print(f"\n现有数据数量: {len(existing_data)}")
        
        # 处理2024年web网站数据
        new_websites = []
        start_id = len(existing_data) + 1
        
        for index, row in df_web.iterrows():
            # 处理Database name列的特殊格式
            original_name = row.get('Database name', '')
            processed_name, extracted_description = process_database_name(original_name)
            
            # 如果有从name中提取的描述，使用它；否则使用原有的Short description
            final_description = extracted_description if extracted_description else str(row.get('Short description', ''))
            
            web_info = {
                'id': start_id + index,
                'name': processed_name,
                'url': str(row.get('URL', '')),
                'short_description': final_description,
                'description': final_description,
                'last_update': '',
                'access': 'Free',
                'data_type': 'web',  # 标记为web工具类型
                'resource_type': 'web'   # 区分数据库和网站
            }
            
            # 添加分类
            category = categorize_database(web_info['name'], web_info['short_description'])
            web_info['category'] = category
            web_info['category_name'] = UPDATED_CATEGORIES[category]['name']
            
            # 添加中文翻译
            web_info['short_description_zh'] = translate_description(web_info['short_description'])
            
            new_websites.append(web_info)
            
            # 显示处理结果（前几个）
            if index < 5:
                print(f"\n处理第{index+1}个网站:")
                print(f"  原始名称: {original_name}")
                print(f"  处理后名称: {processed_name}")
                print(f"  提取的描述: {extracted_description}")
                print(f"  最终描述: {final_description}")
        
        # 合并数据
        all_resources = existing_data + new_websites
        
        # 保存合并后的数据
        with open('databases_processed.json', 'w', encoding='utf-8') as f:
            json.dump(all_resources, f, ensure_ascii=False, indent=2)
        
        print(f"\n成功添加了 {len(new_websites)} 个2024年web网站")
        print(f"总资源数量: {len(all_resources)}")
        
        # 统计分类和类型
        category_stats = {}
        db_stats = {}
        web_stats = {}
        
        for resource in all_resources:
            cat = resource['category']
            res_type = resource.get('resource_type', 'database')
            
            if cat not in category_stats:
                category_stats[cat] = 0
                db_stats[cat] = 0
                web_stats[cat] = 0
            
            category_stats[cat] += 1
            if res_type == 'database':
                db_stats[cat] += 1
            else:
                web_stats[cat] += 1
        
        print("\n更新后的资源分类统计:")
        for cat, count in category_stats.items():
            print(f"  {UPDATED_CATEGORIES[cat]['name']}: {count}个 (数据库: {db_stats[cat]}, 网站: {web_stats[cat]})")
        
        # 统计总数
        total_databases = sum(db_stats.values())
        total_websites = sum(web_stats.values())
        print(f"\n总计: {len(all_resources)}个资源 (数据库: {total_databases}, 网站: {total_websites})")
        
        return all_resources
        
    except Exception as e:
        print(f"处理2024年web网站数据时出错: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    resources = read_2024_web_sites()
