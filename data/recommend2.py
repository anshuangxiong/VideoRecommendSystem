from collections import defaultdict
import math
import operator

"""
data_path = "data/ratings.csv"
sep = ","
fp = open(data_path, "r")
user2item_matrix = defaultdict(defaultdict) # 用户到物品的评分矩阵
item2user_matrix = defaultdict(defaultdict) # 物品到用户的倒排评分矩阵
# UserID \t MovieID \t Score \t Time
for line in open(data_path):
    lines = line.strip().split(sep)
    userID, movieID, score = lines[0],lines[1],lines[2]
    user2item_matrix[userID][movieID] = float(score)
    item2user_matrix[movieID][userID] = float(score)
fp.close()
"""


def read_data(data_path, sep):
    fp = open(data_path, "r")
    user2item_matrix = defaultdict(defaultdict)  # 用户到物品的评分矩阵
    item2user_matrix = defaultdict(defaultdict)  # 物品到用户的倒排评分矩阵
    # UserID \t MovieID \t Score \t Time
    for line in open(data_path):
        lines = line.strip().split(sep)
        userID, movieID, score = lines[0], lines[1], lines[2]
        user2item_matrix[userID][movieID] = float(score)
        item2user_matrix[movieID][userID] = float(score)
    fp.close()
    print("totol users:", len(user2item_matrix))  # 一维矩阵的长度为用户的数量
    print("totol items:", len(item2user_matrix))  # 一维矩阵的长度为物品的数量
    return user2item_matrix, item2user_matrix


def user_sim_cosine(user2item_matrix):
    W = defaultdict(defaultdict)  # 用户-用户-相似度矩阵
    user_list = user2item_matrix.keys()
    for i in user_list:
        for j in user_list:
            if i == j:
                continue
            W[i][j] = len(set(user2item_matrix[i].keys()) & set(user2item_matrix[j].keys())) # 交集
            W[i][j] /= math.sqrt(len(user2item_matrix[i].keys())*len(user2item_matrix[j].keys())*1.0)


    """
   
    """
    f = open('user.txt', 'w')
    for i in W:
        for j in W:
            if i == j:
                continue
            f.write("("+i+","+j+")    "+str(W[str(i)][str(j)])+"\n")
    f.close()
    print(W['1'])
    print(W['1']['2'])
    print(W['1'].items())
    return W

# W = user_sim_cosine(user2item_matrix)


def recommend(user2item_matrix, user_id, W, K=10):
    '''通过用户userid、训练集数据、用户相似度矩阵进行topN推荐'''
    rank=defaultdict(int)
    # 获取用户的物品列表
    user_item_set = user2item_matrix[user_id].keys()
    # 遍历与该user_id相似的用户和相似度得分
    for w_userid,w_score in sorted(W[user_id].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
        # 遍历相似用户看过的物品与打分
        for item_id,item_score in user2item_matrix[w_userid].items():
            # 如果相似用户看过的电影也在目标用户的物品集合中，则忽略该物品的推荐
            if item_id in user_item_set:
                continue
            # 计算该物品推荐给用户的排序分  用户的相似度*评分
            rank[item_id] = w_score*item_score
    # 对所有推荐物品与打分按照排序分进行降序排序，取前K个物品
    rank_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:K]
    return rank_list

# print (recommend(user2item_matrix,'1',W))


if __name__ == "__main__":
    data_path = "data/ratings.csv"
    sep = ","
    user2item_matrix, item2user_matrix = read_data(data_path, sep)
    W = user_sim_cosine(user2item_matrix)
    userId = input("请输入推荐的用户: ")
    recommendNum = input("请输入给用户"+userId+"推荐的数量: ")
    rank_list = recommend(user2item_matrix, str(userId), W, int(recommendNum))
    print(rank_list)


"""
    用户相似度  
    物品相似度   给定用户  根据用户的的物品找到与该物品相似度最高的物品
    
"""