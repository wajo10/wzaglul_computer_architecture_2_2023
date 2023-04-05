from components import processor, main_memory, bus
import time
import utils
import random

def initialize(processors_list:list):
    while True:
        proc = random.choice(processors_list)
        inst = utils.hypergeometric_distribution(10, 2, 20, 1)[0]
        if inst == 0:
            address = (utils.hypergeometric_distribution(100, 7, 155, 1)[0])
            print(f"Read in processor {proc.name} address {hex(address)}")
            value = proc.cache.read(address)
            if not value:
                print("Read miss")
                bus.read_cache(address, proc.cache)
            else:
                print(f"Value Read: {hex(value)}")
                proc.cache.print_cache()
        elif inst == 1:
            data = int(utils.create_hex_data(),16)
            address = (utils.hypergeometric_distribution(100, 7, 155, 1)[0])
            print(f"Write in processor {proc.name} address {hex(address)} the data {hex(data)}")
            if not proc.cache.write(address, data):
                print("Write miss")
                bus.write_main_memory(address, data)
                print("________Main Memory________")
                memory.print_memory()
            else:
                proc.cache.print_cache()

        else:
            print("calc")

        time.sleep(1)

    processor1.cache.write(0x0001, 0x0108)
    processor1.cache.print_cache()
    print("-------------------")

    processor1.cache.write(0x0003, 0x0105)
    processor1.cache.print_cache()
    print("-------------------")

    processor1.cache.write(0x0000, 0x0102)
    processor1.cache.print_cache()
    print("-------------------")

    processor1.cache.write(0x0002, 0x0103)
    processor1.cache.print_cache()
    print("------Main Memory--------")

    if not processor1.cache.write(0x0004, 0x0104):
        bus.write_main_memory(0x0004, 0x0104)

    memory.print_memory()



"""
To do:
    - Concat random values from hypergeometric_distribution and convert them to hex
    - Figure out how to create a communication bus
    - Write main function that keeps calling the processor's methods
    - Start working on the GUI
    - Figure out how to do step by step execution
    - State machine for cache blocks
    - Write the cache's methods 
    - Write the main memory's access methods
    - Escribir en cache segun paridad
    

"""


if __name__ == "__main__":
    processor1 = processor.Processor("P0")
    processor2 = processor.Processor("P1")
    processor3 = processor.Processor("P2")
    processor4 = processor.Processor("P3")
    processors = [processor1, processor2, processor3, processor4]

    memory = main_memory.MainMemory()

    bus = bus.Bus(memory, processors)
    initialize(processors)