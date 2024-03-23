import hw13_data as data
import csv
import json
import os

genres_dict = json.loads(data.genres)
header_list = ['title', 'year', 'rating', 'type', 'genres']
os.mkdir('genres')
os.chdir('genres')
for genre in genres_dict['results']:
    genre_name = genre['genre']
    os.mkdir(genre_name)
    os.chdir(genre_name)
    csv_file = genre_name + ".csv"
    file_obj = open(csv_file, 'w', newline='')
    csv_obj = csv.writer(file_obj, quotechar=' ')
    csv_obj.writerow(header_list)
    file_obj.close()
    os.chdir("..")
for film in data.films_data:
    data_list = [film['title']]
    data_list.append(str(film['year']))
    data_list.append(str(film['rating']))
    data_list.append(film['type'])
    gen_list = []
    gen_line = ''
    for gen in film['gen']:
        gen_list.append(gen['genre'])
        gen_line += gen['genre'] + '; '
    # removing last ;
    gen_line = gen_line.strip()[:-1]
    data_list.append(gen_line)
    for genre in gen_list:
        os.chdir(genre)
        csv_file = genre + ".csv"
        file_obj = open(csv_file, 'a', newline='')
        csv_obj = csv.writer(file_obj, quotechar=' ')
        csv_obj.writerow(data_list)
        file_obj.close()
        os.chdir("..")