# -*- coding: utf-8 -*-
"""
上机3 任务2：分析学生考试成绩与各个特征之间的关系
功能：
    1) 使用 NumPy 均值函数，求 自我效能感、考试课程准备情况 两个特征下总成绩的均值
    2) 创建画布并添加子图
    3) 在子图上绘制两个特征与总成绩均值的柱状图
    4) 分析两个特征与考试总成绩的关系
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 自动切换到脚本所在目录，保证相对路径读取数据文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置中文字体为黑体，并解决负号显示为方块的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取学生成绩数据
df = pd.read_excel('student_grade.xlsx')

# ---------- (1) 使用 NumPy 均值函数求两个特征下对应总成绩的均值 ----------
# 自我效能感（低/中/高）下的总成绩均值
se_mean = df.groupby('自我效能感')['总成绩'].apply(np.mean).reindex(['低', '中', '高'])
# 考试课程准备情况（未完成/完成）下的总成绩均值
prep_mean = df.groupby('考试课程准备情况')['总成绩'].apply(np.mean).reindex(['未完成', '完成'])
print('自我效能感下总成绩均值:')
print(se_mean)
print('\n考试课程准备情况下总成绩均值:')
print(prep_mean)

# ---------- (2) 创建画布，并添加子图 ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---------- (3) 在子图上绘制对应内容的柱状图 ----------
axes[0].bar(se_mean.index, se_mean.values, color='steelblue')
axes[0].set_title('自我效能感与总成绩均值关系')
axes[0].set_xlabel('自我效能感')
axes[0].set_ylabel('总成绩均值')
for i, v in enumerate(se_mean.values):
    axes[0].text(i, v + 1, round(v, 1), ha='center')

axes[1].bar(prep_mean.index, prep_mean.values, color='orange')
axes[1].set_title('考试课程准备情况与总成绩均值关系')
axes[1].set_xlabel('考试课程准备情况')
axes[1].set_ylabel('总成绩均值')
for i, v in enumerate(prep_mean.values):
    axes[1].text(i, v + 1, round(v, 1), ha='center')

plt.tight_layout()
plt.savefig('task2_柱状图.png', dpi=150, bbox_inches='tight')
plt.show()

# ---------- (4) 分析两个特征与考试总成绩的关系 ----------
print('\n特征与总成绩均值关系分析:')
print('自我效能感越高，总成绩均值越高，说明自我效能感与成绩呈正相关。')
print('完成考试课程准备的学生总成绩均值明显高于未完成者，说明备考情况影响成绩。')
