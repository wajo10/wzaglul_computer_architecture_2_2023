
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class MainMemory(object):
    def __init__(self):
        self.block1 = self.MemoryBlock( 0x0000)
        self.block2 = self.MemoryBlock( 0x0001)
        self.block3 = self.MemoryBlock( 0x0002)
        self.block4 = self.MemoryBlock( 0x0003)
        self.block5 = self.MemoryBlock( 0x0004)
        self.block6 = self.MemoryBlock( 0x0005)
        self.block7 = self.MemoryBlock( 0x0006)
        self.block8 = self.MemoryBlock( 0x0007)
        self.blocks = [self.block1, self.block2, self.block3, self.block4, self.block5, self.block6, self.block7, self.block8]

    def print_memory(self):
        for i in range(len(self.blocks)):
            print("Block " + str(i) + ": " + str(hex(self.blocks[i].address)) + " " + str(self.blocks[i].data))


    def write(self, address, data):
        for i in range(len(self.blocks)):
            if self.blocks[i].address == address:
                self.blocks[i].data = data
                return True
        return False

    def read(self, address):
        for i in range(len(self.blocks)):
            if self.blocks[i].address == address:
                return self.blocks[i].data
        return False


    class MemoryBlock:
        def __init__(self, address):
            self.address = address
            self.data = 0x0000

        def read(self, address, length):
            offset = address - self.address
            return self.data[offset:offset + length]

        def write(self, address, data):
            offset = address - self.address
            self.data[offset:offset + len(data)] = data