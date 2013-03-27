'''
Created on 7 sept. 2011

@author: Laurent
'''

import re
import os
import glob

os.chdir("C://Users/Laurent/Documents/Enseignement/SaintEx/Maple/TDMaple09")

for filename in glob.glob("*.tex"):
    with open(filename,"r") as f:
        s=f.read()
        groups=re.findall(r"\\begin{maplegroup}.*?\\end{maplegroup}",s,re.DOTALL)
        for group in groups:
            newgroup=group;
            inputs=re.findall(r"\\begin{mapleinput}.*?\\end{mapleinput}",group,re.DOTALL)
            for inp in inputs:
                newinput=inp
                inlines=re.findall(r"\\mapleinline{active}{1d}{.*?}\s*{\s*}",inp,re.DOTALL)
                for inline in inlines:
                    newinline=inline
                    newinline=re.sub(r"^\\mapleinline{active}{1d}{","",newinline)
                    newinline=re.sub(r"}\s*{\s*}$","",newinline)
                    newinline=newinline.replace("\{","{").replace("\}","}")
                    newinline=re.sub(r"\\ts\s*","  ",newinline)
                    newinput=newinput.replace(inline,newinline,1)
                newinput=re.sub(r"^\\begin{mapleinput}","",newinput)
                newinput=re.sub(r"\\end{mapleinput}$","",newinput)
                newgroup=newgroup.replace(inp,newinput,1)
            newgroup=re.sub(r"^\\begin{maplegroup}",r"\\begin{maple}",newgroup)
            newgroup=re.sub(r"\\end{maplegroup}$",r"\\end{maple}",newgroup)
            s=s.replace(group,newgroup,1)
        s=re.sub(r"\\begin{maple}\s*",r"\\begin{maple}\n",s,re.DOTALL)
        s=re.sub(r"\s*\\end{maple}",r"\n\\end{maple}",s,re.DOTALL)
        
    with open(filename,"w") as f:
        f.write(s)