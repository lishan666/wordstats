import sys
import os
current_dir = os.path.dirname(sys.argv[0])
lib_dir = os.path.join(current_dir, "lib")
sys.path.append(lib_dir)
os.environ['path'] += ';./lib'


# 终端运行打包exe命令
# pyinstaller main.py --noconsole --hidden-import PySide2.QtXml --runtime-hook="runtimehook.py"

# 然后：
# 新建一个名为 lib 的目录，把除了下面的几个文件之外的所有其他文件都放到lib目录里面。
# base_library.zip
# main.exe
# main .exe.manifest
# python37.dll

