import sys
import os
current_dir = os.path.dirname(sys.argv[0])
lib_dir = os.path.join(current_dir, "lib")
sys.path.append(lib_dir)
os.environ['path'] += ';./lib'


# �ն����д��exe����
# pyinstaller main.py --noconsole --hidden-import PySide2.QtXml --runtime-hook="runtimehook.py"

# Ȼ��
# �½�һ����Ϊ lib ��Ŀ¼���ѳ�������ļ����ļ�֮������������ļ����ŵ�libĿ¼���档
# base_library.zip
# main.exe
# main .exe.manifest
# python37.dll

