
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
        self.block1 = self.MemoryBlock(16, 0x1000)
        self.block2 = self.MemoryBlock(16, 0x2000)
        self.block3 = self.MemoryBlock(16, 0x3000)
        self.block4 = self.MemoryBlock(16, 0x4000)
        self.block5 = self.MemoryBlock(16, 0x5000)
        self.block6 = self.MemoryBlock(16, 0x6000)
        self.block7 = self.MemoryBlock(16, 0x7000)
        self.block8 = self.MemoryBlock(16, 0x8000)


    class MemoryBlock:
        def __init__(self, size, address):
            self.size = size
            self.address = address
            self.data = bytearray(size)
            for i in range(size):
                self.data[i] = 0x0000 # Initialize memory to 0x0000

        def read(self, address, length):
            offset = address - self.address
            return self.data[offset:offset + length]

        def write(self, address, data):
            offset = address - self.address
            self.data[offset:offset + len(data)] = data