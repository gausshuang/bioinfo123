#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取nar2025databases.xlsx文件并提取数据库信息
"""
import pandas as pd
import json
import requests
import time

def translate_text(text, target_lang='zh'):
    """
    简单的翻译功能，这里使用一个基础的翻译逻辑
    实际项目中可以使用Google Translate API或其他翻译服务
    """
    # 这里先返回原文，后续可以集成真正的翻译API
    return text

def read_database_info():
    """读取Excel文件中的数据库信息"""
    try:
        # 读取Excel文件
        df = pd.read_excel('nar2025databases.xlsx')
        
        # 打印列名以了解数据结构
        print("Excel文件的列名:")
        print(df.columns.tolist())
        print("\n数据形状:", df.shape)
        
        # 显示前几行数据
        print("\n前5行数据:")
        print(df.head())
        
        # 将数据转换为字典格式
        databases = []
        for index, row in df.iterrows():
            db_info = {
                'id': index + 1,
                'name': str(row.get('Database name', '')),
                'url': str(row.get('URL', '')),
                'category': '',  # 暂时为空，可以根据数据库名称分类
                'short_description': str(row.get('Short description', '')),
                'short_description_zh': '',  # 待翻译
                'description': str(row.get('Short description', '')),  # 使用short description
                'last_update': '',
                'access': 'Free',  # 假设都是免费的
                'data_type': ''
            }
            databases.append(db_info)
        
        # 保存为JSON文件以便后续使用
        with open('databases.json', 'w', encoding='utf-8') as f:
            json.dump(databases, f, ensure_ascii=False, indent=2)
        
        print(f"\n成功读取了 {len(databases)} 个数据库信息")
        return databases
        
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return []

if __name__ == "__main__":
    databases = read_database_info()
