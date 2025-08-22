#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加遗漏的第73行数据：3D-GNOME 3.0
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
    'personalized medicine': '个性化医疗', 'precision medicine': '精准医疗',
    # 3D基因组相关术语
    '3d': '三维', 'three-dimensional': '三维', 'spatial': '空间', 'chromatin': '染色质',
    'chromosome': '染色体', 'topology': '拓扑', 'conformation': '构象', 'folding': '折叠',
    'compartment': '区室', 'domain': '结构域', 'loop': '环', 'boundary': '边界',
    'insulator': '绝缘子', 'enhancer': '增强子', 'promoter': '启动子', 'tad': 'TAD结构域'
}

# 分类规则
UPDATED_CATEGORIES = {
    'protein': {
        'name': '蛋白质',
        'keywords': ['protein', 'structure', 'fold', 'domain', 'isoform', 'alphafold', 'structural', 'amino acid', 'peptide', 'enzyme', 'kinase', 'phosphatase', 'protease']
    },
    'genomics': {
        'name': '基因组学',
        'keywords': ['genome', 'genomic', 'gene', 'genetic', 'dna', 'sequence', 'chromosome', 'variant', 'mutation', 'gwas', 'snp', 'indel', 'cnv', 'structural variant', '3d', 'chromatin', 'chromosome', 'topology']
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

def add_missing_3d_gnome():
    """添加遗漏的第73行数据：3D-GNOME 3.0"""
    try:
        # 读取Excel文件
        df = pd.read_excel('nar2025web.xlsx')
        
        print("检查第73行数据:")
        row73_data = df.iloc[72]  # Excel第73行 = Python索引72
        print(f"Database name: {row73_data['Database name']}")
        print(f"URL: {row73_data['URL']}")
        print(f"Short description: {row73_data['Short description']}")
        
        # 读取现有数据
        with open('databases_processed.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        
        print(f"\n当前数据库总数: {len(existing_data)}")
        
        # 检查第73行数据是否已存在
        row73_name = str(row73_data['Database name'])
        exists = False
        for db in existing_data:
            if db['name'] == row73_name:
                exists = True
                print(f"第73行工具 '{row73_name}' 已存在，ID: {db['id']}")
                break
        
        if not exists:
            print(f"第73行工具 '{row73_name}' 不存在，需要添加")
            
            # 处理Database name列的特殊格式
            original_name = row73_data['Database name']
            processed_name, extracted_description = process_database_name(original_name)
            
            # 如果有从name中提取的描述，使用它；否则使用原有的Short description
            final_description = extracted_description if extracted_description else str(row73_data['Short description'])
            
            # 创建新的Web工具条目
            new_tool = {
                'id': len(existing_data) + 1,
                'name': processed_name,
                'url': str(row73_data['URL']),
                'short_description': final_description,
                'description': final_description,
                'last_update': '',
                'access': 'Free',
                'data_type': 'web',  # 标记为web工具类型
                'resource_type': 'web'   # 区分数据库和网站
            }
            
            # 添加分类
            category = categorize_database(new_tool['name'], new_tool['short_description'])
            new_tool['category'] = category
            new_tool['category_name'] = UPDATED_CATEGORIES[category]['name']
            
            # 添加中文翻译
            new_tool['short_description_zh'] = translate_description(new_tool['short_description'])
            
            # 添加到数据中
            existing_data.append(new_tool)
            
            # 保存更新后的数据
            with open('databases_processed.json', 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n成功添加第73行Web工具:")
            print(f"  原始名称: {original_name}")
            print(f"  处理后名称: {processed_name}")
            print(f"  提取的描述: {extracted_description}")
            print(f"  最终描述: {final_description}")
            print(f"  中文翻译: {new_tool['short_description_zh']}")
            print(f"  分类: {new_tool['category_name']}")
            print(f"  新的总数: {len(existing_data)}")
            
            return True
        else:
            print("第73行Web工具已存在，无需添加")
            return False
            
    except Exception as e:
        print(f"添加第73行Web工具时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_missing_3d_gnome()
