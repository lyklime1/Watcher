import time
import datetime
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
DEFAULT_OBSERVER_TIMEOUT = 1


def copy(event):
    shutil.copyfile(event.src_path, os.path.join(path_rep, os.path.basename(event.src_path)))


def delete(event):
    file = os.path.join(path_rep, os.path.basename(event.src_path))
    if os.path.exists(file):
        os.remove(file)


def log(event):
    if os.path.exists(path_log):
        with open(path_log, 'a') as log_f:
            log_f.write(f"{event.src_path} {event.event_type} {datetime.datetime.now()}\n")
    else:
        with open(path_log, 'w') as log_f:
            log_f.write(f"{event.src_path} {event.event_type} {datetime.datetime.now()}\n")


class Handler(LoggingEventHandler):

    def on_modified(self, event):
        log(event)
        copy(event)

    def on_created(self, event):
        self.on_modified(event)

    def on_deleted(self, event):
        log(event)
        delete(event)


if __name__ == '__main__':
    path_temp = input('Enter absolute path to directory-temlpate:\n')
    path_rep = input('Enter absolute path to directory-replica:\n')
    DEFAULT_OBSERVER_TIMEOUT = int(input('Enter synchronisation interval in seconds:\n'))
    path_log = os.path.join(input('Enter absolute path to directory for log-file:\n'), 'log.txt')

    # for f in os.listdir(path_temp):
    #     shutil.copyfile(os.path.join(path_temp, f), path_rep)

    if os.path.exists(path_log):
        os.remove(path_log)
    observer = Observer()
    observer.schedule(Handler(), path=path_temp, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
