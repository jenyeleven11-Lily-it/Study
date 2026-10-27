# -*- coding: utf-8 -*-
"""
上机3 任务1：分析学生考试成绩特征的分布与分散情况
功能：
    1) 使用 pandas 读取学生考试成绩数据（student_grade.xlsx）
    2) 将总成绩划分为 不及格/及格/良好/优秀 4 个等级，绘制饼图
    3) 提取 数学/阅读/写作 3 项单科成绩，绘制箱线图
    4) 分析总成绩分布情况和单科成绩的分散情况
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

# 自动切换到脚本所在目录，保证相对路径读取数据文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置中文字体为黑体，并解决负号显示为方块的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ---------- (1) 使用 pandas 读取学生考试成绩数据 ----------
df = pd.read_excel('student_grade.xlsx')
print('数据形状:', df.shape)
print(df.head())

# ---------- (2) 将总成绩分为4个区间，计算各区间的学生人数，绘制饼图 ----------
# 等级划分：0-150 不及格、151-200 及格、201-250 良好、251-300 优秀
bins = [0, 150, 200, 250, 300]
labels = ['不及格', '及格', '良好', '优秀']
df['等级'] = pd.cut(df['总成绩'], bins=bins, labels=labels)
counts = df['等级'].value_counts()
print('各等级学生人数:')
print(counts)

plt.figure(figsize=(6, 6))
plt.pie(counts, labels=counts.index, autopct='%.1f%%', startangle=90)
plt.title('学生考试总成绩分布饼图')
plt.savefig('task1_饼图.png', dpi=150, bbox_inches='tight')
plt.show()

subjects = ['数学成绩', '阅读成绩', '写作成绩']
plt.figure(figsize=(8, 6))
df[subjects].boxplot()
plt.title('学生各项考试成绩分散情况箱线图')
plt.ylabel('成绩')
plt.savefig('task1_箱线图.png', dpi=150, bbox_inches='tight')
plt.show()

print('\n总成绩描述统计:')
print(df['总成绩'].describe())
print('\n单科成绩描述统计:')
print(df[subjects].describe())

