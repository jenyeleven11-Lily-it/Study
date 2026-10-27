# %% [markdown]
# # 上机2  pandas数据分析与处理
# 学号：20241123035　　姓名：何诗怡　　班级：2401班
#
# 本实验完成6项任务：房屋销售数据的读取与索引、时间格式转换与价格统计、分组聚合，以及中风患者数据的合并、异常值删除与年龄离散化。

# %%
# ============ 环境准备 ============
import glob
import os
import numpy as np
import pandas as pd


def find_file(pattern):
    # 在当前位置或一级子目录中查找数据文件
    for path in glob.glob(pattern) + glob.glob('*/' + pattern):
        if os.path.exists(path):
            return path
    raise FileNotFoundError('未找到文件：' + pattern)


# 数据文件路径（自动定位，无需手动修改）
HOUSE_CSV = find_file('*房屋销售数据*.csv')
STROKE_XLSX = find_file('*stroke*.xlsx')
AGE_XLSX = find_file('*age_abs*.xlsx')
print('房屋数据：', HOUSE_CSV)
print('中风数据：', STROKE_XLSX)
print('年龄血糖：', AGE_XLSX)

# %% [markdown]
# ## 任务1  读取并查看某地区房屋销售数据的基本信息

# %%
# （1）使用 read_csv 读取房屋销售数据
# 说明：原始文件表头已损坏（显示为?），故用 names 显式指定中文列名，
#       并设置 header=0 跳过被损坏的首行表头。
housesale = pd.read_csv(HOUSE_CSV, encoding='utf-8', header=0,
                        names=['房屋售出时间', '地区邮编', '房屋价格', '房屋类型', '配套房间数'])
print(housesale.head())

# %%
# （2）查看数据的维度、形状和所有特征名称
print('数据的维度 ndim =', housesale.ndim)
print('数据的形状 shape =', housesale.shape)
print('所有特征名称 columns =', list(housesale.columns))

# %%
# （3）使用 loc 与 iloc 对单身公寓(unit)的数据进行索引
unit_loc = housesale.loc[housesale['房屋类型'] == 'unit']
print('loc 标签索引（前5行）：')
print(unit_loc.head())

unit_pos = housesale.index[housesale['房屋类型'] == 'unit'][:5]
print('iloc 位置索引（前5行）：')
print(housesale.iloc[unit_pos])

print('房屋类型分布：')
print(housesale['房屋类型'].value_counts())

# %% [markdown]
# ## 任务2  提取房屋售出时间信息并描述房屋价格信息

# %%
# （1）使用 to_datetime 转换房屋售出时间字符串
housesale['房屋售出时间'] = pd.to_datetime(housesale['房屋售出时间'])
# 转换为 2010-1-4 这种年-月-日（不补零）的形式
housesale['售出日期'] = housesale['房屋售出时间'].apply(
    lambda d: str(d.year) + '-' + str(d.month) + '-' + str(d.day))
print(housesale[['房屋售出时间', '售出日期']].head())

# %%
# （2）使用 mean、max、min 计算房屋价格的均值、最大值和最小值
price = housesale['房屋价格']
print('房屋价格均值 =', price.mean())
print('房屋价格最大值 =', price.max())
print('房屋价格最小值 =', price.min())

# %%
# （3）使用 describe() 计算房屋价格的统计量
print(housesale['房屋价格'].describe())

# %% [markdown]
# ## 任务3  使用分组聚合方法分析房屋销售情况
# 目标：提取地区邮编前两位生成 new_postcode 特征，并据此统计、比较不同地区的房屋价格。

# %%
# （1）使用 apply() 生成 new_postcode 特征（取邮编前两位）
housesale['地区邮编'] = housesale['地区邮编'].astype(str)
housesale['new_postcode'] = housesale['地区邮编'].apply(lambda x: x[:2])
print(housesale[['地区邮编', 'new_postcode']].head())

# %%
# （2）使用 agg() 方法和 count 函数计算每个地区的房屋售出总数
count_by_area = housesale.groupby('new_postcode')['房屋价格'].agg(['count'])
print('各地区房屋售出总数：')
print(count_by_area)

# %%
# （3）使用 groupby() 按房屋类型 propertyType 和 new_postcode 分组，赋值给 housesale1
housesale1 = housesale.groupby(['房屋类型', 'new_postcode'])
print('分组后的对象：', housesale1)

# %%
# （4）使用 transform() 聚合方法和 mean 函数计算 housesale1 中房屋价格的均值
housesale['均价'] = housesale1['房屋价格'].transform('mean')
print('分组内房屋价格均值（前5行）：')
print(housesale[['房屋类型', 'new_postcode', '房屋价格', '均价']].head())

# %% [markdown]
# ## 任务4  合并年龄、平均血糖和中风患者信息数据

# %%
# （1）利用 read_excel 读取中风患者基础信息和体检数据
stroke = pd.read_excel(STROKE_XLSX)
print('中风患者基础信息维度：', stroke.shape)
print(stroke.head())

# %%
# （2）利用 read_excel 读取年龄和平均血糖数据
age_abs = pd.read_excel(AGE_XLSX)
print('年龄血糖数据维度：', age_abs.shape)
print(age_abs.head())

# %%
# （3）查看两表的数据量
print('中风患者数据量：', stroke.shape[0], '行 ', stroke.shape[1], '列')
print('年龄血糖数据量：', age_abs.shape[0], '行 ', age_abs.shape[1], '列')

# %%
# （4）以编号作为主键进行外连接（merge, how=outer）
data = pd.merge(stroke, age_abs, on='编号', how='outer')
print('合并后数据维度：', data.shape)
print('合并后数据列名：', list(data.columns))

# %%
# （5）查看数据是否合并成功
print('合并后是否有缺失值（每列缺失数）：')
print(data.isnull().sum())
print('合并后前5行：')
print(data.head())

# %% [markdown]
# ## 任务5  删除年龄异常的数据
# 观察发现年龄特征中存在小数（如1.8）这类异常值，需要将其删除。

# %%
# （1）获取年龄特征
age_col = [c for c in data.columns if str(c).startswith('年龄')][0]
print('年龄特征名称：', age_col)
age = data[age_col]
print(age.describe())

# %%
# （2）使用for循环获取年龄数值，并用if-else判断是否为异常值
# 判定规则：年龄不应为小数，若取整后与原值不相等，即为异常值。
anomaly_idx = []
for i in age.index:
    val = age[i]
    if pd.notnull(val) and val % 1 == 0:
        pass                 # 正常值，保留
    else:
        anomaly_idx.append(i)   # 小数或缺失值，记为异常
print('检测到异常值行数：', len(anomaly_idx))
print('异常值样例：', age.loc[anomaly_idx].head().to_dict())

# %%
# （3）删除年龄异常值所在的行
data = data.drop(index=anomaly_idx).reset_index(drop=True)
print('删除后数据维度：', data.shape)
print('删除后年龄最小值：', data[age_col].min())
print('删除后是否仍存在小数年龄：', bool((data[age_col] % 1 != 0).any()))

# %% [markdown]
# ## 任务6  离散化年龄特征
# 分类算法要求数据离散，使用等宽法将连续的年龄特征离散化。

# %%
# （1）获取年龄特征
age_clean = data[age_col]
print('年龄区间：', age_clean.min(), '~', age_clean.max())
print(age_clean.describe())

# %%
# （2）使用等宽法对年龄进行离散化
# 等宽法：区间宽度 = (最大值 - 最小值) / 区间个数，本例划分为5个等宽区间。
k = 5
amin, amax = age_clean.min(), age_clean.max()
width = (amax - amin) / k
bins = [amin + i * width for i in range(k + 1)]   # 生成6个边界，形成5个区间
print('区间宽度：', width)
print('分箱边界：', bins)

data['年龄区间'] = pd.cut(age_clean, bins=bins, right=False)
print('等宽离散化后的年龄分布：')
print(data['年龄区间'].value_counts().sort_index())

# %%
# 将离散化结果整理为“区间 + 人数”的表格，便于报告展示
age_discrete = data['年龄区间'].value_counts().sort_index().rename_axis('年龄区间').reset_index(name='人数')
print(age_discrete)
