import sys
import os
import re


def grep(filename, str):
    # def usage():
    #     print("[Usage]: python grep.py filename grepString.")

    # if len(sys.argv) != 2:
    #     usage()
    #     sys.exit(1)

    if os.path.isfile(filename):
        pass
        sys.exit(2)
    else:
        print(filename)
        f = open(filename)
        content = f.read()
        f.close()
        s = "\n".join(re.findall(str + '.*', content))
        print(s)
