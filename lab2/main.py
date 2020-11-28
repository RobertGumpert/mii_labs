import csv
import itertools
import random
import sys
import matplotlib.pyplot as plt

objects_table = []
accessory_table = []
fuzziness_m = 4
rnd = 20
steps_reports = list()


#
# -----------------------------------------------------------------------------------------------------------------------
#

def euclidean_distance(a, b):
    summary = 0
    for i in range(len(a)):
        difference = a[i] - b[i]
        power = round(pow(difference, 2), rnd)
        summary += power
    return round(summary ** (1 / float(2)), rnd)


def write_step_reports(header, table):
    steps_reports.append(header)
    for index, row in enumerate(table):
        if index == 0:
            steps_reports.append(' '.join([elem for elem in row]))
            # print('\t\t\t\t\t\t', ' '.join([elem for elem in row]))
        else:
            steps_reports.append(' '.join(["{:.6f}".format(float(elem)) for elem in row]))
            # print('\t\t\t\t\t\t', ' '.join(["{:.6f}".format(float(elem)) for elem in row]))


def update_accessory(m, centers, x_table, header):
    #
    # || xi - xl || or ||xi - xj||, (d(L))
    #
    def get_distances_table():
        distances_list = list(list())
        for x_index, x_row in enumerate(x_table):
            if x_index == 0:
                continue
            row = list()
            for center_index, center_row in enumerate(centers):
                if center_index == 0:
                    continue
                distance = euclidean_distance(x_row, center_row)
                row.insert(center_index - 1, distance)
            distances_list.insert(x_index - 1, row)
        return distances_list

    #
    # u(ij) = 1 / sum[(||xi - xj|| / || xi - xl ||)^3.3]
    #
    def get_new_accessory_table(distances_list):
        # ( d(i,j) / d(Ln))^3.3
        fractions_dict = dict()
        update_accessory_list = list(list())
        update_accessory_list.insert(0, header)
        for l_index, _ in enumerate(distances_list[0]):
            fractions_dict[l_index] = list(list())
        for l_index, _ in enumerate(distances_list[0]):
            # Ln
            l_column = [row[l_index] for row in distances_list]
            for i, _ in enumerate(distances_list):
                row = list()
                for j, _ in enumerate(distances_list[i]):
                    fraction = round((distances_list[i][j] / l_column[i]), rnd)
                    power = round(pow(fraction, 3.33), rnd)
                    row.insert(j, power)
                fractions_dict[l_index].insert(i, row)
        for row_index, _ in enumerate(distances_list):
            row = list()
            for j, _ in enumerate(distances_list[0]):
                summary = 0
                for l_index, _ in enumerate(distances_list[0]):
                    summary += fractions_dict[l_index][row_index][j]
                update = round((1 / summary), rnd)
                row.insert(j, update)
            update_accessory_list.insert(row_index + 1, row)
        return update_accessory_list

    #
    # j = sum of sum [u(I,j)^m * d(L)]
    #
    def get_j(u_table, distances_list):
        um_multiply_distance_table = []
        for i, _ in enumerate(u_table):
            if i == 0:
                continue
            um_multiply_distance_row = []
            for j, _ in enumerate(u_table[i]):
                power = round(pow(u_table[i][j], m), rnd)
                multiply = power * distances_list[i - 1][j]
                um_multiply_distance_row.append(round(multiply, rnd))
            um_multiply_distance_table.append(um_multiply_distance_row)
        #
        j_value = sum(sum(um_multiply_distance_table, []))
        return j_value

    #
    #
    #
    distances_table = get_distances_table()
    new_accessory_table = get_new_accessory_table(distances_table)
    j = get_j(new_accessory_table, distances_table)
    #
    #
    #
    write_step_reports(
        header='Функция потерь        :' + str(j) + '\nТаблица принадлежности: ',
        table=new_accessory_table
    )
    return new_accessory_table, j


def center_of_clusters(m, u_table, x_table):
    #
    # u(i,j) ^ m
    #
    def get_u_power_m():
        u_power_m_table = []
        sum_columns_u_power_m_table = []
        #
        for row in u_table[1:len(u_table)]:
            power_row = []
            for u in row:
                power_row.append(round(pow(u, m), rnd))
            u_power_m_table.append(power_row)
        #
        for column in range(len(u_power_m_table[0])):
            sum_column = 0
            for row in range(len(u_power_m_table)):
                sum_column += u_power_m_table[row][column]
            sum_columns_u_power_m_table.append(sum_column)
        #
        return u_power_m_table, sum_columns_u_power_m_table

    #
    # u(i,j) ^ m * [x0, x1, ... xn]
    #
    def get_u_multiply_feature(u_power_m_table):
        um_multiply_feature_dict = dict()
        feature_index_name = dict()
        for feature_index, feature_name in enumerate(x_table[0]):
            um_multiply_feature_dict[feature_index] = list(list())
            um_multiply_feature_dict[feature_name] = list(list())
            feature_index_name[feature_index] = feature_name
        for i, _ in enumerate(x_table):
            if i == 0:
                continue
            for j, _ in enumerate(x_table[i]):
                row_multiply = list()
                for u_power_m_value in u_power_m_table[i - 1]:
                    multiply = x_table[i][j] * u_power_m_value
                    row_multiply.append(round(multiply, rnd))
                if len(row_multiply) == 0:
                    continue
                um_multiply_feature_dict[j].insert(i - 1, row_multiply)
        for key, val in um_multiply_feature_dict.items():
            if type(key) is int:
                name = feature_index_name[key]
                um_multiply_feature_dict[name] = val
        return um_multiply_feature_dict

    #
    # center of clusters
    #
    def get_center_of_clusters(sum_columns_u_power_m_table, um_multiply_feature_dict):
        centers_table = list(list())
        header = list()
        for feature_index, feature_name in enumerate(x_table[0]):
            header.insert(feature_index, feature_name)
        centers_table.insert(0, header)
        for um_index, um_sum in enumerate(sum_columns_u_power_m_table):
            row_centers = list()
            for key, val in um_multiply_feature_dict.items():
                if type(key) is int:
                    column = [row[um_index] for row in val]
                    center = round((sum(column) / sum_columns_u_power_m_table[um_index]), rnd)
                    row_centers.insert(key, center)
            centers_table.insert(um_index + 1, row_centers)
        return centers_table

    #
    #
    #
    u_power_m, sum_u_power_m = get_u_power_m()
    u_multiply_feature = get_u_multiply_feature(u_power_m)
    centers = get_center_of_clusters(sum_u_power_m, u_multiply_feature)
    #
    write_step_reports(
        header='Центры                : ',
        table=centers
    )
    return centers


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


def fcm():
    output_j = sys.float_info.max
    output_centers = None
    output_accessory = accessory_table
    steps = 1
    while True:
        steps_reports.append('\nШаг : ' + str(steps))
        next_step_centers = center_of_clusters(fuzziness_m, output_accessory, objects_table)
        next_step_accessory, next_step_j = update_accessory(fuzziness_m, next_step_centers, objects_table,
                                                            accessory_table[0])
        if next_step_j > output_j:
            break
        output_j = next_step_j
        output_centers = next_step_centers
        output_accessory = next_step_accessory
        steps += 1
    return output_j, output_centers, output_accessory


def write_report_file():
    with open('report.txt', mode='w') as open_file:
        open_file.truncate(0)
        for step in steps_reports:
            open_file.write(step + '\n')
    return


def show_plot(output_centers, output_accessory):
    max_in_feature = [max(i) for i in itertools.zip_longest(*objects_table[1:len(objects_table)], fillvalue=0)]
    plt.xlim(0, max_in_feature[0])
    plt.xlabel(objects_table[0][0])
    plt.ylim(0, max_in_feature[1])
    plt.ylabel(objects_table[0][1])
    cluster_colors = dict()
    # marker="x"
    for cluster_index, _ in enumerate(output_centers):
        if cluster_index == 0:
            continue
        cluster_color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        cluster_name = output_accessory[0][cluster_index-1]
        cluster_colors[cluster_name] = cluster_color
        plt.plot(output_centers[cluster_index][0], output_centers[cluster_index][1], 'ro',
                 label=cluster_name, marker="x", color=cluster_color)
    for u_index, _ in enumerate(output_accessory):
        if u_index == 0:
            continue
        index_max = max(range(len(output_accessory[u_index])), key=output_accessory[u_index].__getitem__)
        cluster_name = output_accessory[0][index_max]
        cluster_color = cluster_colors[cluster_name]
        plt.plot(objects_table[u_index][0], objects_table[u_index][1], 'ro',
                 marker=".", color=cluster_color)
    #
    plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    objects_table = read('test_objects.csv', objects_table)
    accessory_table = read('test_clusters.csv', accessory_table)
    #
    j, centers, accessory = fcm()
    write_report_file()
    show_plot(
        output_centers=centers,
        output_accessory=accessory
    )
    print()
