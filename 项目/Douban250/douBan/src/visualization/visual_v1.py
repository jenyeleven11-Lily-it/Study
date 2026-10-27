"""
豆瓣 Top250 数据可视化（全英文标签版）
生成 4 张图表：
1. Boxplot of Ratings by Genre
2. Year vs Rating Trend
3. Number of High-Score Movies by Region
4. Distribution of Number of Ratings
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ========================= 配置 =========================
CLEAN_PATH = r"D:\Studywork\studySpace\douBan\data\cleaned\douban_top250_cleaned.csv"
OUTPUT_DIR = r"D:\Studywork\studySpace\douBan\result\visualization"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 设置全局画布大小和样式（不涉及中文字体）
sns.set_style("whitegrid")
plt.rcParams['axes.unicode_minus'] = False

# ========================= 1. 加载数据 =========================
df = pd.read_csv(CLEAN_PATH)
print(f"Loaded {len(df)} movies")


# ============================================================
# Chart 1: Boxplot of Ratings by Genre (Top 8)
# ============================================================
print("\nGenerating Chart 1: Genre Boxplot")

df['genre'] = df['genre'].fillna('')
df['genre_list'] = df['genre'].apply(lambda x: x.split(', ') if x != '' else [])
df_exploded = df.explode('genre_list')
df_exploded = df_exploded[df_exploded['genre_list'] != ''].reset_index(drop=True)

genre_counts = df_exploded['genre_list'].value_counts()
top8_genres = genre_counts.head(8).index.tolist()
data_box = df_exploded[df_exploded['genre_list'].isin(top8_genres)]

plt.figure(figsize=(12, 6))
sns.boxplot(x='genre_list', y='rating', data=data_box, palette='Set2')
plt.title('Top 8 Genres: Rating Distribution (Boxplot)', fontsize=16, fontweight='bold')
plt.xlabel('Genre', fontsize=13)
plt.ylabel('Douban Rating', fontsize=13)
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(fontsize=11)
plt.ylim(8.0, 9.8)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '1_genre_boxplot.png'), dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 1_genre_boxplot.png")


# ============================================================
# Chart 2: Year vs Rating Trend
# ============================================================
print("\nGenerating Chart 2: Year-Rating Line")

df['year'] = pd.to_numeric(df['year'], errors='coerce')
yearly_avg = df.groupby('year')['rating'].agg(['mean', 'count']).round(2)
yearly_avg = yearly_avg[yearly_avg['count'] >= 2]

plt.figure(figsize=(14, 6))
plt.plot(yearly_avg.index, yearly_avg['mean'],
         marker='o', linewidth=2.5, markersize=7, color='#2E86AB',
         markerfacecolor='#A23B72', markeredgecolor='#A23B72')
plt.title('Average Rating by Year', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=13)
plt.ylabel('Average Rating', fontsize=13)
plt.xticks(fontsize=11, rotation=45)
plt.yticks(fontsize=11)
plt.ylim(8.0, 9.8)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '2_year_rating_line.png'), dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 2_year_rating_line.png")


# ============================================================
# Chart 3: High-Score Movies by Region (>= 9.0)
# ============================================================
print("\nGenerating Chart 3: High-Score by Region Bar")

HIGH_SCORE = 9.0
df_high = df[df['rating'] >= HIGH_SCORE]
region_counts = df_high['region'].value_counts()

plt.figure(figsize=(10, 6))
colors = ['#FF6B6B', '#FECA57', '#48DBFB', '#FF9FF3']
bars = plt.bar(region_counts.index, region_counts.values, color=colors[:len(region_counts)],
               edgecolor='black', linewidth=1.2)
plt.title(f'Number of High-Rating Movies (≥{HIGH_SCORE}) by Region', fontsize=16, fontweight='bold')
plt.xlabel('Region', fontsize=13)
plt.ylabel('Count', fontsize=13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=11)
for bar, val in zip(bars, region_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             str(val), ha='center', va='bottom', fontsize=14, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '3_region_highscore_bar.png'), dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 3_region_highscore_bar.png")


# ============================================================
# Chart 4: Distribution of Number of Ratings (for high-score movies)
# ============================================================
print("\nGenerating Chart 4: Ratings Count Histogram")

df_high = df[df['rating'] >= HIGH_SCORE].copy()
df_high['num_ratings'] = pd.to_numeric(df_high['num_ratings'], errors='coerce')
df_high = df_high.dropna(subset=['num_ratings'])

plt.figure(figsize=(12, 6))
n, bins, patches = plt.hist(df_high['num_ratings'], bins=30, edgecolor='black',
                            alpha=0.75, color='#2E86AB')
for i, patch in enumerate(patches):
    patch.set_facecolor(plt.cm.Blues(i / len(patches) + 0.3))

plt.title(f'Distribution of Number of Ratings (Movies ≥ {HIGH_SCORE})', fontsize=16, fontweight='bold')
plt.xlabel('Number of Ratings (in 10k)', fontsize=13)
plt.ylabel('Number of Movies', fontsize=13)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

# Format x-axis in 10k
from matplotlib.ticker import FuncFormatter
def format_wan(x, p):
    if x >= 10000:
        return f'{int(x/10000)}万'
    return str(int(x))
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_wan))

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '4_ratings_distribution_hist.png'), dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 4_ratings_distribution_hist.png")


# ========================= 汇总输出 =========================
print("\n" + "="*50)
print("🎉 All charts generated successfully!")
print(f"📁 Output directory: {OUTPUT_DIR}")
print("📈 Generated images:")
print("   ✅ 1_genre_boxplot.png        - Genre Rating Boxplot")
print("   ✅ 2_year_rating_line.png     - Year-Rating Trend")
print("   ✅ 3_region_highscore_bar.png - High-Score Movies by Region")
print("   ✅ 4_ratings_distribution_hist.png - Ratings Count Distribution")
print("="*50)