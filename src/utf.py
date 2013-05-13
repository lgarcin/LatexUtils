'''
Created on 11 mai 2013

@author: Laurent
'''

import glob, os


for name in glob.glob("E:/Documents/Probabilites/*.tex"):
    with open(name,"r") as f:
        s=f.read()
        with open(os.path.join("E:/Documents/ExercicesPrepaSupSpe/Probabilites",os.path.basename(name)),"w",encoding="utf-8") as ff:
            ff.write(s)