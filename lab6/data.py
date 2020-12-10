import random

import trapezoid

fuzzy_scores = dict(
    температура=dict(
        x_limit=26.0
    ),
    ветер=dict(
        x_limit=27.0
    ),
    осадки=dict(
        x_limit=24.0
    )
)

base_rules = [
    ["температура", "ветер", "осадки"],
    #
    ["низкая", "высокая", "много"],
    ["низкая", "средняя", "много"],
    ["низкая", "низкая", "среднее"],
    ["средняя", "высокая", "среднее"],
    ["высокая", "низкая", "мало"]
]


def init():
    fuzzy_scores["температура"]["низкая"] = dict(
        a=0.0,
        b=0.0,
        c=12.0,
        d=14.0,
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    fuzzy_scores["температура"]["средняя"] = dict(
        a=12.0,
        b=14.0,
        c=19.0,
        d=21.0,
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    fuzzy_scores["температура"]["высокая"] = dict(
        a=19.0,
        b=21.0,
        c=fuzzy_scores["температура"]["x_limit"],
        d=fuzzy_scores["температура"]["x_limit"],
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    #
    #
    #
    fuzzy_scores["ветер"]["низкая"] = dict(
        a=0.0,
        b=0.0,
        c=13.0,
        d=15.0,
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    fuzzy_scores["ветер"]["средняя"] = dict(
        a=13.0,
        b=15.0,
        c=20.0,
        d=22.0,
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    fuzzy_scores["ветер"]["высокая"] = dict(
        a=20.0,
        b=22.0,
        c=fuzzy_scores["ветер"]["x_limit"],
        d=fuzzy_scores["ветер"]["x_limit"],
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    #
    #
    #
    fuzzy_scores["осадки"]["мало"] = dict(
        a=0.0,
        b=0.0,
        c=10.0,
        d=12.0,
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    fuzzy_scores["осадки"]["среднее"] = dict(
        a=10.0,
        b=12.0,
        c=17.0,
        d=19.0,
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )
    fuzzy_scores["осадки"]["много"] = dict(
        a=17.0,
        b=19.0,
        c=fuzzy_scores["осадки"]["x_limit"],
        d=fuzzy_scores["осадки"]["x_limit"],
        color="#" + "%06x" % random.randint(0, 0xFFFFFF)
    )

    return
