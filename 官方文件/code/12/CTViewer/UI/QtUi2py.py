# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:20:19 2019

@author: HP
"""

import os
import os.path

#UI文件所在的路径

dir = './'

#列出目录下的所有UI文件
def listUiFile():
    list = []
    files = os.listdir(dir)
    for filename in files:
        #print(dir + os.sep + f )
        #print(filename)
        if os.path.splitext(filename)[1] == '.ui':
            list.append(filename)
    return list


#把扩展名为.ui的文件改为扩展名为.py的文件
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'

#调用系统命令吧UI文件转为Python文件
def runMain():
    list = listUiFile()
    print(list)
    for uifile in list:
        pyfile = transPyFile(uifile)
        cmd = 'pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyfile,uifile=uifile)
        #print(cmd)

        os.system(cmd)

if __name__=="__main__":
    runMain()