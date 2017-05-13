# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
from operator import itemgetter

import Knapsack

# シード値を設定(再現させるため)
random.seed(33)
# 商品の数
Knapsack.N = 10
# ナップサックの入れられる重さ
Knapsack.MAX_weight = 250
# 個体をKnapsack.MAX_biontだけ生成する
Knapsack.MAX_biont = 10
# エリート保存数
Knapsack.MAX_elite = 1

# Knapsack.WeightandValue:クラスのための実データ
Knapsack.WeightandValue = Knapsack.make_randdata(Knapsack.N)
print("Knapsack.WeightandValue")
print(Knapsack.WeightandValue)
print("最適解:{0}".format(Knapsack.rec_dp(0, Knapsack.MAX_weight, Knapsack.dp, Knapsack.WeightandValue)))

# オブジェクト生成(個体をKnapsack.MAX_biontだけ生成)
bionts = []
for i in range(Knapsack.MAX_biont) :
    bionts.append(Knapsack.Genetic_Biont(Knapsack.WeightandValue, Knapsack.MAX_weight))
    bionts[i].showinfo()

# 価値が最大のものを抽出しエリート保存戦略する
# ここでは上位二個
elite = []
elite.extend(Knapsack.extract_elite(bionts, Knapsack.MAX_elite))
print(elite)

# generation:世代交代回数
generation = 1000
print("generation:{0}".format(generation))
for i in range(generation) :
    Knapsack.somepoints_crossover(Knapsack.roulette_choice(bionts), start_point=random.randint(0, Knapsack.MAX_biont-1), end_point=random.randint(0, Knapsack.MAX_biont-1))
    for j in bionts :
        # 5%で突然変異
        j.mutation(0.03)

for i in range(Knapsack.MAX_biont) :
    bionts[i].updateinfo()
    bionts[i].showinfo()

print("elite")
elite.extend(Knapsack.extract_elite(copy.copy(bionts), Knapsack.MAX_elite))
print(elite)
for i in elite :
    i.updateinfo()
    i.showinfo()
