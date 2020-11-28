import matplotlib.pyplot as plt


def add_parameters(a, b, c):
    return dict(
        a=a,
        b=b,
        c=c
    )


def add_rating_linguistic_scale(a, b, c, name, fuzzy_sets, universal_set):
    if name in fuzzy_sets:
        raise Exception("Такое множество существует")
    if a < universal_set[0] or c > universal_set[-1]:
        raise Exception("Выход за границы универ. множ.")
    fuzzy_sets[name] = add_parameters(a, b, c)
    return fuzzy_sets


def update_rating_linguistic_scale(a, b, c, name, fuzzy_sets, universal_set):
    if name not in fuzzy_sets:
        raise Exception("Такое множество не существует")
    if a < universal_set[0] or c > universal_set[-1]:
        raise Exception("Выход за границы универ. множ.")
    update = add_parameters(a, b, c)
    fuzzy_sets[name] = update
    return fuzzy_sets


def predict(name, fuzzy_sets, universal_set, x):
    if x < universal_set[0] or x > universal_set[-1]:
        raise Exception("Выход за границы универ. множ.")
    if name not in name:
        raise Exception("Множество не определенно")
    fuzzy_set = fuzzy_sets[name]
    if fuzzy_set['a'] <= x <= fuzzy_set['b']:
        fraction = 1 - (fuzzy_set['b'] - x) / (fuzzy_set['b'] - fuzzy_set['a'])
        return fraction
    if fuzzy_set['b'] <= x <= fuzzy_set['c']:
        fraction = 1 - (x - fuzzy_set['b']) / (fuzzy_set['c'] - fuzzy_set['b'])
        return fraction
    return 0


def show_plot(fuzzy_sets, fuzzy_colors, universal_set):
    plt.ylim(0, 1)
    plt.xlim(universal_set[0], universal_set[-1])
    for name in fuzzy_sets:
        plt.plot([fuzzy_sets[name]['a'], fuzzy_sets[name]['b'], fuzzy_sets[name]['c'],
                  fuzzy_sets[name]['a']], [0, 1, 0, 0], label=name,
                 color=fuzzy_colors[name])
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()
    return
