import sys
from src.__init__ import *

if __name__ == "__main__":
    clear()
    banner()
    while True:
        try:
            major = Major()
            major.main()
        except KeyboardInterrupt:
            log(mrh + f"Interrupted by users, exiting..")
            sys.exit()