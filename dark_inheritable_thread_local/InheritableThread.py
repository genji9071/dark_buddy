import copy
import threading
from threading import current_thread

from config.ThreadLocalSource import dark_local


class InheritableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.parent = current_thread()
        try:
            self.parent_local = copy.deepcopy(dark_local.__dict__)
        except KeyError:
            self.parent_local = {}
        threading.Thread.__init__(self, *args, **kwargs)
