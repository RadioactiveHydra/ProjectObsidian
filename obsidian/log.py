from __future__ import annotations

import time
import traceback
import datetime
import sys
import os

from obsidian.constants import Colour


class Logger:
    DEBUG = False
    VERBOSE = False
    LOGFILE = None

    @staticmethod
    def _getTimestamp():
        return time.strftime("%H:%M:%S", time.localtime())

    @classmethod
    def setupLogFile(cls, logPath=None):
        # Setup LogPath If Not Defined
        if logPath is None:
            logPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        # Ensure File Exists
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        # Open File
        cls.LOGFILE = open(
            os.path.join(
                logPath,
                f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
            ), "a"
        )

    @classmethod
    def log(cls, message, tags=[], colour=Colour.NONE, textColour=Colour.NONE):
        # Generating Message (Add Tags, Message, Format, Etc)
        output = ""
        # Adding Tags
        for tag in tags:
            output += f"[{colour}{tag.upper()}{Colour.RESET}{Colour.BACK_RESET}]"
        # Add Message
        if len(tags) != 0:
            output += f": {textColour}{message}{Colour.BACK_RESET}"
        else:
            output += f"{textColour}{message}{Colour.BACK_RESET}"
        # Log String Into LogFile (If Fail Skip)
        if cls.LOGFILE is not None:
            try:
                # Write Tags
                for tag in tags:
                    cls.LOGFILE.write(f"[{tag.upper()}]")
                # Write Message
                if len(tags) != 0:
                    cls.LOGFILE.write(f": {message}\n")
                else:
                    cls.LOGFILE.write(f"{message}\n")
                # Save File
                cls.LOGFILE.flush()
            except Exception as e:
                print(f"Error While Handing Log Message - {type(e).__name__}: {e}")
        # Print Final String
        print(output)

    @classmethod
    def askConfirmation(cls, message: str = "Do you want to continue?"):
        while True:
            cls.log("")
            # Give user Warning, and ask them for further input
            cls.warn(f"{message} (y/n)", module="confirmation")
            userInput = input()
            if userInput.lower() == "y" or userInput.lower() == "yes":
                cls.log("")
                break
            elif userInput.lower() == "n" or userInput.lower() == "no":
                cls.warn("Ok Exiting...", module="confirmation")
                sys.exit()

    @classmethod
    def info(cls, message, module="unknown"):
        cls.log(
            str(message),
            tags=[cls._getTimestamp(), "log", module],
            colour=Colour.GREEN,
            textColour=Colour.WHITE
        )

    @classmethod
    def warn(cls, message, module="unknown"):
        cls.log(
            str(message),
            tags=[cls._getTimestamp(), "warn", module],
            colour=Colour.YELLOW,
            textColour=Colour.WHITE
        )

    @classmethod
    def error(cls, message, module="unknown", printTb=True):
        if cls.DEBUG and printTb:
            cls.log(f"{traceback.format_exc()}")
        cls.log(
            str(message) + (" | Enable Debug For More Information" if not cls.DEBUG and printTb else ""),
            tags=[cls._getTimestamp(), "error", module],
            colour=Colour.RED,
            textColour=Colour.WHITE
        )

    @classmethod
    def fatal(cls, message, module="unknown", printTb=True):
        if cls.DEBUG and printTb:
            cls.log(f"{traceback.format_exc()}")
        cls.log(
            str(message) + (" | Enable Debug For More Information" if not cls.DEBUG and printTb else ""),
            tags=[cls._getTimestamp(), "fatal", module],
            colour=Colour.BLACK + Colour.BACK_RED,
            textColour=Colour.WHITE
        )

    @classmethod
    def debug(cls, message, module="unknown"):
        if cls.DEBUG:
            cls.log(
                str(message),
                tags=[cls._getTimestamp(), "debug", module],
                colour=Colour.CYAN,
                textColour=Colour.WHITE
            )

    @classmethod
    def verbose(cls, message, module="unknown"):
        if cls.DEBUG and cls.VERBOSE:
            cls.log(
                str(message),
                tags=[cls._getTimestamp(), "verbose", module],
                colour=Colour.MAGENTA,
                textColour=Colour.WHITE
            )
