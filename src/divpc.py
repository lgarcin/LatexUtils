# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 22:33:07 2012

@author: Laurent
"""

from sympy import *

X = Symbol('X')

def valuation(poly):
    for k in range(0,poly.degree()+1):
        if(poly.nth(k)!=0):
            return k
    return None
    
def polystring(poly,order):
    s=""
    val=True
    for k in range(0,order+1):
        l=poly.nth(k)
        if(l==0):
            s+="&&"
        else:
            if(l<0):
                s+="&-&"
            elif(l>0):
                if val:
                    s+="&&"
                else:
                    s+="&+&"
            val=False
            s+=latex(Poly("X**"+str(k),X)*Abs(l))
    return s;

def divpc(A,B,p,truncate=True):
    Q=Poly(0,X)
    R=A
    listpoly=[]
    for k in range(0,p+1):
        l=R.nth(k)/B.nth(0)
        Q=Q+l*X**k
        M=B*X**k*l
        R=R-M
        if(l!=0):
            listpoly.append((M,R))
    if(truncate):
        order=p
    else:
        order=max(p,R.degree());
    s="\\begin{array}{l"+"r"*(2*(order+1)+1)+"|l}\n"
    s+=polystring(A,order)+"&&"+latex(B,order="old")+"\\\\\n"
    s+="\\cline{"+str(2*order+5)+"-"+str(2*order+5)+"}\n"
    lastrem=A
    init=True
    for M,R in listpoly:
        s+="\ominus"+polystring(M,order)+"&&"
        if(init):
            s+=latex(Q,order="old")
            init=False
        s+="\\\\\n"
        first=3+2*valuation(M)
        if(M.EC()<0):
            first-=1;
        last=2*max(M.degree(),lastrem.degree())+3
        if(truncate):
            last=min(last,2*p+3)
        s+="\\cline{"+str(first)+"-"+str(last)+"}\n"
        s+=polystring(R,order )+"&&\\\\\n"
        lastrem=R
    s+="\end{array}"
    return s


A = Poly(X**2-1,X)
B = Poly(X-1,X)
p = 3;

print(divpc(A,B,p,False))
