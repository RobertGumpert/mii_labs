import numpy as np
import matplotlib.pyplot as plt
import random

universal_set = list()
fuzzy_sets = dict(
    name_example=dict(
        a=0,
        b=1,
        c=2,
        d=3
    )
)


def exist_number(num):
    return universal_set[0] <= num <= universal_set[-1]


def trapezoid_function_accessories(fuzzy_set_name, x):
    if not exist_number(x):
        raise Exception("Объект не лежит в пределах универсального множества")
    if fuzzy_set_name not in fuzzy_set_name:
        raise Exception("Множество не определенно")
    fuzzy_set = fuzzy_sets[fuzzy_set_name]
    if fuzzy_set['a'] <= x <= fuzzy_set['b']:
        fraction = (x - fuzzy_set['a']) / (fuzzy_set['b'] - fuzzy_set['a'])
        return fraction
    if fuzzy_set['b'] <= x <= fuzzy_set['c']:
        return 1
    if fuzzy_set['c'] <= x <= fuzzy_set['d']:
        fraction = (fuzzy_set['d'] - x) / (fuzzy_set['d'] - fuzzy_set['c'])
        return fraction
    if fuzzy_set['d'] < x or fuzzy_set['a'] > x:
        return 0
    raise Exception("Не удв. системе")


def trapezoid_show_plot():
    plt.ylim(0, 1)
    plt.xlim(universal_set[0], universal_set[-1])
    for set_name in fuzzy_sets:
        if set_name == "name_example":
            continue
        plt.plot([fuzzy_sets[set_name]['a'], fuzzy_sets[set_name]['b'], fuzzy_sets[set_name]['c'],
                  fuzzy_sets[set_name]['d'], fuzzy_sets[set_name]['a']], [0, 1, 1, 0, 0], label=set_name)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()


def trapezoid_set_object():
    print('\n\nВведите имя множества и объект: \n<- name:x')
    while True:
        input_val = input()
        if input_val == "end":
            print("->", input_val)
            break
        args = input_val.split(':')
        fuzzy_set_name = args[0]
        x = float(args[1])
        q = trapezoid_function_accessories(fuzzy_set_name, x)
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        plt.plot(x, q, 'ro', label=input_val, color=color)
        print("\t\t->Принадлежность объкта ", x, " множеству ", fuzzy_set_name, " = ", q * 100, "%")
    trapezoid_show_plot()


def trapezoid_add_sets():
    print("Добавить нечеткие множества: <- end")
    print("Границы нечеткого множества: \n<- name:a,b,c,d")
    while True:
        input_val = input()
        if input_val == "end":
            print("->", fuzzy_sets)
            break
        args = input_val.split(':')
        name = args[0]
        borders = args[1].split(',')
        a = float(borders[0])
        b = float(borders[1])
        c = float(borders[2])
        d = float(borders[3])
        if (not exist_number(a) or not exist_number(b) or not exist_number(c) or not exist_number(d)) or (
                d > c > b > a) == False or (
                name in fuzzy_sets):
            print("\t\t->Неправльные границы")
            continue
        fuzzy_sets[name] = dict(
            a=a,
            b=b,
            c=c,
            d=d
        )
        print("\t\t->", input_val, "\t\tСледующее множество:")
    trapezoid_show_plot()
    trapezoid_set_object()


if __name__ == "__main__":
    print("Границы универсального множества : \n<- x0,x1")
    us_range = input().split(',')
    universal_set = [i for i in np.arange(int(us_range[0]), int(us_range[1]), 0.1)]
    print("->", universal_set)
    trapezoid_add_sets()
