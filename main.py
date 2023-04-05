from components import processor, main_memory, bus

def initialize(processors_list:list):
    global memory
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