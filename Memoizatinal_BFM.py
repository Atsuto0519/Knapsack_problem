# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt

import Knapsack

# シード値を設定(再現させるため)
random.seed(151)

# 商品の数
Knapsack.N = 10
# ナップサックの入れられる重さ
Knapsack.MAX_weight = 10

# WeightandValue[i][0]:i番目商品の重さ
# WeightandValue[i][1]:i番目商品の価値
Knapsack.WeightandValue = Knapsack.make_randdata(Knapsack.N)
Knapsack.w = []
for i in Knapsack.WeightandValue :
    Knapsack.w.append(i[0])

# Wの最大値
Knapsack.MAX_W = sum(Knapsack.w)

# メモ化テーブル。
# dp[i][j]はi番目以降の品物から重さの和がj以下なるように選んだときの価値の和の最大値を表す。
# -1なら値が未決定であることを表す
Knapsack.dp = np.zeros([Knapsack.N+1,Knapsack.MAX_W+1])
for i in range(Knapsack.N+1) :
    for j in range(Knapsack.MAX_W+1) :
        Knapsack.dp[i][j] = -1

print("WeightandValue")
print(Knapsack.WeightandValue)
print(Knapsack.rec_dp(0, Knapsack.MAX_weight, Knapsack.dp, Knapsack.WeightandValue))
