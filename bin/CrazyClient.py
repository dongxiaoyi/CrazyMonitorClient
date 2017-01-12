#_*_coding:utf-8_*_
import sys
sys.path.append("..")
from core import main


if __name__ == "__main__":
    client = main.command_handler(sys.argv)