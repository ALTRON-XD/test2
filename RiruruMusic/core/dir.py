import sys

from os import remove, listdir, mkdir
from RiruruMusic.logging import LOGGER


def dirr():
    if "assets" not in listdir("RiruruMusic"):
        LOGGER(__name__).warning("Assets Folder not Found. Please clone repository again.")
        sys.exit()

    for file in listdir():
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            remove(file)

    if "downloads" not in listdir():
        mkdir("downloads")
    if "cache" not in listdir():
        mkdir("cache")
    LOGGER(__name__).info("All Folders & Plug-ins Loaded!")
