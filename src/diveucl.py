# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 21:33:38 2012

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
        l=poly.nth(order-k)
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
            s+=latex(Poly("X**"+str(order-k),X)*Abs(l))
    return s;

def diveucl(A,B):
    Q=Poly(0,X)
    R=A
    listpoly=[]
    while R.degree()>=B.degree():
        D=Poly("X**"+str(R.degree()-B.degree()),X)*R.LC()/B.LC()
        Q=Q+D
        M=B*D
        R=R-B*D
        listpoly.append((M,R))
    order=A.degree()
    s="\\begin{array}{l"+"r"*(2*(order+1)+1)+"|l}\n"
    s+=polystring(A,order)+"&&"+latex(B)+"\\\\\n"
    s+="\\cline{"+str(2*order+5)+"-"+str(2*order+5)+"}\n"
    lastrem=A
    init=True
    for M,R in listpoly:
        s+="\ominus"+polystring(M,order)+"&&"
        if(init):
            s+=latex(Q)
            init=False
        s+="\\\\\n"
        first=3+2*(order-M.degree())
        if(M.LC()<0):
            first-=1;
        last=2*(order-min(valuation(M),valuation(lastrem)))+3
        s+="\\cline{"+str(first)+"-"+str(last)+"}\n"
        s+=polystring(R,order )+"&&\\\\\n"
        lastrem=R
    s+="\end{array}"
    return s

A = Poly(X**3-1,X)
B = Poly(X-1,X)

print(diveucl(A,B))
        