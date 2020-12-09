import enum
import pprint


class ExploredField(enum.Enum):
    NVR = 0
    Trends = 1


class SongModel(object):
    max_learn_deep = 1
    explored_field = None
    all_rule_bases = None
    clear_time_series = None
    fuzzy_scores = None
    rule_convert_from_trend_to_score = None
    explored_series = None

    def __init__(self, explored_field, max_learn_deep, clear_time_series, accessory_table, fuzzy_scores,
                 rule_convert_from_trend_to_score):
        self.explored_field = explored_field
        self.max_learn_deep = max_learn_deep
        self.all_rule_bases = dict()
        self.clear_time_series = clear_time_series
        self.accessory_table = accessory_table
        self.fuzzy_scores = fuzzy_scores
        self.rule_convert_from_trend_to_score = rule_convert_from_trend_to_score

    def fit(self, series):
        self.explored_series = series

        def create_base_rules(deep_):
            rules = list()
            for i, _ in enumerate(series):
                if series[i] is None:
                    continue
                if i == (len(series) - deep_):
                    break
                left_part = ""
                right_part = series[i + deep_]
                for next_value in range(0, deep_):
                    left_part += series[i + next_value]
                rules.append(dict(
                    left=left_part,
                    right=right_part
                ))
            return rules

        def base_is_describe_model(rules_, deep_):
            last_value_in_series = self.__get_last_value_in_series(deep_, series)
            for rule in rules_:
                if rule["left"] == last_value_in_series:
                    return True
            return False

        for deep in range(1, self.max_learn_deep + 1):
            base_rules = create_base_rules(deep)
            if base_is_describe_model(base_rules, deep) is True:
                self.all_rule_bases[deep] = base_rules
        pprint.pprint(self.explored_series)
        pprint.pprint(self.all_rule_bases)
        return

    def predict_next(self, nvr=None):
        if self.explored_field.value is ExploredField.NVR.value:
            return self.__predict_nvr()
        if self.explored_field.value is ExploredField.Trends.value:
            pprint.pprint(nvr)
            return self.__predict_trends(nvr)
        return

    def __predict_nvr(self):
        result = dict()
        for deep, base in self.all_rule_bases.items():

            last_value_in_series_ = self.__get_last_value_in_series(deep, self.explored_series)
            predicted_values = list()
            rule_indices = list()
            mape_list = list()
            for index, rule in enumerate(base):
                if rule["left"] == last_value_in_series_:
                    predict_value = self.__centroid(rule["right"])
                    if predict_value is None:
                        continue
                    rule_indices.append(index)
                    predicted_values.append(predict_value)
                    mape_list.append(self.__get_mape(predict_value))
            min_mape_index = min(range(len(mape_list)), key=mape_list.__getitem__)
            # print(len(self.clear_time_series))
            # if len(self.clear_time_series) == 13 and deep == 2:
            #     print()
            result[deep] = dict(
                predict=predicted_values[min_mape_index],
                score=base[rule_indices[min_mape_index]]["right"],
                mape=mape_list[min_mape_index]
            )
        return result

    def __predict_trends(self, nvr):
        result = dict()

        def get_fuzzy_score(step_):
            last_fuzzy_score = nvr[-1]
            index_score = nvr.index(last_fuzzy_score)
            if step_ == 0:
                return last_fuzzy_score
            if step_ > 0 and self.fuzzy_scores[-1] == last_fuzzy_score:
                return last_fuzzy_score
            if step_ > 0 and self.fuzzy_scores[-1] != last_fuzzy_score:
                return self.fuzzy_scores[index_score + 1]
            if step_ < 0 and self.fuzzy_scores[0] == last_fuzzy_score:
                return last_fuzzy_score
            if step_ < 0 and self.fuzzy_scores[0] != last_fuzzy_score:
                return self.fuzzy_scores[index_score - 1]
            return

        for deep, base in self.all_rule_bases.items():
            last_value_in_series = self.__get_last_value_in_series(deep, self.explored_series)
            predicted_values = list()
            rule_indices = list()
            fuzzy_scores = list()
            mape_list = list()
            for index, rule in enumerate(base):
                if rule["left"] == last_value_in_series:
                    right = rule["right"]
                    step = self.rule_convert_from_trend_to_score[right]
                    predict_fuzzy_score = get_fuzzy_score(step)
                    predict_value = self.__centroid(predict_fuzzy_score)
                    if predict_value is None:
                        continue
                    rule_indices.append(index)
                    predicted_values.append(predict_value)
                    mape_list.append(self.__get_mape(predict_value))
                    fuzzy_scores.append(predict_fuzzy_score)
            min_mape_index = min(range(len(mape_list)), key=mape_list.__getitem__)
            result[deep] = dict(
                predict=predicted_values[min_mape_index],
                score=fuzzy_scores[min_mape_index],
                mape=mape_list[min_mape_index],
                trend=base[rule_indices[min_mape_index]]["right"]
            )
        return result

    def __centroid(self, fuzzy_score):
        index_column_fuzzy_score = self.fuzzy_scores.index(fuzzy_score)
        sum_accessory = 0.0
        sum_mult = 0.0
        for i, _ in enumerate(self.accessory_table):
            if i == 0:
                continue
            sum_accessory += self.accessory_table[i][index_column_fuzzy_score]
            sum_mult += self.accessory_table[i][index_column_fuzzy_score] * self.clear_time_series[i][1]
        if sum_accessory == 0.0:
            return None
        predict = sum_mult / sum_accessory
        return predict

    def __get_last_value_in_series(self, deep, series):
        last_value_in_series = ""
        for prev in range((len(series) - deep), len(series)):
            index = (len(series) - prev) * (-1)
            last_value_in_series += series[index]
        return last_value_in_series

    def __get_mape(self, predicted_value):
        sum_ = 0.0
        for i, val in enumerate(self.clear_time_series):
            if i == 0:
                continue
            sum_ += (abs(val[1] - predicted_value)) / predicted_value
        mape = float(sum_) / float(len(self.clear_time_series))
        return mape
