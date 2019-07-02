class trie_node(object):

    def __init__(self, char = '*'):
        self.char = char
        self.children = []
        self.data = None

    def add(self,key:str,data):
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

    def get(self,key:str):
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

    def print(self, prefix=''):
        for child in self.children:
            if child.children:
                child.print(prefix + child.char)
            else:
                print(prefix + child.char + ' : ' + str(child.data))

    def search(self, prefix):
        node = self
        for letter in prefix:
            found = False
            for child in node.children:
                if letter == child.char:
                    node = child
                    found = True
                    break
            if not found:
                return []

        results = []
        if node.data:
            results.append([prefix, node.data])
        for child in node.children:
            child.scan(prefix,results)
        return results

    def scan(self,prefix,results):
        if self.data:
            results.append([prefix + self.char, self.data])
        else:
            for child in self.children:
                child.scan(prefix + self.char,results)



if __name__ == '__main__':
    print('Hewoooooow 0w0')
    names = trie_node()
    names.add('batata',22)
    names.add('baiacu',71)
    names.add('baiana',38)
    names.add('cenoura', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH')
    print(names.get('batata'))
    print(names.get('baiana'))
    print(names.get('balada'))
    print(names.get('baiacu'))
    print(names.get('cenoura'))
    names.print()