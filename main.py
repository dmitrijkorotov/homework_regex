import csv
import re
from pprint import pprint


def open_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        return list(reader)

def correct_full_name(data):
    new_data = [data[0]]
    for all_data in data[1:]:
        full_name = " ".join(all_data[:3]).split()
        for idx, last_first_surname in enumerate(full_name):
            all_data[idx] = last_first_surname
        new_data.append(all_data)
    return new_data

def format_nunmer(data):
    format_number = [data[0]]
    pattern = r'(\+7|8)?\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})\s*\(*(доб.)*\s*(\d*)\)*'
    for list_data in data[1:]:
        data_list = []
        for value in list_data:
            result = re.sub(pattern, r'+7(\2)\3-\4-\5 \6\7', value)
            data_list.append(result.strip())
        format_number.append(data_list)
    return format_number

def dublicate_del(data):
    combined_data = {}
    for entry in data:
        key = (entry[0], entry[1])
        if key not in combined_data:
            combined_data[key] = entry
        else:
            for i in range(2, len(entry)):
                if entry[i] and not combined_data[key][i]:
                    combined_data[key][i] = entry[i]
    return list(combined_data.values())

def save_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(data)

if __name__ == '__main__':
    data = open_csv('phonebook_raw.csv')
    new_data = correct_full_name(data)
    pprint(new_data)
    format_number_list = format_nunmer(new_data)
    pprint(format_number_list)
    dublicate_del_list = dublicate_del(format_number_list)
    pprint(dublicate_del_list)
    save_csv(dublicate_del_list, 'phonebook.csv')
