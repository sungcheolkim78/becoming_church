#!/usr/local/bin/python3

from py_kbible import kbible
import sys

if len(sys.argv) < 2:
    print("... Usgae: {} day [bible_version]".format(sys.argv[0]))
    sys.exit(1)

if len(sys.argv) == 2:
    bible_version = "개역개정판성경"

if len(sys.argv) == 3:
    bible_version = sys.argv[2]

yaml_file = "./yaml_40days/day{}.yaml".format(sys.argv[1])

kbible.make_mdpage(bible_version, yaml_file, save_dir="./md_40days")

