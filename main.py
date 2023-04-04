from components import processor, main_memory

def initialize(processors_list:list):
    global memory
    for i in range(len(processors_list)):
        processors_list[i].start()

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
    

"""


if __name__ == "__main__":
    processor1 = processor.Processor("P0")
    processor2 = processor.Processor("P1")
    processor3 = processor.Processor("P2")
    processor4 = processor.Processor("P3")
    processors = [processor1, processor2, processor3, processor4]

    memory = main_memory.MainMemory()
    initialize(processors)