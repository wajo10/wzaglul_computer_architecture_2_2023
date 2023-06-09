import queue
import threading
from utils import Logs

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Bus(object):
    """
    Modificar para que se utilice el bus para buscar en otro cache
    """
    def __init__(self, memory, processors, logger: Logs):
        self.memory = memory
        self.logger = logger
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

    def invalidate_cache(self, address, cache_list):
        """
        Invalidates the cache
        :param address: address to invalidate
        :param cache_list:  list of caches to keep the data
        """
        # Add invalidate event to the event queue
        self.event_queue.put(('invalidate', address, cache_list))

    def handle_events(self):
        """
        Handles events from the event queue
        """
        while True:
            # Get the next event from the queue
            event = self.event_queue.get()
            operation = event[0]
            address = event[1]
            if operation == 'write':
                data = event[2]
                # Write data to memory
                self.memory.write(address, data)
                self.event_queue.task_done()
            elif operation == 'read':
                data = self.memory.read(address)
                cache = event[2]
                # Save data in cache
                cache.write(address, data)
                self.event_queue.task_done()
            elif operation == 'read_cache':
                # Read data from each cache
                solicited_cache = event[2]
                read_success = False
                for cache in self.caches:
                    if cache != event[2]:
                        data = cache.read(address)
                        if data is not False:
                            print(f"Read hit, read from cache {cache.name}")
                            self.logger.add_log(f"Read hit, {event[2].name} read from cache {cache.name}")
                            # Save data in cache
                            solicited_cache.write(address, data, True)
                                # self.invalidate_cache(address, [solicited_cache, cache])
                            cache.print_cache()
                            solicited_cache.print_cache()
                            read_success = True
                            self.event_queue.task_done()
                            break
                        else:
                            print(f"Read miss in cache {self.caches.index(cache)}")

                    else:
                        pass
                if not read_success:
                    # Read data from memory
                    data = self.memory.read(address)
                    print("Read miss in all caches, reading from memory")
                    self.logger.add_log(f"Read miss in all caches, {event[2].name} is now reading from memory")
                    # Save data in cache
                    cache = event[2]
                    cache.write_from_memory(address, data)
                    cache.print_cache()
                    self.event_queue.task_done()

            elif operation == 'invalidate':
                # Invalidate data in each cache
                for cache in self.caches:
                    if cache not in event[2]:
                        cache.invalidate(address)
                    else:
                        pass
                self.event_queue.task_done()
