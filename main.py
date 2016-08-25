import tornado.ioloop
import tornado.web
from threading import Thread
from settings import watch_directories
import logging

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def make_app():
    return tornado.web.Application()

class StartWatchDog(Thread):
    def run(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        # watch a set of directories
        for directory in watch_directories:
            event_handler = LoggingEventHandler()
            observer = Observer()
            observer.schedule(event_handler, directory, recursive=False)
            observer.start()

class StartPyINotify(Thread):
    def run(self):
        pass


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    # start the Watchdog
    watchdog_instance = StartWatchDog()
    watchdog_instance.start()
    tornado.ioloop.IOLoop.current().start()
