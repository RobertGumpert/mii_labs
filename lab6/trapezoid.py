import matplotlib.pyplot as plt


def predict(fuzzy_set, x):
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


def show_plot(score_name, fuzzy_score):
    plt.ylim(0, 1)
    plt.xlim(0, fuzzy_score["x_limit"])
    for name, _ in fuzzy_score.items():
        if name == "x_limit":
            continue
        plt.plot([fuzzy_score[name]['a'], fuzzy_score[name]['b'], fuzzy_score[name]['c'],
                  fuzzy_score[name]['d'], fuzzy_score[name]['a']], [0, 1, 1, 0, 0], label=name,
                 color=fuzzy_score[name]["color"])
    plt.title(score_name)
    plt.xlabel('x')
    plt.ylabel('q')
    plt.legend()
    plt.show()
    return
