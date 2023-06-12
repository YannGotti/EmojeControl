import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

python = sys.executable
process = subprocess.Popen([python, 'app.py'])

class BotRestartHandler(FileSystemEventHandler):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            global process
            process.kill()
            process.wait()
            process = subprocess.Popen([python, 'app.py'])

            

def start_bot():
    python = sys.executable


def main():
    observer = Observer()
    event_handler = BotRestartHandler(observer)
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    start_bot()

    observer.join()

if __name__ == '__main__':
    main()
