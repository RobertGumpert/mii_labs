import pprint
import random

import data
import trapezoid


def calc(scores, unknown_score):
    predict_score_index = data.base_rules[0].index(unknown_score)
    accessory_table = [[None for _ in range(len(scores.keys()))] for _ in range(len(data.base_rules))]
    j = 0
    for score, x in scores.items():
        accessory_table[0][j] = score
        index = data.base_rules[0].index(score)
        fuzzy_sets = [row[index] for row in data.base_rules][1:len(data.base_rules)]
        for i, fuzzy_set in enumerate(fuzzy_sets):
            predict = trapezoid.predict(data.fuzzy_scores[score][fuzzy_set], x)
            accessory_table[i + 1][j] = predict
        j += 1
    accessory_table[0].append("&")
    accessory_table[0].append("->")
    predict_accessory = 0.0
    mind = 0.0
    for i, _ in enumerate(data.base_rules):
        if i == 0:
            continue
        m = min(accessory_table[i])
        if m > predict_accessory:
            predict_accessory = m
            mind = i
        accessory_table[i].append(m)
        accessory_table[i].append(m)
    if predict_accessory == 0.0:
        print("Упс, агрегировать нечего...")
        pprint.pprint(accessory_table)
        return predict_accessory, 0, "?"
    predict_fuzzy = data.base_rules[mind][predict_score_index]
    predict_value = -1.0
    if predict_accessory == 1.0:
        b = data.fuzzy_scores[unknown_score_name][predict_fuzzy]["b"]
        c = data.fuzzy_scores[unknown_score_name][predict_fuzzy]["c"]
        predict_value = random.uniform(b, c)
    if (predict_accessory > 0.0) and (predict_accessory < 1.0):
        a = data.fuzzy_scores[unknown_score_name][predict_fuzzy]["a"]
        b = data.fuzzy_scores[unknown_score_name][predict_fuzzy]["b"]
        predict_value = (predict_accessory * (b - a)) + a
        if predict_value == 0.0:
            c = data.fuzzy_scores[unknown_score_name][predict_fuzzy]["c"]
            d = data.fuzzy_scores[unknown_score_name][predict_fuzzy]["d"]
            predict_value = (predict_accessory * (d - c)) + d
    pprint.pprint(accessory_table)
    return predict_accessory, predict_value, predict_fuzzy


# температура:17.0,ветер:26.0,осадки:?
#
if __name__ == "__main__":
    data.init()
    while True:
        print("Введите ком. -> ")

        input_value = input()
        if input_value == "end":
            break
        if input_value == "show":
            for score_name, fuzzy_score in data.fuzzy_scores.items():
                trapezoid.show_plot(score_name, fuzzy_score)
            continue
        unknown_score_count = input_value.count('?')
        if unknown_score_count != 1:
            print("Укажати правильное кол-во неизвестных")
            continue
        split = input_value.split(",")
        known_scores = dict()
        unknown_score_name = ""
        for args in split:
            pair = args.split(":")
            if pair[1] == "?":
                unknown_score_name = pair[0]
                continue
            known_scores[pair[0]] = float(pair[1])
        accessory, value, fuzzy = calc(known_scores, unknown_score_name)
        print(
            f"Логический предсказывает для '{unknown_score_name}' нечетку метку '{fuzzy}' "
            f"с принадлежностью {str(round(accessory, 2) * 100)}% и четким значением {str(round(value, 2))}")
