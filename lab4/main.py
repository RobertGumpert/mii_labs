import csv
import random
import numpy as np
import trapezoid
import triangular
import matplotlib.pyplot as plt

universal_set = list()
fuzzy_sets = dict()
scales = list()
fuzzy_colors = dict()
clear_time_series = list()


def init():
    global universal_set, fuzzy_sets, scales, fuzzy_colors
    scales = ["дешево", "терпимо", "дорого", "очень дорого"]
    for scale in scales:
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        fuzzy_colors[scale] = color
    #
    universal_set = list(np.arange(30, 95, 0.25))
    universal_set = [np.float64(x).item() for x in universal_set]
    #
    trapezoid_dict = dict()
    triangular_dict = dict()
    #
    trapezoid.add_rating_linguistic_scale(30.0, 35.0, 40.0, 50.0, "дешево", trapezoid_dict, universal_set)
    trapezoid.add_rating_linguistic_scale(40.0, 45.0, 50.0, 55.0, "терпимо", trapezoid_dict, universal_set)
    trapezoid.add_rating_linguistic_scale(50.0, 55.0, 60.0, 65.0, "дорого", trapezoid_dict, universal_set)
    trapezoid.add_rating_linguistic_scale(60.0, 65.0, 70.0, 75.0, "очень дорого", trapezoid_dict, universal_set)
    #
    triangular.add_rating_linguistic_scale(30.0, 40.0, 50.0, "дешево", triangular_dict, universal_set)
    triangular.add_rating_linguistic_scale(40.0, 47.5, 55.0, "терпимо", triangular_dict, universal_set)
    triangular.add_rating_linguistic_scale(50.0, 57.5, 65.0, "дорого", triangular_dict, universal_set)
    triangular.add_rating_linguistic_scale(60.0, 67.5, 75.0, "очень дорого", triangular_dict, universal_set)
    #
    fuzzy_sets["trapezoid"] = trapezoid_dict
    fuzzy_sets["triangular"] = triangular_dict
    return


# com:[show];args:[all]              - показать, все
# com:[show];args:[td]               - показать, трапеция
# com:[show];args:[tr]               - показать, треугольник
#
# com:[add];args[td,name,a,b,c,d]    - добавить для трапеции
# com:[add];args[tr,name,a,b,c]      - добавить для треугольник
#
# com:[update];args[td,name,a,b,c,d] - обновить для трапеции
# com:[update];args[tr,name,a,b,c]   - обновить для треугольник
#
# com:[predict];args:[tr,name,x]     - предсказать, треугольник
# com:[predict];args:[td,name,x]     - предсказать, трапеции
#
# Example:
#   com:[add];args:[td,много,70,75,80,85]
#   com:[update];args:[td,много,40,75,80,90]
#   com:[add];args:[tr,много,70,77.5,85]
#   com:[update];args:[tr,много,40,77.5,90]
#   com:[predict];args:[tr,много,49]
#   com:[predict];args:[td,много,49]
#
def input_parser(input_string):
    split = input_string.split(";")
    com = split[0].split(":")[1]
    if com == "[show]":
        args = split[1].split(":")[1].replace("[", "").replace("]", "")
        if args == "all":
            trapezoid.show_plot(fuzzy_sets=fuzzy_sets["trapezoid"], fuzzy_colors=fuzzy_colors,
                                universal_set=universal_set)
            triangular.show_plot(fuzzy_sets=fuzzy_sets["triangular"], fuzzy_colors=fuzzy_colors,
                                 universal_set=universal_set)
        if args == "td":
            trapezoid.show_plot(fuzzy_sets=fuzzy_sets["trapezoid"], fuzzy_colors=fuzzy_colors,
                                universal_set=universal_set)
        if args == "tr":
            triangular.show_plot(fuzzy_sets=fuzzy_sets["triangular"], fuzzy_colors=fuzzy_colors,
                                 universal_set=universal_set)
    if com == "[update]" or com == "[add]":
        args = split[1].split(":")[1].replace("[", "").replace("]", "").split(",")
        f = args[0]
        name = args[1]
        if com == "[update]":
            if f == "td":
                trapezoid.update_rating_linguistic_scale(
                    a=float(args[2]),
                    b=float(args[3]),
                    c=float(args[4]),
                    d=float(args[5]),
                    universal_set=universal_set,
                    fuzzy_sets=fuzzy_sets["trapezoid"],
                    name=name
                )
                trapezoid.show_plot(fuzzy_sets=fuzzy_sets["trapezoid"], fuzzy_colors=fuzzy_colors,
                                    universal_set=universal_set)
            if f == "tr":
                triangular.update_rating_linguistic_scale(
                    a=float(args[2]),
                    b=float(args[3]),
                    c=float(args[4]),
                    universal_set=universal_set,
                    fuzzy_sets=fuzzy_sets["triangular"],
                    name=name
                )
                triangular.show_plot(fuzzy_sets=fuzzy_sets["triangular"], fuzzy_colors=fuzzy_colors,
                                     universal_set=universal_set)
        if com == "[add]":
            if f == "td":
                trapezoid.add_rating_linguistic_scale(
                    a=float(args[2]),
                    b=float(args[3]),
                    c=float(args[4]),
                    d=float(args[5]),
                    universal_set=universal_set,
                    fuzzy_sets=fuzzy_sets["trapezoid"],
                    name=name
                )
                color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
                fuzzy_colors[name] = color
                trapezoid.show_plot(fuzzy_sets=fuzzy_sets["trapezoid"], fuzzy_colors=fuzzy_colors,
                                    universal_set=universal_set)
            if f == "tr":
                triangular.add_rating_linguistic_scale(
                    a=float(args[2]),
                    b=float(args[3]),
                    c=float(args[4]),
                    universal_set=universal_set,
                    fuzzy_sets=fuzzy_sets["triangular"],
                    name=name
                )
                color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
                fuzzy_colors[name] = color
                triangular.show_plot(fuzzy_sets=fuzzy_sets["triangular"], fuzzy_colors=fuzzy_colors,
                                     universal_set=universal_set)
    if com == "[predict]":
        args = split[1].split(":")[1].replace("[", "").replace("]", "").split(",")
        f = args[0]
        name = args[1]
        x = float(args[2])
        if f == "td":
            q = trapezoid.predict(
                x=x,
                universal_set=universal_set,
                fuzzy_sets=fuzzy_sets["trapezoid"],
                name=name
            )
            color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
            plt.plot(x, q, 'ro', label=split[1], color=color)
            print("\t\t->Принадлежность объкта ", x, " множеству ", name, " = ", q * 100, "%")
            trapezoid.show_plot(fuzzy_sets=fuzzy_sets["trapezoid"], fuzzy_colors=fuzzy_colors,
                                universal_set=universal_set)
        if f == "tr":
            q = triangular.predict(
                x=x,
                universal_set=universal_set,
                fuzzy_sets=fuzzy_sets["triangular"],
                name=name
            )
            color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
            plt.plot(x, q, 'ro', label=split[1], color=color)
            print("\t\t->Принадлежность объкта ", x, " множеству ", name, " = ", q * 100, "%")
            triangular.show_plot(fuzzy_sets=fuzzy_sets["triangular"], fuzzy_colors=fuzzy_colors,
                                 universal_set=universal_set)
    return


def read(file, data_list):
    with open(file, mode='r') as open_file:
        file_reader = csv.reader(open_file)
        data_list = list(rows[0:] for rows in file_reader)
        for i, row in enumerate(data_list):
            if i == 0:
                continue
            r = []
            for item in row:
                r.append(float(item))
            data_list[i] = r
    return data_list


if __name__ == "__main__":
    init()
    clear_time_series = read('main_series.csv', clear_time_series)
    trapezoid.create_accessory_table(fuzzy_sets["trapezoid"], clear_time_series, universal_set)
    print("-> введите ком.: ")
    while True:
        input_string = input()
        if input_string == "end":
            break
        input_parser(input_string)
        print("-> следующая ком. : ")
    print()
