import queue
import threading


class Bus(object):
    """
    Modificar para que se utilice el bus para buscar en otro cache
    """
    def __init__(self, memory, processors):
        self.memory = memory
        self.caches = []
        for processor in processors:
            self.caches.append(processor.cache)
        self.event_queue = queue.Queue()  # Event queue

        # Start thread to handle events from the queue
        threading.Thread(target=self.handle_events).start()

    def read_main_memory(self, address, cache):
        # Add read event to the event queue
        self.event_queue.put(('read', address, cache))

    def write_main_memory(self, address, data):
        # Add write event to the event queue
        self.event_queue.put(('write', address, data))

    def read_cache(self, address, cache):
        # Add read event to the event queue
        self.event_queue.put(('read_cache', address, cache))

    def handle_events(self):
        while True:
            # Get the next event from the queue
            event = self.event_queue.get()
            operation = event[0]
            address = event[1]
            if operation == 'write':
                data = event[2]
                # Write data to memory
                self.memory.write(address, data)
            elif operation == 'read':
                data = self.memory.read(address)
                cache = event[2]
                # Save data in cache
                cache.write(address, data)
            elif operation == 'read_cache':
                # Read data from each cache
                for cache in self.caches:
                    if cache != event[2]:
                        data = cache.read(address)
                        if data:
                            return data
                    else:
                        pass
                # Read data from memory
                data = self.memory.read(address)
