# -*- coding: utf-8 -*-
"""
上机3 任务4：绘制交互式基础图形（漏斗图 + 词云图）
数据：某商场5台自动售货机(A/B/C/D/E) 2023年6月商品销售数据（商品销售数据.csv）
功能：
    1) 读取“商品销售数据.csv”文件
    2) 按照二级类别统计商品类别销售额
    3) 设置系列配置项和全局配置项，绘制销售额前5的商品类别漏斗图
    4) 统计商品销售数量
    5) 设置系列配置项和全局配置项，绘制商品销售数量和商品名称的词云图
"""
import os
import pandas as pd
from pyecharts.charts import Funnel, WordCloud
from pyecharts import options as opts

# 自动切换到脚本所在目录，保证相对路径读取数据文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------- (1) 读取“商品销售数据.csv”文件（UTF-8 with BOM） ----------
df = pd.read_csv('商品销售数据.csv', encoding='utf-8-sig')
print('数据形状:', df.shape)
print(df.head())

# ---------- (2) 按照二级类别统计商品类别销售额（按实际金额求和） ----------
sales = df.groupby('二级类')['实际金额'].sum().sort_values(ascending=False)
print('各二级类别销售额前8:')
print(sales.head(8))

# ---------- (3) 绘制销售额前5的商品类别漏斗图 ----------
top5 = sales.head(5)
funnel_data = [[str(k), round(float(v), 2)] for k, v in top5.items()]
funnel = (
    Funnel(init_opts=opts.InitOpts(width='900px', height='600px'))
    .add(
        '商品类别销售额',
        funnel_data,
        label_opts=opts.LabelOpts(position='inside', formatter='{b}: {c}'),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='销售额前5的商品类别漏斗图'),
        legend_opts=opts.LegendOpts(pos_left='5%', pos_bottom='10%'),
    )
)
funnel.render('task4_销售额前5漏斗图.html')
print('已生成: task4_销售额前5漏斗图.html')

# ---------- (4) 统计商品销售数量（按商品名称统计销售笔数） ----------
counts = df.groupby('商品')['订单号'].count().sort_values(ascending=False)
print('销售数量前5:')
print(counts.head())

# ---------- (5) 绘制商品销售数量和商品名称的词云图 ----------
wc_data = [[str(k), int(v)] for k, v in counts.items()]
wordcloud = (
    WordCloud(init_opts=opts.InitOpts(width='900px', height='600px'))
    .add(
        '',
        wc_data,
        word_size_range=[12, 60],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='商品销售数量词云图'),
    )
)
wordcloud.render('task4_商品销售数量词云图.html')
print('已生成: task4_商品销售数量词云图.html')
