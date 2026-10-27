"""
豆瓣 Top250 数据清洗、转换与集成脚本
功能：去除 NBSP、拆分中英文、过滤低分/少评、去重、
      统一年份、提取类型、评分四舍五入、按大区分类（国产/日韩/欧美）
"""

import pandas as pd
import os
import re
import unicodedata

# ========================= 配置 =========================
RAW_PATH = r"D:\Studywork\studySpace\douBan\data\raw\douban_top250_2026.csv"
CLEAN_PATH = r"D:\Studywork\studySpace\douBan\data\cleaned\douban_top250_cleaned.csv"

MIN_RATING = 2.0
MIN_RATINGS = 1000

# ========================= 清洗函数 =========================
def clean_text(s):
    """去除所有常见 Unicode 空白字符及 NBSP"""
    if isinstance(s, str):
        s = unicodedata.normalize('NFKC', s)
        s = re.sub(r'[\u00A0\u3000\u200B\u200C\u200D\uFEFF]', '', s)
        s = s.strip()
        return s
    return s

def clean_all_text_columns(df):
    """对所有字符串列应用清洗"""
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(clean_text)
    return df

# ========================= 转换函数 =========================
def extract_genre(row):
    """
    从 info_text 中提取类型，按 '/' 分割取最后一段，
    再按空格或 '/' 拆分成多个类型，去重后返回逗号分隔的字符串。
    """
    info = row.get('info_text', '')
    if not isinstance(info, str) or not info.strip():
        return ''
    parts = [p.strip() for p in info.split('/') if p.strip()]
    if not parts:
        return ''
    genre_part = parts[-1]
    genre_part = genre_part.replace('/', ' ')
    genres = [g.strip() for g in genre_part.split() if g.strip()]
    seen = set()
    unique_genres = []
    for g in genres:
        if g not in seen:
            seen.add(g)
            unique_genres.append(g)
    return ', '.join(unique_genres)

# ========================= 集成函数（区域分类） =========================
def assign_region(country):
    """根据主要制片地区划分大区"""
    if not isinstance(country, str) or not country:
        return '其他'
    # 取第一个国家（若存在多个以'/'分隔）
    main_country = country.split('/')[0].strip()
    # 定义关键词
    china_keywords = ['中国', '台湾', '香港', '澳门']
    japan_korea_keywords = ['日本', '韩国']
    europe_america_keywords = [
        '美国', '英国', '法国', '德国', '意大利', '西班牙',
        '加拿大', '澳大利亚', '新西兰', '荷兰', '比利时',
        '瑞士', '瑞典', '挪威', '丹麦', '芬兰', '爱尔兰',
        '葡萄牙', '希腊', '俄罗斯', '乌克兰', '波兰',
        '捷克', '匈牙利', '奥地利'
    ]
    # 匹配
    if any(key in main_country for key in china_keywords):
        return '国产'
    if any(key in main_country for key in japan_korea_keywords):
        return '日韩'
    if any(key in main_country for key in europe_america_keywords):
        return '欧美'
    return '其他'   # 未匹配的归为其他（如印度、伊朗等）

# ========================= 主流程 =========================
def main():
    if not os.path.exists(RAW_PATH):
        print(f"错误：找不到原始数据文件 {RAW_PATH}")
        return

    df = pd.read_csv(RAW_PATH)
    print(f"原始数据共 {len(df)} 条记录")

    # -------- 清洗 ----------
    # 1. 清洗所有原始文本列
    df = clean_all_text_columns(df)

    # 2. 拆分 title
    split_titles = df['title'].str.split('/', expand=True)
    df['cn_title'] = split_titles[0].str.strip()
    df['en_title'] = split_titles.iloc[:, -1].str.strip()
    df['cn_title'] = df['cn_title'].apply(clean_text)
    df['en_title'] = df['en_title'].apply(clean_text)
    df.loc[df['en_title'] == df['cn_title'], 'en_title'] = ''

    # 3. original_title
    df['original_title'] = df['original_title'].fillna('')
    split_orig = df['original_title'].str.split('/', expand=True)
    df['original_title_clean'] = split_orig.iloc[:, -1].str.strip()
    df['original_title_clean'] = df['original_title_clean'].apply(clean_text)

    # 4. 过滤评分和评分人数
    df = df[df['rating'] >= MIN_RATING]
    df = df[df['num_ratings'] >= MIN_RATINGS]

    # 5. 去重
    df = df.sort_values(by=['rating', 'num_ratings'], ascending=[False, False])
    df = df.drop_duplicates(subset=['title'], keep='first')
    # 重置行号
    df = df.reset_index(drop=True)

    # -------- 转换 ----------
    # 1. 统一年份（只保留四位数字）
    df['year'] = df['year'].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df['year'] = df['year'].str[:4]
    df.loc[df['year'].str.len() < 4, 'year'] = ''

    # 2. 提取类型
    df['genre'] = df.apply(extract_genre, axis=1)

    # 3. 评分保留1位小数
    df['rating'] = df['rating'].round(1)

    # -------- 集成（添加 region 列） ----------
    df['region'] = df['country'].apply(assign_region)

    # 检测是否还有 NBSP（调试用）
    for col in df.select_dtypes(include=['object']).columns:
        mask = df[col].astype(str).str.contains('\u00A0', na=False)
        if mask.any():
            print(f"警告：列 {col} 仍有 NBSP，示例：{df.loc[mask, col].iloc[0][:50]}")

    # 调整列顺序（加入 region）
    pref = ['cn_title', 'en_title', 'original_title_clean', 'year', 'country',
            'region', 'genre', 'rating', 'num_ratings', 'quote', 'tail', 'info_text']
    existing = [c for c in pref if c in df.columns]
    others = [c for c in df.columns if c not in existing]
    df = df[existing + others]

    # 保存
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False, encoding='utf-8-sig')
    print(f"清洗转换集成完成，保留 {len(df)} 条记录，保存至 {CLEAN_PATH}")
    # 打印各区域数量统计
    print("\n各区域电影数量：")
    print(df['region'].value_counts())

if __name__ == "__main__":
    main()