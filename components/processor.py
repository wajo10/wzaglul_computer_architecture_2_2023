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

        def print_cache(self):
            print("__________Cache_____________")
            for i in range(self.num_blocks):
                print(self.blocks[i].name, hex(self.blocks[i].memory_address), hex(self.blocks[i].data), self.blocks[i].state)
            print("____________________________")

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

        def write(self, address:hex, data:hex):
            for i in range(self.num_blocks):
                if self.blocks[i].memory_address == address:
                    index = i
                    if self.blocks[index].state in ['I', 'O', 'S']:
                        self.blocks[index].data = data
                        self.blocks[index].state = 'M'
                        time.sleep(0.1)
                        return True
                    else:
                        # Write to memory
                        return False


                # check if there is a free block
                for blk in self.blocks:
                    if blk.state == 'I':
                        # write to block
                        blk.memory_address = address
                        blk.data = data
                        blk.state = 'M'
                        time.sleep(0.1)
                        return True
                # no free block
                return False


        class CacheBlock:
            def __init__(self, name:str):
                self.name = name
                self.memory_address = 0x0000
                self.data = 0x0000
                self.state = 'I'






