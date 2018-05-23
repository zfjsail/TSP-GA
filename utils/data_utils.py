from os.path import join
import codecs
import settings


def load_cities(fname):
    city_dict = {}
    city_list = []
    with codecs.open(join(settings.DATA_DIR, fname), 'r', encoding='utf-8') as rf:
        for line in rf:
            items = line.split()
            city_no = items[0]
            city_list.append(city_no)
            city_dict[city_no] = {}
            city_dict[city_no]['x'] = float(items[1])
            city_dict[city_no]['y'] = float(items[2])
    return city_list, city_dict


city_list, city_dict = load_cities('dj38.txt')
city_num = len(city_list)


if __name__ == '__main__':
    city_list, city_dict = load_cities('dj38.txt')
    print(city_list)
    print(city_dict)
