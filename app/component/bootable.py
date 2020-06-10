﻿from abstract.component.bootable import Bootable
import threading

class BootableImpl(Bootable, threading.Thread):
    def __init__(self, main_func, *args, daemonic=False):
        self.running = None

        def wrap(*args):
            while True:
                if self.running.is_set():
                    main_func(*args)
                else:
                    self.running.wait()

        super().__init__(target=wrap, args=args)
        self.setDaemon(daemonic)

    def boot_up(self):
        '''
        在第一次调用时创建线程，之后调用时恢复线程
        '''
        if self.running is None:
            self.running = threading.Event()
            self.running.set()
            self.start()
        else:
            self.running.set()


    def shut_down(self, timeout=0):
        '''
        暂停线程
        '''
        self.running.clear()