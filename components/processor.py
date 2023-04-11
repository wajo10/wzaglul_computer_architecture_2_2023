import threading
import time
from components import  bus
import utils



class Processor(threading.Thread):
    def __init__(self, name: str, logger: utils.Logs):
        threading.Thread.__init__(self)
        self.bus = None
        self.name = name
        self.cache = self.cache(name, self)
        self.instructions = []
        self.last_instruction = ""
        self.logger = logger
        self.pause_exec = False

    def set_bus(self, bus_: bus.Bus):
        self.bus = bus_

    def get_state(self):
        state = []
        for block in self.cache.blocks:
            block_state = {"Block": block.name,
                           "Address": block.memory_address,
                           "Data": block.data,
                           "State": block.state}
            state.append(block_state)
        return state


    def generate_random_instruction(self):
        inst = utils.hypergeometric_distribution(10, 2, 30, 1)[0]
        address = (utils.hypergeometric_distribution(100, 7, 155, 1)[0])
        if self.pause_exec:
            return
        if inst == 0:
            self.add_instruction(['read', address])
        elif inst == 1:
            data = int(utils.create_hex_data(), 16)
            self.add_instruction(['write', address, data])
        else:
            print("calc")
            self.add_instruction(['calc', address])
    def pause(self):
        self.pause_exec = True
        self.instructions = []


    def resume(self):
        self.pause_exec = False

    def add_instruction(self, instruction):
        self.instructions.append(instruction)


    def run(self):
        while True:
            while not self.instructions == []:
                instruction = self.instructions.pop(0)
                address = instruction[1]
                if instruction[0] == 'read':
                    instr = f"{self.name}: READ {'0' * (3 - len(bin(address)[2:])) + bin(address)[2:]}"
                    self.last_instruction = instr
                    self.logger.add_log(instr)

                    print(f"Processor {self.name} read from address {hex(instruction[1])}")
                    value = self.cache.read_self(instruction[1])
                    if value is not False:
                        print(f"Hit! Processor {self.name} read {hex(value)} from address {hex(instruction[1])}")
                        self.logger.add_log(f"Hit! Processor {self.name} read {hex(value)} from address {bin(instruction[1])[2:]}")
                        self.cache.print_cache()
                    else:
                        print("Read Miss! Go to Bus")
                        self.logger.add_log(f"Read Miss! {self.name} read from address {bin(instruction[1])[2:]}")
                        self.bus.read_cache(instruction[1], self.cache)

                elif instruction[0] == 'write':
                    data = instruction[2]
                    instr = f"{self.name}: WRITE {'0' * (3 - len(bin(address)[2:])) + bin(address)[2:]}; {hex(data)}"
                    self.last_instruction = instr
                    self.logger.add_log(instr)
                    if self.cache.write(instruction[1], instruction[2]):
                        print(f"Processor {self.name} wrote {hex(instruction[2])} to address {hex(instruction[1])}")
                        self.logger.add_log(f"Processor {self.name} wrote {hex(instruction[2])} to address {bin(instruction[1])[2:]}")
                        self.cache.print_cache()
                    else:
                        print("Write Miss!")
                        self.logger.add_log(f"Write Miss! {self.name}")
                        self.bus.invalidate_cache(instruction[1], [self.cache])
                        self.cache.print_cache()
                elif instruction[0] == 'calc':
                    instr = f"{self.name}: CALC"
                    self.last_instruction = instr
                    self.logger.add_log(instr)
                    time.sleep(1)
                    print(f"Processor {self.name} calculated")
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
                        if comes_from_cache:
                            blk.state = 'S'
                        return True
                    else:
                        # Return False to indicate that invalidation is needed
                        blk.data = data
                        if comes_from_cache:
                            blk.state = 'S'
                        else:
                            blk.state = 'M'
                        return False


            if address % 2 == 0:
                for blk in self.blocks[0:2]:
                    if blk.state == 'I':
                        blk.memory_address = address
                        blk.data = data
                        if comes_from_cache:
                            blk.state = 'S'
                        else:
                            blk.state = 'M'
                        return False
                # If no empty blocks, replace the first block and save the data
                self.processor.bus.write_main_memory(self.blocks[0].memory_address, self.blocks[0].data)
                self.blocks[0].memory_address = address
                self.blocks[0].data = data
                if comes_from_cache:
                    self.blocks[0].state = 'S'
                else:
                    self.blocks[0].state = 'E'
                return False
            else:
                for blk in self.blocks[2:4]:
                    if blk.state == 'I':
                        blk.memory_address = address
                        blk.data = data
                        if comes_from_cache:
                            blk.state = 'S'
                        else:
                            blk.state = 'M'
                        return False
                # If no empty blocks, replace the first block and save the data
                self.processor.bus.write_main_memory(self.blocks[2].memory_address, self.blocks[2].data)
                self.blocks[2].memory_address = address
                self.blocks[2].data = data
                if comes_from_cache:
                  self.blocks[2].state = 'S'
                else:
                    self.blocks[2].state = 'E'
                return False



        def invalidate(self, address:hex):
            for blk in self.blocks:
                if blk.memory_address == address:
                    blk.state = 'I'
                    print(f"Cache {self.name} invalidated block {blk.name} at address {hex(address)}")
                    self.processor.logger.add_log(f"Cache {self.name} invalidated block {blk.name} at address {bin(address)[2:]}")
                    return True
            return False


        class CacheBlock:
            def __init__(self, name:str):
                self.name = name
                self.memory_address = 0x0000
                self.data = 0x0000
                self.state = 'I'






