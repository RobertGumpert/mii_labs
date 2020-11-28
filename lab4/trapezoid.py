import matplotlib.pyplot as plt


def add_parameters(a, b, c, d):
    return dict(
        a=a,
        b=b,
        c=c,
        d=d
    )


def add_rating_linguistic_scale(a, b, c, d, name, fuzzy_sets, universal_set):
    if name in fuzzy_sets:
        raise Exception("Такое множество существует")
    if a < universal_set[0] or d > universal_set[-1]:
        raise Exception("Выход за границы универ. множ.")
    fuzzy_sets[name] = add_parameters(a, b, c, d)
    return fuzzy_sets


def update_rating_linguistic_scale(a, b, c, d, name, fuzzy_sets, universal_set):
    if name not in fuzzy_sets:
        raise Exception("Такое множество не существует")
    if a < universal_set[0] or d > universal_set[-1]:
        raise Exception("Выход за границы универ. множ.")
    update = add_parameters(a, b, c, d)
    fuzzy_sets[name] = update
    return fuzzy_sets


def predict(name, fuzzy_sets, universal_set, x):
    if x < universal_set[0] or x > universal_set[-1]:
        raise Exception("Выход за границы универ. множ.")
    if name not in name:
        raise Exception("Множество не определенно")
    fuzzy_set = fuzzy_sets[name]
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


def show_plot(fuzzy_sets, fuzzy_colors, universal_set):
    plt.ylim(0, 1)
    plt.xlim(universal_set[0], universal_set[-1])
    for name in fuzzy_sets:
        plt.plot([fuzzy_sets[name]['a'], fuzzy_sets[name]['b'], fuzzy_sets[name]['c'],
                  fuzzy_sets[name]['d'], fuzzy_sets[name]['a']], [0, 1, 1, 0, 0], label=name,
                 color=fuzzy_colors[name])
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()
    return


def create_accessory_table(fuzzy_sets, clear_time_series, universal_set):
    accessory_table = [[0] * len(fuzzy_sets)] * len(clear_time_series)
    column = 0
    for rating, borders in fuzzy_sets.items():
        accessory_table[0].insert(column, rating)
        for row_index, _ in enumerate(clear_time_series):
            if row_index == 0:
                continue
            q = predict(
                name=rating,
                fuzzy_sets=fuzzy_sets,
                x=clear_time_series[row_index][1],
                universal_set=universal_set
            )
            accessory_table[row_index].insert(column, q)
        column += 1
    return accessory_table
