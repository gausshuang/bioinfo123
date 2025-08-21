#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
找出缺失的数据库
"""
import pandas as pd
import json

def find_missing_database():
    try:
        # 读取Excel文件
        df = pd.read_excel('nar2024databases.xlsx')
        
        print("Excel文件第92-186行的所有数据库:")
        excel_databases = []
        
        # 提取第92-186行（索引91-185）
        for i in range(91, 186):
            db_name = df.iloc[i]['Database name']
            excel_databases.append(db_name)
            print(f"第{i+1}行: {db_name}")
        
        print(f"\nExcel中第92-186行总数: {len(excel_databases)}")
        
        # 读取当前处理的数据
        with open('databases_processed.json', 'r', encoding='utf-8') as f:
            processed_data = json.load(f)
        
        # 找出最后95个添加的数据库（从ID 327开始）
        last_95_databases = []
        for db in processed_data:
            if db['id'] >= 327:  # 326个现有 + 1
                last_95_databases.append(db['name'])
        
        print(f"\n已处理的最后95个数据库:")
        for i, db_name in enumerate(last_95_databases, 1):
            print(f"{i}: {db_name}")
        
        print(f"\n已处理的数据库总数: {len(last_95_databases)}")
        
        # 找出缺失的数据库
        missing = []
        for excel_db in excel_databases:
            if excel_db not in last_95_databases:
                missing.append(excel_db)
        
        extra = []
        for processed_db in last_95_databases:
            if processed_db not in excel_databases:
                extra.append(processed_db)
        
        if missing:
            print(f"\n缺失的数据库 ({len(missing)}个):")
            for db in missing:
                print(f"  - {db}")
        
        if extra:
            print(f"\n多出的数据库 ({len(extra)}个):")
            for db in extra:
                print(f"  - {db}")
        
        if not missing and not extra:
            print("\n✅ 所有数据库都正确匹配！")
            
    except Exception as e:
        print(f"检查时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_missing_database()
