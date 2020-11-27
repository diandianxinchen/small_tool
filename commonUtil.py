import os

def changeDir(name):
    if (os.path.exists(name) == False):
        os.mkdir(name)
    os.chdir(name)
    print('当前工作目录为：' + os.getcwd())

