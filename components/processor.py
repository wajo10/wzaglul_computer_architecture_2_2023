import threading
import time



class Processor(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print ("Starting " + self.name)
        print ("Exiting " + self.name)

    class cache(object):
        def __init__(self):
            self.block1 = self.CacheBlock("B0")
            self.block2 = self.CacheBlock("B1")
            self.block3 = self.CacheBlock("B2")
            self.block4 = self.CacheBlock("B3")
            self.num_blocks = 4
            self.blocks = [self.block1, self.block2, self.block3, self.block4]

        def read(self, address):
            for i in range(self.num_blocks):
                if self.blocks[i].memory_address == address:
                    index = i
                    if self.blocks[index].state in ['M', 'O', 'E', 'S']:
                        data = self.blocks[index].data
                        self.blocks[index].state = 'S'
                    else:
                        """
                        # Read from memory
                        data = memory.read(address, self.block_size)
                        self.blocks[index].data = data
                        self.blocks[index].state = 'S'
                        self.blocks[index].tag = tag
                        """
                        data = 0x0000

                    return data
                else:
                    """
                    # Read from memory
                    Value was not in cache
                    """




        class CacheBlock:
            def __init__(self, name):
                self.name = name
                self.memory_address = 0x0000
                self.data = 0x0000
                self.state = 'I'






