# lottery.py
import random

def draw_lottery():
    # 定義獎項和對應的概率
    prizes = ['大吉', '吉', '中吉', '小吉', '半吉', '末吉', '末小吉']
    probabilities = [0.12, 0.23, 0.18, 0.13, 0.08, 0.1, 0.06]  # 對應大吉，吉，中吉，小吉，半吉，末吉，末小吉的概率

    # 使用 random.choices 來根據概率抽取獎項
    result = random.choices(prizes, probabilities)[0]  # 選擇一個獎項
    
    return result
