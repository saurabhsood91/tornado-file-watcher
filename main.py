import tornado.ioloop
import tornado.web
from concurrent import futures
from settings import WATCH_DIRECTORIES
import logging
import pyinotify
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import argparse
import os

def make_app():
    return tornado.web.Application()

# class FileWatcher(object):
#     executor = futures.ThreadPoolExecutor(max_workers=1)
#     @tornado.concurrent.run_on_executor
#     def run(self):
#         tornado.ioloop.IOLoop.instance().add_callback(self.run)

class StartWatchDog(object):
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        # watch a set of directories
        for directory in WATCH_DIRECTORIES:
            event_handler = LoggingEventHandler()
            observer = Observer()
            observer.schedule(event_handler, directory, recursive=False)
            observer.start()

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print 'Creating: ', event.pathname
    def process_IN_DELETE(self, event):
        print 'Removing: ', event.pathname

class StartPyINotify(object):
    def __init__(self):
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE
        handler = EventHandler()
        notifier = pyinotify.Notifier(wm, handler)

        for directory in WATCH_DIRECTORIES:
            wm.add_watch(directory, mask, rec=False)
        notifier.loop()

if __name__ == '__main__':
    # Parse arguments and instantiate appropriate watcher
    parser = argparse.ArgumentParser(description='Notifier to use')
    parser.add_argument('--notifier', help='Either (pyinotify, watchdog)')
    args = parser.parse_args()

    # get watch directories from environment variables
    watch_dirs = os.environ.get('WATCHDIRS')
    if watch_dirs:
        WATCH_DIRECTORIES = watch_dirs.split(';')

    if args.notifier == 'pyinotify':
        instance = StartPyINotify()
    else:
        instance = StartWatchDog()

    app = make_app()
    app.listen(8888)
    # tornado.ioloop.IOLoop.instance().add_callback(instance.run)
    tornado.ioloop.IOLoop.current().start()
