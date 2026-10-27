import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd
import os
# 配置
BASE_URL = "https://movie.douban.com/top250"#爬取地址
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
SAVE_PATH = "D:Studywork/douBan/result/raw/douban_top250_2026.csv"

# 自动创建保存文件夹
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)#在当前.py文件创建文件夹
def parse_movie_item(item):
    """解析单个电影条目"""
    title_spans = item.select("div.hd span.title")
    titles = [s.get_text(strip=True) for s in title_spans]
    title = " / ".join(titles)

    other = item.select_one("div.hd span.other")
    original_title = other.get_text(strip=True) if other else ""

    info_p = item.select_one("div.bd p")
    info_text = ""
    if info_p:
        info_text = info_p.get_text(separator=" ").strip()
        info_text = re.sub(r"\s+", " ", info_text)

    year_match = re.search(r"(\d{4})", info_text)
    year = year_match.group(1) if year_match else ""

    tail = ""
    try:
        parts = [p.strip() for p in info_p.get_text(separator=" ").strip().split(" ")]
        year_idx = next((i for i, p in enumerate(parts) if re.search(r"\d{4}", p)), -1)
        if year_idx != -1 and year_idx + 1 < len(parts):
            country = parts[year_idx + 1]
        else:
            country = ""
    except Exception:
        country = ""
    try:
        parts = [p.strip() for p in info_text.split('/') if p.strip()]
        idx = next((i for i, p in enumerate(parts) if re.search(r"\d{4}", p)), None)
        if idx is not None:
            tail = " / ".join(parts[idx + 1:])
    except Exception:
        tail = ""

    try:
        rating = item.select_one("span.rating_num").get_text(strip=True)
    except AttributeError:
        rating = ""

    try:
        spans = item.select("div.bd div > span")
        num_ratings = ""
        for sp in spans:
            text = sp.get_text(strip=True)
            if "人评价" in text:
                num_ratings = re.search(r"([\d,]+)", text).group(1).replace(",", "")
                break
    except Exception:
        num_ratings = ""

    try:
        quote = item.select_one("p.quote span").get_text(strip=True)
    except AttributeError:
        quote = ""

    return {
        "title": title,
        "original_title": original_title,
        "info_text": info_text,
        "year": year,
        "country": country,
        "tail": tail,
        "rating": rating,
        "num_ratings": num_ratings,
        "quote": quote
    }

def fetch_static_top250():
    """一次性抓取最新静态榜单"""
    all_movies = []
    print("正在抓取2026最新豆瓣Top250榜单...")
    for start in range(0, 250, 25):
        params = {"start": start}
        print(f"正在抓取第 {int(start/25)+1} 页")
        try:
            resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"第{int(start/25)+1}页请求失败: {e}")
            time.sleep(5)
            continue

        # 使用Python自带解析器，无需lxml
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("div.item")
        if not items:
            print("未获取到电影数据，页面可能被拦截")
            break

        for it in items:
            data = parse_movie_item(it)
            all_movies.append(data)

        time.sleep(random.uniform(1.0, 2.5))

    # 整理数据类型
    df = pd.DataFrame(all_movies)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["num_ratings"] = pd.to_numeric(df["num_ratings"], errors="coerce")

    # 保存为CSV
    df.to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")
    print(f"\n抓取完成！共获取{len(df)}条电影数据")
    print(f"数据已保存至: {SAVE_PATH}")
    return df

if __name__ == "__main__":
    fetch_static_top250()