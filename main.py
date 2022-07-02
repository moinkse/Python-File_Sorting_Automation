import os
import shutil
import time
import logging
from os.path import splitext, exists
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

dest_dir_sfx = "/home/" + os.getlogin() + "/Templates/"
dest_dir_docs = "/home/" + os.getlogin() + "/Documents/"
dest_dir_video = "/home/" + os.getlogin() + "/Videos/"
dest_dir_images = "/home/" + os.getlogin() + "/Pictures/"
dest_dir_music = "/home/" + os.getlogin() + "/Music/"
source_dir = "/home/" + os.getlogin() + "/Downloads/"


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = make_unique(dest, name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            print(os.listdir(source_dir))
            for entry in entries:
                name = entry.name
                if name.endswith(".wav") or name.endswith(".mp3"):
                    if entry.stat().st_size < 25000000 or "SFX" in name:
                        dest = dest_dir_sfx
                    else:
                        dest = dest_dir_music
                    move(dest, entry, name)
                    logging.info(f"Moved document file: {name}")
                elif name.endswith(".mp4") or name.endswith(".avi"):
                    dest = dest_dir_video
                    move(dest, entry, name)
                    logging.info(f"Moved document file: {name}")
                elif name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".png"):
                    dest = dest_dir_images
                    move(dest, entry, name)
                    logging.info(f"Moved document file: {name}")
                elif name.endswith(".pdf") or name.endswith(".txt") or name.endswith(".lyx"):
                    dest = dest_dir_docs
                    move(dest, entry, name)
                    logging.info(f"Moved document file: {name}")


if __name__ == "__main__":
    print(os.listdir(source_dir))
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
