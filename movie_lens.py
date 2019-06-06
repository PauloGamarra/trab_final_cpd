from trie import trie_node

def ids_trie(data_path):
    with open(data_path, 'r') as movies_csv:
        lines = movies_csv.readlines()


    movie_ids = trie_node()

    for line in lines[1:]:
        movie_ids.add_data(line.split(',')[1][1:-1],int(line.split(',')[0]))

    return movie_ids
if __name__ == '__main__':

    #INICIALIZACAO DAS ESTRUTURAS DE DADOS

    #1 - TRIE

    movie_ids = ids_trie('Dados/movie.csv')

    #2 - HASH TABLE

    #3 - ANY STRUCTURE

    #MODO CONSOLE