import threading
import time


class StoppableThread(threading.Thread):

    def __init__(self, main_func, *args, daemonic=False):
        super().__init__(target=main_func, args=args)
        self.setDaemon(daemonic)

    def boot_up(self):
        self.start()

    def shut_down(self, timeout: float = None):
        self.join(timeout=timeout)


if __name__ == '__main__':
    x = time.perf_counter()

    a = StoppableThread(lambda: time.sleep(2), daemonic=True)
    a.boot_up()
    a.shut_down(1)

    print(time.perf_counter() - x)

    x = time.perf_counter()

    a = StoppableThread(lambda: time.sleep(0.5), daemonic=True)
    a.boot_up()
    a.shut_down(1)

    print(time.perf_counter() - x)
