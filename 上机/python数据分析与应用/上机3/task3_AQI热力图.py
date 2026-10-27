# -*- coding: utf-8 -*-
"""
上机3 任务3：分析各空气质量指数之间的相关关系
功能：
    1) 使用 pandas 读取某市2023年1月-9月 AQI 统计数据（aqi.csv）
    2) 解决中文显示问题，设置字体为黑体，并解决保存图像时负号显示为方块的问题
    3) 计算各空气质量指标与 AQI 的相关系数
    4) 绘制空气质量特征相关性热力图
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 自动切换到脚本所在目录，保证相对路径读取数据文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------- (1) 使用 pandas 读取 AQI 统计数据 ----------
df = pd.read_csv('aqi.csv', encoding='utf-8')
print('数据形状:', df.shape)
print(df.head())

# ---------- (2) 解决中文显示问题，设置字体为黑体，解决负号显示为方块 ----------
plt.rcParams['font.sans-serif'] = ['SimHei']   # 黑体
plt.rcParams['axes.unicode_minus'] = False      # 负号正常显示

# ---------- (3) 计算相关系数 ----------
# 选取数值型指标列（去除日期、质量等级）
num_cols = ['AQI', 'PM2.5含量/ppm', 'PM10含量/ppm', 'SO2含量/ppm',
            'CO含量/ppm', 'NO2含量/ppm', 'O3含量/ppm']
corr = df[num_cols].corr()
print('相关系数矩阵:')
print(corr)

# ---------- (4) 绘制空气质量特征相关性热力图 ----------
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True)
plt.title('空气质量特征相关性热力图')
plt.tight_layout()
plt.savefig('task3_热力图.png', dpi=150, bbox_inches='tight')
plt.show()
