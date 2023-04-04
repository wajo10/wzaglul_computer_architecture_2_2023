import threading
import time



class Processor(threading.Thread):
    def __init__(self, name: str):
        threading.Thread.__init__(self)
        self.name = name
        self.cache = self.cache()

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

        def read(self, address:hex):
            for i in range(self.num_blocks):
                if self.blocks[i].memory_address == address:
                    index = i
                    if self.blocks[index].state in ['M', 'O', 'E', 'S']:
                        data = self.blocks[index].data
                        self.blocks[index].state = 'S'
                        time.sleep(0.1)
                        return data
                    else:
                        return False

                else:
                    return False

        class CacheBlock:
            def __init__(self, name:str):
                self.name = name
                self.memory_address = 0x0000
                self.data = 0x0000
                self.state = 'I'






