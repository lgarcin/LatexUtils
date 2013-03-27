'''
Created on 23 oct. 2011

@author: Laurent
'''

import sys
import re
import locale
from PyQt4 import QtGui

class LatexPb(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LatexPb, self).__init__(parent)
        filenames = QtGui.QFileDialog.getOpenFileNames(self, "Ouvrir", "C://Users/Laurent/Documents", "LaTeX Files (*.tex)")

        for filename in filenames:
            with open(filename, "r") as f:
                s = f.read()
                parties = re.findall(r"\\begin{partie}.*?\\end{partie}", s, re.DOTALL)
                for partie in parties:
                    newpartie = partie
                    ind = str.find(partie, "\Qn")
                    if ind != -1:
                        while ind != -1:
                            nextind = str.find(partie, "\Qn", ind + 1)
                            if nextind == -1:
                                nextind = str.find(partie, "\end{partie}", ind + 1)
                            qn = partie[ind:nextind]
                            if str.find(qn, "\qn") != -1:
                                newqn = qn.replace("\qn", "\\begin{question}\n\\item", 1).replace("\qn", "\\item")
                                newqn += ("\n\\end{question}\n")
                                newpartie = newpartie.replace(qn, newqn, 1)
                            ind = nextind
                        newpartie = newpartie.replace("\Qn", "\\begin{question}\n\\item", 1).replace("\Qn", "\\item")
                        newpartie = newpartie.replace("\end{partie}", "\\end{question}\n\\end{partie}")
                        s = s.replace(partie, newpartie, 1)
                with open(filename, "w") as f:
                    f.write(s)
        sys.exit(1)

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    app = QtGui.QApplication(sys.argv)
    latexpb = LatexPb()
    latexpb.show()
    sys.exit(app.exec_())
