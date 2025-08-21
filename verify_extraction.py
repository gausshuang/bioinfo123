#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证第92-186行的提取是否正确
"""
import pandas as pd

def verify_extraction():
    try:
        # 读取Excel文件
        df = pd.read_excel('nar2024databases.xlsx')
        
        print(f"Excel文件总行数: {len(df)}")
        print(f"第92-186行应该有: {186-92+1} = 95行")
        
        # Excel第92行 = Python索引91
        # Excel第186行 = Python索引185
        start_idx = 91  # Excel第92行
        end_idx = 186   # Excel第186行，Python切片需要+1
        
        # 正确的提取应该是df.iloc[91:186]，这会提取索引91到185，共95行
        correct_range = df.iloc[start_idx:end_idx]
        print(f"正确提取的行数: {len(correct_range)}")
        
        print(f"\n第92行(索引91): {df.iloc[91]['Database name']}")
        print(f"第186行(索引185): {df.iloc[185]['Database name']}")
        
        # 检查我们之前的提取
        previous_range = df.iloc[91:187]  # 这个范围实际上是91:186，因为187超出了范围
        print(f"\n之前提取的实际行数: {len(previous_range)}")
        
        # 显示前5行和后5行，确认范围正确
        print(f"\n前5行:")
        for i in range(5):
            idx = 91 + i
            print(f"  第{idx+1}行(Excel第{idx+1}行): {df.iloc[idx]['Database name']}")
            
        print(f"\n后5行:")
        for i in range(5):
            idx = 185 - 4 + i  # 从第182行开始显示5行到第186行
            print(f"  第{idx+1}行(Excel第{idx+1}行): {df.iloc[idx]['Database name']}")
            
    except Exception as e:
        print(f"验证时出错: {e}")

if __name__ == "__main__":
    verify_extraction()
