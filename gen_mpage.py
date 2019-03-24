#!/usr/local/bin/python3

from py_kbible import kbible
import sys

if len(sys.argv) != 3:
    print("... Usgae: {} bible_version yaml_file".format(sys.argv[0]))
    sys.exit(1)

bible_version = sys.argv[1]
yaml_file = sys.argv[2]

kbible.make_mdpage(bible_version, yaml_file, save=True)

