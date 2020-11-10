import sys
import os
current_dir = os.path.dirname(sys.argv[0])
lib_dir = os.path.join(current_dir, "lib")
sys.path.append(lib_dir)
os.environ['path'] += ';./lib'


