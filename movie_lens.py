import csv
import time
from trie import trie_node
from hash import hash

def ids_trie(data_path):
    movie_ids = trie_node()

    with open(data_path, 'r') as movies_csv:
        csv_reader = csv.reader(movies_csv)
        next(csv_reader, None)
        for row in csv_reader:
            movie_ids.add(row[1],int(row[0]))

    return movie_ids

def titles_hash(data_path):
    movie_titles = hash(2**15)

    with open(data_path, 'r') as movies_csv:
        csv_reader = csv.reader(movies_csv)
        next(csv_reader, None)
        for row in csv_reader:
            movie_titles.add(int(row[0]), row[1])
    return movie_titles

def read_ratings(movies_data, ratings_data):

    movies_info = hash(2**15)
    users_info = hash(2**18)

    with open(movies_data, 'r') as movies_csv:
        csv_reader = csv.reader(movies_csv)
        next(csv_reader, None)
        for row in csv_reader:
            movies_info.add(int(row[0]),[row[2].split('|'),[],0])

    with open(ratings_data, 'r') as ratings_csv:
        csv_reader = csv.reader(ratings_csv)
        next(csv_reader, None)
        for row in csv_reader:

            #movies_info operations

            data = movies_info.get(int(row[1]))[0]
            data[1].append(float(row[2]))
            data[2] += 1
            movies_info.update(int(row[1]), data)

            #users_info operations

            data = users_info.get(int(row[0]))[0]
            if not data:
                users_info.add(int(row[0]), [[int(row[1])], [float(row[2])]])
            else:
                data[0].append(row[1])
                data[1].append(row[2])
                users_info.update(int(row[0]), data)

    for cell in movies_info.data:
        if cell != None:
            if cell[1][2]:
                sum = 0
                for rating in cell[1][1]:
                    sum += rating
                cell[1][1] = sum / cell[1][2]
            else:
                cell[1][1] = 0

    return movies_info, users_info


def read_tags(data_path, movie_titles):

    tags = trie_node()

    with open(data_path, 'r') as tags_csv:
        csv_reader = csv.reader(tags_csv)
        next(csv_reader, None)
        for row in csv_reader:
            movies = tags.get(row[2])
            if movies:
                movie = movie_titles.get(int(row[1]))[0]
                if movie not in movies:
                    movies.append(movie)
                    tags.add(row[2],movies)
            else:
                movie = movie_titles.get(int(row[1]))[0]
                tags.add(row[2],[movie])
    return tags



def partition(ids, low, high, movies_info):
    i = low - 1
    pivot_id = ids[high]

    for j in range(low,high):
        if movies_info.get(ids[j])[0][1] >= movies_info.get(pivot_id)[0][1]:
            i += 1
            ids[i],ids[j] = ids[j],ids[i]

    ids[i+1],ids[high] = ids[high],ids[i+1]
    return i+1

def quicksort(ids, low, high, movies_info):

    if low < high:
        pivot_idx = partition(ids, low, high, movies_info)

        quicksort(ids, low, pivot_idx-1, movies_info)
        quicksort(ids, pivot_idx+1, high, movies_info)





if __name__ == '__main__':

    start_time = time.time()


    #INICIALIZACAO DAS ESTRUTURAS DE DADOS

    #1 - TRIE

    movie_ids = ids_trie('Dados/movie.csv')

    movie_titles = titles_hash('Dados/movie.csv')

    #2 - HASH TABLE AND 3 - ANY STRUCTURE

    movies_info, users_info = read_ratings('Dados/movie.csv', 'Dados/rating.csv')

    #EXTRA - TRIE PARA TAGS

    tags = read_tags('Dados/tag.csv', movie_titles)

    print("--- %s seconds ---" % (time.time() - start_time))

    #MODO CONSOLE
    sorted_ids = []
    query = input('$ ')
    while(query):

        #movie <prefix> -----------------------------------------------------------------------------------------------

        if query.split(' ')[0] == 'movie':

            results = movie_ids.search(query[6:])
            print("{0:<7} | {1:<40} | {2:<40} | {3:<7} | {4:<6}".format('movieid','title','genres','ratings','count'))
            for result in results:
                print("{0:7} | {1:40.40} | {2:40.40} | {3:7.6} | {4:6}".format(result[1],
                                                                               result[0],
                                                                               '|'.join(movies_info.get(result[1])[0][0]),
                                                                            movies_info.get(result[1])[0][1],
                                                                            movies_info.get(result[1])[0][2]))


        #user <id> ----------------------------------------------------------------------------------------------------

        if query.split(' ')[0] == 'user':

            user_info = users_info.get(int(query.split(' ')[1]))[0]
            if user_info != None:
                print('{0:11} | {1:40} | {2:13} | {3:6}'.format('user_rating','title','global_rating','count'))
                for i in range(len(user_info[0])):
                    print('{0:>11.1f} | {1:40.40} | {2:>13.6f} | {3:<5}'.format(float(user_info[1][i]),
                                                                               movie_titles.get(int(user_info[0][i]))[0],
                                                                               float(movies_info.get(int(user_info[0][i]))[0][1]),
                                                                               movies_info.get(int(user_info[0][i]))[0][2]))

            else:
                print('No matching results')




        #topN <genre> -----------------------------------------------------------------------------------------------


        if query[:3] == 'top':
            N = int(query.split(' ')[0][3:])
            genre = query.split(' ')[1].replace("'",'')
            if not sorted_ids:
                sorted_ids = [x[0] for x in [y for y in movies_info.data if y != None] if x[1][2] >= 1000]
                quicksort(sorted_ids, 0, len(sorted_ids)-1, movies_info)
            print("{0:<40} | {1:<40} | {2:<7} | {3:<6}".format('title', 'genres', 'ratings', 'count'))
            for id in sorted_ids:
                if genre in movies_info.get(id)[0][0]:
                    print("{0:40.40} | {1:40.40} | {2:7.6} | {3:6}".format(movie_titles.get(id)[0],
                                                                           '|'.join(movies_info.get(id)[0][0]),
                                                                           movies_info.get(id)[0][1],
                                                                           movies_info.get(id)[0][2]))
                    N -= 1
                    if N == 0:
                        break






        #tags <list of tags> -----------------------------------------------------------------------------------------


        if query.split(' ')[0] == 'tags':
            tag_list = [x for x in query[5:].split("'") if x != '' and x != ' ']
            movies = tags.get(tag_list[0])
            if not movies:
                movies = []
            for tag in tag_list[1:]:
                movies = [movie for movie in movies if movie in tags.get(tag)]

            print('{0:40} | {1:<40} | {2:<7} | {3:<6}'.format('title','genres','rating','count'))

            for movie in movies:
                id = movie_ids.get(movie)
                print('{0:40.40s} | {1:40.40s} | {2:.5f} | {3:<6}'.format(movie,
                                                                         "|".join(movies_info.get(id)[0][0]),
                                                                         float(movies_info.get(id)[0][1]),
                                                                         movies_info.get(id)[0][2]))


        #LE QUERY ----------------------------------------------------------------------------------------------------

        query = input('$ ')