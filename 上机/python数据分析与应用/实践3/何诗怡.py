import numpy as np
import pandas as pd

df=pd.read_csv('新能源汽车销售数据.csv')
print(df)

deal_number = df['成交商品件数/件'].to_numpy()
deal_money= df['成交金额/元'].to_numpy()

print("========成交商品件数统计========")
print(f"均值: {np.mean(deal_number)}")
print(f"标准差: {np.std(deal_number)}")
print(f"最小值: {np.min(deal_number)}")
print(f"最大值: {np.max(deal_number)}")

print("\n========成交金额统计========")
print(f"均值: {np.mean(deal_money)}")
print(f"标准差: {np.std(deal_money)}")
print(f"最小值: {np.min(deal_money)}")
print(f"最大值: {np.max(deal_money)}")

df['单件平均成交金额/元'] = np.where(deal_number == 0, np.nan, deal_money / deal_number)

df['加购率'] = df['加购商品件数/件'] / df['访客数/人']
df['下单率'] = df['下单客户数/人'] / df['访客数/人']
df['成交率'] = df['成交客户数/人'] / df['访客数/人']

print("\n====加购率、下单率、成交率描述统计====")
print(df[['加购率','下单率','成交率']].describe())

df['最近上架时间'] = pd.to_datetime(df['最近上架时间'])
df['上架月份'] = df['最近上架时间'].dt.month

group_result = df.groupby('上架月份')[['加购率','下单率','成交率']].mean()
print("\n====按上架月份分组均值====")
print(group_result)

df.to_csv('新能源汽车销售数据_经过项目3处理.csv', index=False, encoding='utf-8-sig')
print("\n✅ 文件保存完成")
