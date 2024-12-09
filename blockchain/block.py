import hashlib


def update_hash(*args):
    text = ""
    h = hashlib.sha256()
    for arg in args:
        text += str(arg)

    h.update(text.encode("utf-8"))
    return h.hexdigest()


class Block:
    data = None
    hash = None
    nonce = 0
    previous_hash = "0" * 64

    def __init__(self, data, number=0):
        self.data = data
        self.number = number

    def hashit(self):
        return update_hash(self.previous_hash, self.number, self.data, self.nonce)

    def __str__(self):
        return f"N: {self.number}\nHash: {self.hashit()}\nPrh: {self.previous_hash}\nNonce: {self.nonce}\nData: {self.data}"


class Blockchain:
    diff = 3

    def __init__(self, prev_chain=None):
        if prev_chain is None:
            prev_chain = []
        self.chain = prev_chain

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hashit()
        except IndexError:
            pass

        while True:
            if block.hashit()[:self.diff] == "0" * self.diff:
                self.add(block)
                break
            else:
                block.nonce += 1

    def is_valid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hashit()
            if _previous != _current or _current[:self.diff] != "0" * self.diff:
                return False


chain = Blockchain()
db = [
    "hi",
    "hello",
    "bye",
    "mucho gusto"
]
n = 0

for d in db:
    n += 1
    chain.mine(Block(d, n))

for block in chain.chain:
    print(block)
