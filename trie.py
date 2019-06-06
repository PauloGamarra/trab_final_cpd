class trie_node(object):

    def __init__(self, char = '*'):
        self.char = char
        self.children = []
        self.data = None

    def add_data(self,key:str,data):
        node = self
        for letter in key:
            found = False
            for child in node.children:
                if letter == child.char:
                    node = child
                    found = True
                    break
            if not found:
                node.children.append(trie_node(letter))
                node = node.children[-1]
        node.data = data

    def get_data(self,key:str):
        node = self
        for letter in key:
            found = False
            for child in node.children:
                if letter == child.char:
                    node = child
                    found = True
                    break
            if not found:
                return False
        return node.data


if __name__ == '__main__':
    print('Hewoooooow 0w0')
    names = trie_node()
    names.add_data('batata',22)
    names.add_data('baiacu',71)
    names.add_data('baiana',38)
    names.add_data('cenoura', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH')
    print(names.get_data('batata'))
    print(names.get_data('baiana'))
    print(names.get_data('balada'))
    print(names.get_data('baiacu'))
    print(names.get_data('cenoura'))