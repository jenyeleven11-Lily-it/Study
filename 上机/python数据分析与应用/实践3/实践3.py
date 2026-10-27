import pandas as pd

# ---------- 1. 读取数据 ----------
df = pd.read_csv("新能源汽车销售分析结果_20250610_204619.csv", encoding="utf-8-sig")

print("读取成功，数据形状：", df.shape)
print("原始数据前3行：")
print(df.head(3))
print(df.shape)
# ---------- 2. 处理重复值 ----------
df.drop_duplicates(inplace=True)
print("\n去重后数据形状：", df.shape)

# ---------- 3. 计算成交金额的分位数 ----------
col = "成交金额/元"

df[col] = pd.to_numeric(df[col], errors="coerce")
# 【重点】过滤成交金额等于0的行，0不是有效成交，避免分位数扎堆0
df = df[(df[col] > 0) & (df[col].notna())]

min_val = df[col].min()          # 最小值
q33 = df[col].quantile(0.33)     # 33% 分位数
q66 = df[col].quantile(0.66)     # 66% 分位数
max_val = df[col].max()          # 最大值

print(f"\n成交金额统计（已剔除金额=0）：")
print(f"最小值  : {min_val:.2f}")
print(f"33%分位 : {q33:.2f}")
print(f"66%分位 : {q66:.2f}")
print(f"最大值  : {max_val:.2f}")

# ---------- 4. 用 cut 离散化为低/中/高 3 个等级 ----------
df["成交金额等级"] = pd.cut(
    df[col],
    bins=[min_val, q33, q66, max_val],
    labels=["低", "中", "高"],
    include_lowest=True
)

print("\n等级分布：")
print(df["成交金额等级"].value_counts())

# ---------- 5. 保存结果 ----------
df.to_csv("新能源汽车销售数据_经过项目4处理.csv", index=False, encoding="utf-8-sig")
print("\n已保存：新能源汽车销售数据_经过项目4处理.csv")
