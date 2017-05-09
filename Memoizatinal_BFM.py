# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt

# メモ化再起による全探索関数
# i番目以降の品物から重さの和がj以下なるように選んだときの、
# 取りうる価値の総和の最大値を返す関数
def rec_dp(i, j):
    # 既にメモ化によって探索された後ならその結果を
    # 探索されていないなら探索した結果を返す
    if (dp[i][j] == -1) :
        if (i == N) :
            # 品物がもう残っていないときは、価値の和の最大値は0で確定
            dp[i][j] = 0
        elif (j < w[i]) :
            # 残りの容量が足りず品物iを入れられないので、入れないパターンだけ処理
            # i+1 以降の品物のみを使ったときの最大値をそのままこの場合の最大値にする
            dp[i][j] = rec_dp(i + 1, j)
        else :
            # 品物iを入れるか入れないか選べるので、両方試して価値の和が大きい方を選ぶ
            dp[i][j] = max(rec_dp(i + 1, j), rec_dp(i + 1, j - w[i]) + v[i])

    return dp[i][j]


# シード値を設定(再現させるため)
random.seed(0)

# 商品の数
N = 10
# ナップサックの入れられる重さ
W = 300

# w[i]:i番目商品の重さ
# v[i]:i番目商品の価値
# item:ナップサックに入れた価値リスト
w = []
v = []
# w,vを1~100のランダムに設定
for i in range(N) :
    w.append(random.randint(1,100))
    v.append(random.randint(1,100))

# Wの最大値
MAX_W = sum(w)

# メモ化テーブル。
# dp[i][j]はi番目以降の品物から重さの和がj以下なるように選んだときの価値の和の最大値を表す。
# -1なら値が未決定であることを表す
dp = np.zeros([N+1,MAX_W+1])
for i in range(N+1) :
    for j in range(MAX_W+1) :
        dp[i][j] = -1


print("w")
print(w)
print("MAX_W")
print(MAX_W)
print("v")
print(v)
print(rec_dp(0, W))
