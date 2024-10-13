# encoding :utf-8
import sys
from py_func.gen_db import GenerateDB

gdb = GenerateDB( sys.argv[1], True )
gdb.gen_db()
