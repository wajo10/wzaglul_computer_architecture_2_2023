import threading
import time
from components import  bus



class Processor(threading.Thread):
    def __init__(self, name: str):
        threading.Thread.__init__(self)
        self.bus = None
        self.name = name
        self.cache = self.cache(name, self)
        self.instructions = []

    def set_bus(self, bus_: bus.Bus):
        self.bus = bus_

    def add_instruction(self, instruction):
        self.instructions.append(instruction)


    def run(self):
        while True:
            if len(self.instructions) > 0:
                instruction = self.instructions.pop(0)
                if instruction[0] == 'read':
                    print(f"Processor {self.name} read from address {hex(instruction[1])}")
                    value = self.cache.read_self(instruction[1])
                    if value is not False:
                        print(f"Hit! Processor {self.name} read {hex(value)} from address {hex(instruction[1])}")
                        self.cache.print_cache()
                    else:
                        print("Read Miss! Go to Bus")
                        self.bus.read_cache(instruction[1], self.cache)

                elif instruction[0] == 'write':
                    if self.cache.write(instruction[1], instruction[2]):
                        print(f"Processor {self.name} wrote {hex(instruction[2])} to address {hex(instruction[1])}")
                        self.cache.print_cache()
                    else:
                        print("Write Miss!")
                        self.bus.invalidate_cache(instruction[1], [self.cache])
                        self.cache.print_cache()
            else:
                time.sleep(0.1)

    class cache(object):
        def __init__(self, name: str, processor):
            self.block1 = self.CacheBlock("B0")
            self.block2 = self.CacheBlock("B1")
            self.block3 = self.CacheBlock("B2")
            self.block4 = self.CacheBlock("B3")
            self.name = name
            self.num_blocks = 4
            self.blocks = [self.block1, self.block2, self.block3, self.block4]
            self.processor = processor

        def print_cache(self):
            print(f"__________Cache {self.name}_____________")
            for i in range(self.num_blocks):
                print(self.blocks[i].name, hex(self.blocks[i].memory_address), hex(self.blocks[i].data), self.blocks[i].state)
            print("____________________________")
        def read_self(self, address:hex):
            for blk in self.blocks:
                if blk.memory_address == address:
                    if blk.state in ['M', 'O', 'E', 'S']:
                        data = blk.data
                        return data
                    else:
                        return False

            return False
        def write_from_memory(self, address:hex, data:hex):
            if address % 2 == 0:
                for blk in self.blocks[0:2]:
                    if blk.state == 'I':
                        blk.memory_address = address
                        blk.data = data
                        blk.state = 'M'
                        return True
                # If no empty blocks, replace the first block and save the data
                self.processor.bus.write_main_memory(address, data)
                self.blocks[0].memory_address = address
                self.blocks[0].data = data
                self.blocks[0].state = 'M'
                return True
            else:
                for blk in self.blocks[2:4]:
                    if blk.state == 'I':
                        blk.memory_address = address
                        blk.data = data
                        blk.state = 'M'
                        return True
                # If no empty blocks, replace the first block and save the data
                self.processor.bus.write_main_memory(address, data)
                self.blocks[2].memory_address = address
                self.blocks[2].data = data
                self.blocks[2].state = 'M'
                return True

        def read(self, address:hex):
            for blk in self.blocks:
                if blk.memory_address == address:
                    if blk.state in ['M', 'O', 'E', 'S']:
                        data = blk.data
                        if blk.state == 'M':
                            blk.state = 'O'
                        else:
                            blk.state = 'S'
                        time.sleep(0.1)
                        return data
                    else:
                        return False

            return False

        def write(self, address:hex, data:hex, comes_from_cache=False):
            for blk in self.blocks:
                if blk.memory_address == address:
                    if blk.state in ['M', 'E']:
                        blk.data = data
                        blk.state = 'E'
                        return True
                    else:
                        # Return False to indicate that invalidation is needed
                        blk.data = data
                        blk.state = 'M'
                        return False

            if address % 2 == 0:
                for blk in self.blocks[0:2]:
                    if blk.state == 'I':
                        blk.memory_address = address
                        blk.data = data
                        if comes_from_cache:
                            blk.state = 'S'
                        blk.state = 'M'
                        return False
                # If no empty blocks, replace the first block and save the data
                self.processor.bus.write_main_memory(address, data)
                self.blocks[0].memory_address = address
                self.blocks[0].data = data
                if comes_from_cache:
                    self.blocks[0].state = 'S'
                self.blocks[0].state = 'E'
                return False
            else:
                for blk in self.blocks[2:4]:
                    if blk.state == 'I':
                        blk.memory_address = address
                        blk.data = data
                        if comes_from_cache:
                            blk.state = 'S'
                        blk.state = 'M'
                        return False
                # If no empty blocks, replace the first block and save the data
                self.processor.bus.write_main_memory(address, data)
                self.blocks[2].memory_address = address
                self.blocks[2].data = data
                if comes_from_cache:
                  self.blocks[2].state = 'S'
                self.blocks[2].state = 'E'
                return False



        def invalidate(self, address:hex):
            for blk in self.blocks:
                if blk.memory_address == address:
                    blk.state = 'I'
                    print(f"Cache {self.name} invalidated block {blk.name} at address {hex(address)}")
                    return True
            return False


        class CacheBlock:
            def __init__(self, name:str):
                self.name = name
                self.memory_address = 0x0000
                self.data = 0x0000
                self.state = 'I'






