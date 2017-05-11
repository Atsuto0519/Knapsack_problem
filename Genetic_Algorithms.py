# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
from operator import itemgetter


def getNearestValue(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]

def extract_elite(bionts, num_elite=-1) :
    """エリート保存戦略関数
    上位num_eliteまでをエリートとして返す．
    """
    # エリート保存数がおかしければ個体数に依存
    if (num_elite<1) :
        num_elite = len(bionts)

    tmp = []
    elite = []
    for i in bionts :
        tmp.append(i.value)

    for i in range(num_elite) :
        elite.append(bionts[tmp.index(max(tmp))].gene)
        tmp.remove(max(tmp))
    return elite

def make_randdata(MIN_data=1, MAX_data=100, N=0) :
    """適当にランダムデータを生成する．
    MIN_data --- 乱数の最小値
    MAX_data --- 乱数の最大値
    N --- 遺伝子数
    """
    # 遺伝子数がおかしければデフォルトで10
    if (N<1) :
        N = 10
    # クラスのためのベクトル生成
    WeightandValue = []
    while (len(WeightandValue) < N) :
        WeightandValue.append([random.randint(MIN_data,MAX_data), random.randint(MIN_data,MAX_data)])
    return WeightandValue

def somepoints_crossover(twin_bionts, *, start_point=0, end_point=0) :
    """somepoints_crossover():一点交叉する関数
    第一引数:twin_bionts
    第二引数:start_point（要素数）
    第三引数:end_point  (要素数)
    """
    gene_xx = twin_bionts[0].gene
    gene_yy = twin_bionts[1].gene
    len_gene_xx = len(gene_xx)
    # 交叉点がおかしければ遺伝子の中間
    if (start_point<1 or end_point<2) :
        start_point = 0
        end_point = len_gene_xx/2-1
    # 遺伝子数が異なる場合は交叉しない
    if (len_gene_xx == len(gene_yy)) :
        start_point = int(start_point)
        end_point = int(end_point+1)
        gene_xy = []
        gene_yx = []
        gene_xy.extend(gene_yy[0:start_point].copy())
        gene_xy.extend(gene_xx[start_point:end_point].copy())
        gene_xy.extend(gene_yy[end_point:len_gene_xx].copy())

        gene_yx.extend(gene_xx[0:start_point].copy())
        gene_yx.extend(gene_yy[start_point:end_point].copy())
        gene_yx.extend(gene_xx[end_point:len_gene_xx].copy())

        # もし子がナップサックの容量を超えていなかったら
        if (np.dot(gene_xy, twin_bionts[0].WeightandValue)[0] <= MAX_weight) :
            for i in range(len_gene_xx) :
                twin_bionts[0].gene[i] = gene_xy[i]
        if (np.dot(gene_yx, twin_bionts[0].WeightandValue)[0] <= MAX_weight) :
            for i in range(len_gene_xx) :
                twin_bionts[1].gene[i] = gene_yx[i]

def roulette_choice(bionts, MIN_data=1, MAX_data=100) :
    """ルーレット選択を行う関数
    第一引数:bions
    """
    f_all = []
    # 適合度割合を求める
    for i in bionts :
        f_all.append(i.value)
    p_all = []
    for i in bionts :
        i.raito = i.value / (sum(f_all) * i.weight)
        p_all.append(i.raito)

    # 二対の個体をルーレット選択
    twin_bionts = []
    nearest_value = p_all[random.randint(0, len(p_all)-1)]
    for i in range(2) :
        # ルーレットを回す
        rand_raito = random.random()
        # すでに選ばれたものが出た場合は出なくなるまで回す
        while (nearest_value == getNearestValue(p_all, rand_raito)) :
            # ルーレットを回す
            rand_raito = random.random()
        # 回した値に最も近い値をリストから取る
        nearest_value = getNearestValue(p_all, rand_raito)
        nearest_index = p_all.index(nearest_value)

        # 遺伝子を選択
        twin_bionts.append(bionts[p_all.index(nearest_value)])

    return twin_bionts

# def ranking_choice() :

class Genetic_Biont :
    """遺伝的アルゴリズムのためのクラス
    WeightandValue --- [[重み, 価値], ...]
    MAX_weight --- ナップサックの重さ容量
    N --- 遺伝子数

    メソッド内関数一覧
    showinfo():オブジェクトの情報を表示
    updateinfo():スコア情報を更新
    """
    # コンストラクタ
    def __init__(self, WeightandValue, MAX_weight ,N=0) :
        # 遺伝子を生成
        self.gene = []
        self.weight = 0
        self.WeightandValue = WeightandValue.copy()
        # 遺伝子数がおかしければ実データに依存
        if (N<1) :
            N = len(WeightandValue)
        for j in range(N) :
            self.gene.append(random.randint(0,1))
            if (self.gene[j]==1) :
                # 入れる商品の重さがナップサックに入るなら入れる
                if (self.weight+WeightandValue[j][0] <= MAX_weight) :
                    self.weight += WeightandValue[j][0]
                # 入らなければ遺伝子を操作
                else :
                    self.gene[j] = 0
        self.updateinfo()

    def showinfo(self) :
        print("gene:{0}, weight:{1}, value:{2}".format(self.gene, self.weight, self.value))

    def updateinfo(self) :
        tmp = np.dot(self.gene, self.WeightandValue)
        self.weight = tmp[0]
        self.value  = tmp[1]


# シード値を設定(再現させるため)
random.seed(7)
# 商品の数
N = 10
# ナップサックの入れられる重さ
MAX_weight = 200
# 個体をMAX_biontだけ生成する
MAX_biont = 10
# エリート保存数
MAX_elite = 2

# WeightandValue:クラスのための実データ
WeightandValue = make_randdata()
print("WeightandValue")
print(WeightandValue)
# オブジェクト生成(個体をMAX_biontだけ生成)
bionts = []
for i in range(MAX_biont) :
    bionts.append(Genetic_Biont(WeightandValue, MAX_weight))
    bionts[i].showinfo()

# 価値が最大のものを抽出しエリート保存戦略する
# ここでは上位二個
elite = extract_elite(bionts, MAX_elite)
# 世代交代generation回
generation = 1000
print("generation:{0}".format(generation))
for i in range(generation) :
    somepoints_crossover(roulette_choice(bionts), start_point=3, end_point=6)
#    elite.append(extract_elite(bionts, MAX_elite))

for i in range(MAX_biont) :
    bionts[i].updateinfo()
    bionts[i].showinfo()

#print("elite")
#print(elite)
