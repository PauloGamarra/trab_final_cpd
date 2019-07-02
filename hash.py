class hash(object):
    def __init__(self, size):
        self.size = size
        self.data = [None for i in range(size)]

    # função de inserção na tabela usando quadratic probing para resolver colisões
    # os valores de c1 e c2 escolhidos são adequados para size igual a uma potencia de 2
    # None significa que o endereço está livre e nunca foi usado enquanto False significa que apenas está livre
    def add(self, key, data):

        initial_address = (key * 73) % self.size
        address = initial_address
        if (self.data[address] == None or self.data[address] == False):
            self.data[address] = [key, data]
            return (1)
        else:
            i = 1
            while (self.data[address] != None and self.data[address] != False):
                address = (initial_address + int(1/2 * i + 1/2 * i ** 2)) % self.size
                i += 1
            self.data[address] = [key, data]
            return (i)

    def get(self, key):

        initial_address = (key * 73) % self.size
        address = initial_address
        if(self.data[address] == None):
            return None, 1
        if(self.data[address] != False):
            if(self.data[address][0] == key):
                return self.data[address][1], 1
        i = 1
        while (self.data[address] != None):
            address = (initial_address + int(1/2 * i + 1/2 * i ** 2)) % self.size
            i += 1
            if(address == initial_address):
                return None, i
            if(self.data[address] != False and self.data[address] != None):
                if(self.data[address][0] == key):
                    return self.data[address][1], i
        return None, i

    def update(self, key, data):

        initial_address = (key * 73) % self.size
        address = initial_address
        if self.data[address][0] == key:
            self.data[address][1] = data
            return 1
        else:
            i = 1
            while (1):
                address = (initial_address + int(1 / 2 * i + 1 / 2 * i ** 2)) % self.size
                i += 1
                if self.data[address] != False:
                    if self.data[address][0] == key:
                        self.data[address][1] = data
                        return i


if __name__ == '__main__':

    hash = hash(16)
    hash.add(16, 'kobayashi-san')
    hash.add(32, 'alface')
    hash.update(32,'cenoura')
    print(hash.get(32))