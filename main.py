from components import processor, main_memory, bus
import time
import utils
import random
import threading
import tkinter as tk
from tkinter import ttk

def create_cache_visualization():
    # Function to update cache and memory block states
    def update_block_state(block, new_state):
        address = bin(new_state['Address'])[2:]
        if len(address) < 3:
            address = "0" * (3 - len(address)) + address
        txt = f"{new_state['Block']} - {address} - {hex(new_state['Data'])} - {new_state['State']}"
        block.config(text=txt)

    def update_memory(block, new_state):
        address = bin(new_state['Address'])[2:]
        if len(address) < 3:
            address = "0" * (3 - len(address)) + address
        txt = f"{address} - {hex(new_state['Data'])}"
        memory_blocks[block].config(text=txt)

    def update():
        while True:
            for idxC, proc in enumerate(processors):
                for idxB, state in enumerate(proc.get_state()):
                    update_block_state(caches[idxC][idxB], state)
                    root.update()
            for idxB, state in enumerate(memory.get_state()):
                update_memory(idxB, state)



    # Create main window
    root = tk.Tk()
    root.title("Cache Visualization")

    # Create style for cache titles
    cache_title_style = ttk.Style()
    cache_title_style.configure("CacheTitle.TLabel", foreground="white", background="gray", font=("Helvetica", 12, "bold"))

    # Create frame for cache visualizations
    cache_frame = tk.Frame(root)
    cache_frame.pack(side=tk.TOP, padx=10, pady=10)

    # Create cache visualizations in a 2x2 matrix
    caches = [
        [],
        [],
        [],
        []
    ]
    for i in range(2):
        for j in range(2):
            cache = tk.Frame(cache_frame, relief=tk.RAISED, borderwidth=1, width=200, height=200)
            cache.pack(side=tk.LEFT, padx=10, pady=10)

            # Create cache title
            cache_title = ttk.Label(cache, text="Cache {}-{}".format(i+1, j+1), style="CacheTitle.TLabel")
            cache_title.pack(side=tk.TOP, fill=tk.X)

            # Create space for executing instruction
            instruction_label = tk.Label(cache, text="Executing Instruction: ", anchor=tk.W, justify=tk.LEFT, wraplength=180)
            instruction_label.pack(side=tk.TOP, fill=tk.X)

            for k in range(4):
                block = tk.Label(cache, text="Block {}: 0x0000 - FREE".format(k), anchor=tk.W, justify=tk.LEFT, wraplength=180)
                block.pack(side=tk.TOP, fill=tk.X)
                if i == 0:
                    caches[j].append(block)
                else:
                    caches[j+i+1].append(block)

    # Create style for memory blocks
    memory_block_style = ttk.Style()
    memory_block_style.configure("MemoryBlock.TLabel", foreground="black", background="lightgray", font=("Helvetica", 10))

    # Create memory visualization
    memory_label = ttk.Label(root, text="Main Memory", font=("Helvetica", 14, "bold"))
    memory_label.pack()
    memory_frame = ttk.Frame(root)
    memory_frame.pack()
    memory_blocks = []
    for i in range(8):
        block = ttk.Label(memory_frame, text="Block {}: 0x0000 - FREE".format(i), style="MemoryBlock.TLabel")
        block.pack(side=tk.TOP, fill=tk.X)
        memory_blocks.append(block)

    # Create log window
    log_label = ttk.Label(root, text="Log Window", font=("Helvetica", 14, "bold"))
    log_label.pack()
    log_text = tk.Text(root, height=10, width=50)
    log_text.pack(side=tk.BOTTOM, padx=10, pady=10)

    # Create buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM)
    button1 = ttk.Button(button_frame, text="Button 1")
    button1.pack(side=tk.LEFT, padx=5, pady=5)
    button2 = ttk.Button(button_frame, text="Button 2")
    button2.pack(side=tk.LEFT, padx=5, pady=5)
    button3 = ttk.Button(button_frame, text="Button 3")
    button3.pack(side=tk.LEFT, padx=5, pady=5)

    # Function to handle button clicks
    def handle_button_click(button_num):
        log_text.insert(tk.END, "Button {} clicked\n".format(button_num))

        # Function to handle button clicks
    def handle_button1_click():
        handle_button_click(1)

    def handle_button2_click():
        handle_button_click(2)

    def handle_button3_click():
        handle_button_click(3)

    # Bind button click events to their respective handlers
    button1.config(command=handle_button1_click)
    button2.config(command=handle_button2_click)
    button3.config(command=handle_button3_click)

    updt = threading.Thread(target=update)
    updt.start()

    # Start main event loop
    root.mainloop()


def initialize():
    global processors
    while True:
        for proc in processors:
            proc.generate_random_instruction()
            time.sleep(2)




"""
To do:
    - Figure out how to do step by step execution
    - Show Logs in GUI

"""


if __name__ == "__main__":
    processor1 = processor.Processor("P0")
    processor2 = processor.Processor("P1")
    processor3 = processor.Processor("P2")
    processor4 = processor.Processor("P3")
    processors = [processor1, processor2, processor3, processor4]

    memory = main_memory.MainMemory()

    bus = bus.Bus(memory, processors)

    for proc in processors:
        proc.set_bus(bus)
        proc.start()

    x = threading.Thread(target=initialize)
    y = threading.Thread(target=create_cache_visualization)
    y.start()
    x.start()
