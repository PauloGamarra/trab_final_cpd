import csv
from trie import trie_node

def ids_trie(data_path):
    movie_ids = trie_node()

    with open(data_path, 'r') as movies_csv:
        csv_reader = csv.reader(movies_csv)
        next(csv_reader, None)
        for row in csv_reader:
            movie_ids.add_data(row[1],int(row[0]))

    return movie_ids


if __name__ == '__main__':

    #INICIALIZACAO DAS ESTRUTURAS DE DADOS

    #1 - TRIE

    movie_ids = ids_trie('Dados/movie.csv')

    #2 - HASH TABLE

    #3 - ANY STRUCTURE

    #MODO CONSOLE