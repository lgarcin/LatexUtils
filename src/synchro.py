'''
Created on 22 nov. 2012

@author: Laurent
'''
import fnmatch
import os
import shutil

fromdir = 'C:/Users/Laurent/Documents/ExercicesPrepaSupSpe'
todir = 'C:/Users/Laurent/Dropbox/ExercicesPrepaSupSpe'
os.chdir(fromdir)
for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*LG*.*'):
        fromfile = os.path.normpath(os.path.join(root, filename))
        tofile = os.path.normpath(os.path.join(todir, root, filename))
        shutil.copy2(fromfile, tofile)
        
print('Fichiers copiés')
