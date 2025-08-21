#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Excel文件第92-187行的数据
"""
import pandas as pd

def check_excel_rows():
    try:
        # 读取Excel文件
        df = pd.read_excel('nar2024databases.xlsx')
        
        print(f"总行数: {len(df)}")
        print(f"第92-187行应该有: {187-92+1} = 96行")
        
        # 检查实际的行范围
        # Excel第92行 = Python索引91
        # Excel第187行 = Python索引186
        start_idx = 91  # Excel第92行
        end_idx = 187   # Excel第187行+1（因为Python切片不包含结束索引）
        
        if len(df) >= 187:
            actual_rows = df.iloc[start_idx:end_idx]
            print(f"实际提取的行数: {len(actual_rows)}")
            
            print(f"\n第92行(索引91): {df.iloc[91]['Database name']}")
            print(f"第187行(索引186): {df.iloc[186]['Database name']}")
            
            # 检查我们之前提取的范围
            previous_range = df.iloc[91:187]  # 这只到186，缺少第187行
            print(f"\n之前的提取范围(91:187)行数: {len(previous_range)}")
            print(f"正确的提取范围应该是(91:187): {len(df.iloc[91:187])}")
            
            # 显示缺失的第187行
            print(f"\n缺失的第187行数据:")
            print(f"Database name: {df.iloc[186]['Database name']}")
            print(f"URL: {df.iloc[186]['URL']}")
            print(f"Short description: {df.iloc[186]['Short description']}")
            
        else:
            print(f"Excel文件只有{len(df)}行，没有第187行")
            
    except Exception as e:
        print(f"检查时出错: {e}")

if __name__ == "__main__":
    check_excel_rows()
