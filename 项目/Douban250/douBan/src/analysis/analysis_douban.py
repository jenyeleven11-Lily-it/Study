"""
豆瓣 Top250 数据分析
包含 4 个分析角度 + 4 个可视化图表：
1. 不同类型电影评分对比（箱线图）
2. 上映年份与评分关系（折线图）
3. 各地区高分电影数量（柱状图）
4. 高分电影评分人数分布（直方图）
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')


# ========================= 配置 =========================
CLEAN_PATH = r"D:\Studywork\studySpace\douBan\data\cleaned\douban_top250_cleaned.csv"
OUTPUT_DIR = r"D:\Studywork\studySpace\douBan\result\analysis"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ========================= 1. 加载数据 =========================
df = pd.read_csv(CLEAN_PATH)
print(f" 加载数据：共 {len(df)} 部电影")

# ============================================================
# 分析 1：不同类型电影评分对比（箱线图）
# ============================================================
print("\n" + "="*50)
print(" 分析 1：不同类型电影评分对比")

# 拆分类型（英文逗号分隔）
df['genre'] = df['genre'].fillna('')
df['genre_list'] = df['genre'].apply(lambda x: x.split(', ') if x != '' else [])
df_exploded = df.explode('genre_list')
df_exploded = df_exploded[df_exploded['genre_list'] != ''].reset_index(drop=True)

# 统计各类型数量
genre_stats = df_exploded.groupby('genre_list')['rating'].agg([
    ('数量', 'count'),
    ('平均分', 'mean'),
    ('中位数', 'median'),
    ('标准差', 'std')
]).round(2)
genre_stats = genre_stats.sort_values('数量', ascending=False)

print("\n各类型电影统计：")
print(genre_stats.head(15))

# 保存统计结果
genre_stats.to_csv(os.path.join(OUTPUT_DIR, 'genre_stats.csv'), encoding='utf-8-sig')

# 画箱线图（取数量前 8 的类型）
plt.figure(figsize=(12, 6))
top8_genres = genre_stats.head(8).index.tolist()
data_box = df_exploded[df_exploded['genre_list'].isin(top8_genres)]
sns.boxplot(x='genre_list', y='rating', data=data_box, palette='Set2')
plt.title('Top 8 类型电影评分分布（箱线图）', fontsize=14)
plt.xlabel('类型')
plt.ylabel('评分')
plt.xticks(rotation=45, ha='right')
plt.ylim(8.0, 9.8)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '1_genre_boxplot.png'), dpi=300, bbox_inches='tight')
plt.close()
print(" 箱线图已保存：1_genre_boxplot.png")


# ============================================================
# 分析 2：上映年份与评分关系（折线图）
# ============================================================
print("\n" + "="*50)
print(" 分析 2：上映年份与评分关系")

df['year'] = pd.to_numeric(df['year'], errors='coerce')
yearly_stats = df.groupby('year')['rating'].agg([
    ('平均分', 'mean'),
    ('数量', 'count')
]).round(2)
yearly_stats = yearly_stats[yearly_stats['数量'] >= 2]

print("\n各年份统计（部分）：")
print(yearly_stats.head(10))

yearly_stats.to_csv(os.path.join(OUTPUT_DIR, 'yearly_stats.csv'), encoding='utf-8-sig')

plt.figure(figsize=(14, 6))
plt.plot(yearly_stats.index, yearly_stats['平均分'], marker='o', linewidth=2, markersize=6)
plt.title('不同年份上映电影的平均评分变化', fontsize=14)
plt.xlabel('上映年份')
plt.ylabel('平均评分')
plt.ylim(8.0, 9.8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '2_year_rating_line.png'), dpi=300, bbox_inches='tight')
plt.close()
print(" 年份-评分折线图已保存：2_year_rating_line.png")


# ============================================================
# 分析 3：各地区高分电影数量（柱状图）
# ============================================================
print("\n" + "="*50)
print(" 分析 3：各地区高分电影数量")

HIGH_SCORE_THRESHOLD = 9.0
df_high = df[df['rating'] >= HIGH_SCORE_THRESHOLD]
region_counts = df_high['region'].value_counts()

print(f"\n高分电影（≥{HIGH_SCORE_THRESHOLD}分）地区分布：")
print(region_counts)

plt.figure(figsize=(10, 6))
colors = ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff']
bars = plt.bar(region_counts.index, region_counts.values, color=colors[:len(region_counts)])
plt.title(f'各地区高分电影数量（≥{HIGH_SCORE_THRESHOLD}分）', fontsize=14)
plt.xlabel('地区')
plt.ylabel('高分电影数量（部）')
for bar, val in zip(bars, region_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             str(val), ha='center', va='bottom', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '3_region_highscore_bar.png'), dpi=300, bbox_inches='tight')
plt.close()
print(" 地区高分电影柱状图已保存：3_region_highscore_bar.png")


# ============================================================
# 分析 4：高分电影评分人数分布（直方图）
# ============================================================
print("\n" + "="*50)
print(" 分析 4：高分电影评分人数分布")

df_high = df[df['rating'] >= HIGH_SCORE_THRESHOLD].copy()
df_high['num_ratings'] = pd.to_numeric(df_high['num_ratings'], errors='coerce')
df_high = df_high.dropna(subset=['num_ratings'])

print(f"\n高分电影（≥{HIGH_SCORE_THRESHOLD}分）评分人数统计：")
print(df_high['num_ratings'].describe())

plt.figure(figsize=(12, 6))
plt.hist(df_high['num_ratings'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
plt.title(f'高分电影（≥{HIGH_SCORE_THRESHOLD}分）评分人数分布', fontsize=14)
plt.xlabel('评分人数（万人）')
plt.ylabel('电影数量（部）')
ticks = plt.xticks()[0]
plt.xticks(ticks, [f'{int(t/10000)}万' if t >= 10000 else str(int(t)) for t in ticks])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '4_ratings_distribution_hist.png'), dpi=300, bbox_inches='tight')
plt.close()
print(" 评分人数分布直方图已保存：4_ratings_distribution_hist.png")


# ============================================================
# 汇总输出
# ============================================================
print("\n" + "="*50)
print(" 所有分析完成！生成文件清单：")
print(f" 输出目录：{OUTPUT_DIR}")
print(" 统计表格：")
print(f"     - genre_stats.csv")
print(f"     - yearly_stats.csv")
print("  可视化图片：")
print(f"  - 1_genre_boxplot.png（类型评分箱线图）")
print(f"  - 2_year_rating_line.png（年份-评分折线图）")
print(f"  - 3_region_highscore_bar.png（地区高分电影柱状图）")
print(f"  - 4_ratings_distribution_hist.png（评分人数分布直方图）")
print("="*50)