import random

import matplotlib.pyplot as plt


def analysis_time_series(accessory_table, fuzzy_sets):
    #
    # Нечеткий временой ряд
    #
    fuzzy_time_series_table = [None] * (len(accessory_table) - 1)
    #
    # Ряд тенденций
    #
    series_trends_table = [None] * len(fuzzy_time_series_table)
    #
    # Ряд интенсивности изменений
    #
    intensity_table = [None] * len(series_trends_table)

    def get_intensity(step_value):
        if step == 0:
            return "нет изменений"
        if step_value == 1:
            return "слабый"
        if 1 < step_value <= 3:
            return "заметный"
        if 3 < step_value >= 4:
            return "сиьный"
        return None

    #
    # Заполняем нечекий временной ряд
    #
    for row_index, _ in enumerate(accessory_table):
        if row_index == 0:
            continue
        #
        # Находим позицию (индекс) максимума в строке.
        #
        max_index_column = max(range(len(accessory_table[row_index])), key=accessory_table[row_index].__getitem__)
        if accessory_table[row_index][max_index_column] == 0.0:
            #
            # В случае если объект не принадлежит ни одному
            # из нечетких множеств (q = 0%), считаем что, ячейку
            # врменного ряда не валидной.
            #
            fuzzy_time_series_table[row_index - 1] = None
        else:
            #
            # В шапке таблицы принадлежности находим имя оценки,
            # соответствующую найденному индексу максимума.
            #
            fuzzy_time_series_table[row_index - 1] = accessory_table[0][max_index_column]
            next_row_index = row_index + 1
            #
            if next_row_index != len(accessory_table):
                max_next_index_column = max(range(len(accessory_table[next_row_index])),
                                            key=accessory_table[next_row_index].__getitem__)
                step = abs(max_next_index_column - max_index_column)
                intensity = get_intensity(step)
                intensity_table[next_row_index - 1] = intensity

    for row_index, _ in reversed(list(enumerate(fuzzy_time_series_table))):
        if row_index == 0:
            break
        #
        # В случае если объект не принадлежит ни одному
        # из нечетких множеств (q = 0%), считаем что, ячейку
        # врменного ряда не валидной.
        #
        if fuzzy_time_series_table[row_index - 1] is None or fuzzy_time_series_table[row_index] is None:
            continue

        a_border = fuzzy_sets[fuzzy_time_series_table[row_index]]["a"]
        a_border_next = fuzzy_sets[fuzzy_time_series_table[row_index - 1]]["a"]

        if a_border == a_border_next:
            series_trends_table[row_index] = "стабильность"
            continue
        if a_border < a_border_next:
            series_trends_table[row_index] = "удорожание"
            continue
        if a_border > a_border_next:
            series_trends_table[row_index] = "удешевление"
            continue
        series_trends_table.insert(row_index, None)
    return fuzzy_time_series_table, series_trends_table, intensity_table


def show_fuzzy_time_series(fuzzy_sets, fuzzy_time_series_table, clear_time_series_table):
    moments = [row[0] for row in clear_time_series_table[1:len(clear_time_series_table)]]
    min_moment = min(moments)
    max_moment = max(moments)
    plt.xlim(min_moment, max_moment)
    y = list(fuzzy_sets.keys())
    #
    colors = dict()
    for v in y:
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        colors[v] = color
    for i, _ in enumerate(moments):
        fuzzy_rating = fuzzy_time_series_table[i]
        if fuzzy_rating is None:
            continue
        plt.plot(
            moments[i],
            fuzzy_rating,
            'ro',
            color=colors[fuzzy_rating]  # , marker="x"
        )
    plt.xlabel('t')
    plt.ylabel('rating')
    plt.legend()
    plt.show()
    return


def show_series_trends(series_trends_table, clear_time_series_table):
    moments = [row[0] for row in clear_time_series_table[1:len(clear_time_series_table)]]
    min_moment = min(moments)
    max_moment = max(moments)
    plt.xlim(min_moment, max_moment)
    y = list(set(series_trends_table))
    #
    colors = dict()
    for v in y:
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        colors[v] = color
    for i, _ in enumerate(moments):
        trend = series_trends_table[i]
        if trend is None:
            continue
        plt.plot(
            moments[i],
            trend,
            'ro',
            color=colors[trend]  # , marker="x"
        )
    plt.xlabel('t')
    plt.ylabel('trend')
    plt.legend()
    plt.show()
    return
