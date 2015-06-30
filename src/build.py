'''
Created on 31 août 2011

@author: Laurent
'''

import sys
import subprocess
import os
import locale
from PyQt4 import QtCore, QtGui, uic

form_class, base_class = uic.loadUiType('buildgui.ui')

class Build(form_class, base_class):
    def __init__(self, parent=None):
        super(Build, self).__init__(parent)
        self.setupUi(self)
        self.rootdir = "E:/Documents/ExercicesPrepaSupSpe"
        self.filesystem = QtGui.QFileSystemModel()
        self.tree.setModel(self.filesystem)
        self.tree.setRootIndex(self.filesystem.setRootPath(self.rootdir))
        self.list = set([])
        self.yap = None
        
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_tree_clicked(self, ind):
        path = self.filesystem.filePath(ind)
        if '.tex' in path:
            self.codelatex.setSource(QtCore.QUrl.fromLocalFile(path))

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_tree_doubleClicked(self, ind):
        path = QtCore.QDir(self.rootdir).relativeFilePath(self.filesystem.filePath(ind))
        if '.tex' in path:
            self.exolist.addItem(path)
            self.list.add(path)
            
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_exolist_doubleClicked(self, ind):
        self.list.remove(self.exolist.model().data(ind, 0))
        item = self.exolist.takeItem(self.exolist.currentRow())
        del item
    
    @QtCore.pyqtSlot()
    def on_build_clicked(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Sauvegarder", "C://Users/Laurent/Documents", "LaTeX Files (*.tex)")
        if filename == "":
            return
        titre, ok = QtGui.QInputDialog.getText(self, "Titre du TD", "")
        if titre == "" or not ok:
            return
        if self.combo.currentText() == "TD":
            with open(filename, 'w') as f:
                f.write("\\documentclass{tdprepa}\n")
                f.write("\\usepackage{mylkcz}\n")
                f.write("\\begin{document}\n")
                f.write("\\Opensolutionfile{indics}\n")
                f.write("\\Opensolutionfile{sols}\n")
                f.write("\\titretd{" + titre + "}\n")
                f.write("\\Dossier{C:/Users/Laurent/documents/ExercicesPrepaSupSpe}\n")
                for name in self.list:
                    pos = name.find('.tex')
                    f.write("\lireEnonces." + name[:pos - 1] + "(" + name[pos - 1] + ")\n")
                f.write("\\Closesolutionfile{indics}\n")        
                f.write("\\Closesolutionfile{sols}\n")
                f.write("\\section*{Indications pour les exercices}\n")
                f.write("\\Readsolutionfile{indics}\n")
                f.write("\\end{document}")
            QtGui.QMessageBox.information(self, "Sauvegarde", "Fichier " + filename + " sauvegardé avec succès")
            pos = filename.find('.tex')
            corname = filename[:pos] + "_corrige.tex"
            with open(corname, 'w') as f:
                f.write("\\documentclass{corrigetdprepa}\n")
                f.write("\\usepackage{mylkcz}\n")
                f.write("\\begin{document}\n")
                f.write("\\titretd{" + titre + " (corrigé)}\n")
                f.write("\\input{sols}\n")
                f.write("\\end{document}")
            QtGui.QMessageBox.information(self, "Sauvegarde", "Fichier " + corname + " sauvegardé avec succès")
        elif self.combo.currentText() == "Devoir":
            with open(filename, 'w') as f:
                f.write("\\documentclass{devoirprepa}\n")
                f.write("\\usepackage{mylkcz}\n")
                f.write("\\begin{document}\n")
                f.write("\\Opensolutionfile{indics}\n")
                f.write("\\Opensolutionfile{sols}\n")
                f.write("\\Opensolutionfile{pbsols}\n")
                f.write("\\titredevoir{" + titre + "}\n")
                f.write("\\Dossier{C:/Users/Laurent/documents/ExercicesPrepaSupSpe}\n")
                for name in self.list:
                    pos = name.find('.tex')
                    f.write("\lireEnonces." + name[:pos - 1] + "(" + name[pos - 1] + ")\n")
                f.write("\\Closesolutionfile{indics}\n")        
                f.write("\\Closesolutionfile{sols}\n")
                f.write("\\Closesolutionfile{pbsols}\n")
                f.write("\\end{document}")
            QtGui.QMessageBox.information(self, "Sauvegarde", "Fichier " + filename + " sauvegardé avec succès")
            pos = filename.find('.tex')
            corname = filename[:pos] + "_corrige.tex"
            with open(corname, 'w') as f:
                f.write("\\documentclass{corrigedevoirprepa}\n")
                f.write("\\usepackage{mylkcz}\n")
                f.write("\\begin{document}\n")
                f.write("\\titredevoir{" + titre + " (corrigé)}\n")
                f.write("\\input{sols}\n")
                f.write("\\input{pbsols}\n")
                f.write("\\end{document}")
            QtGui.QMessageBox.information(self, "Sauvegarde", "Fichier " + corname + " sauvegardé avec succès")
        elif self.combo.currentText() == "Colle":
            with open(filename, 'w') as f:
                f.write("\\documentclass{colleprepa}\n")
                f.write("\\usepackage{mylkcz}\n")
                f.write("\\begin{document}\n")
                f.write("\\Opensolutionfile{indics}\n")
                f.write("\\Opensolutionfile{sols}\n")
                f.write("\\titrecolle{" + titre + "}\n")
                f.write("\\Dossier{C:/Users/Laurent/documents/ExercicesPrepaSupSpe}\n")
                for name in self.list:
                    pos = name.find('.tex')
                    f.write("\lireEnonces." + name[:pos - 1] + "(" + name[pos - 1] + ")\n")
                f.write("\\Closesolutionfile{indics}\n")        
                f.write("\\Closesolutionfile{sols}\n")
                f.write("\\end{document}")
            QtGui.QMessageBox.information(self, "Sauvegarde", "Fichier " + filename + " sauvegardé avec succès")
            
    @QtCore.pyqtSlot()
    def on_clear_clicked(self):
        self.list.clear()
        self.exolist.clear()
        
    @QtCore.pyqtSlot()
    def on_view_clicked(self):
        path = self.filesystem.filePath(self.tree.currentIndex())
        if '.tex' not in path:
            return
        with open("C://Temp/temp.tex", 'w') as temp:
            temp.write("\\documentclass{article}\n")
            temp.write("\\usepackage{mylkcz}\n")
            temp.write("\\begin{document}\n")
            temp.write("\\newenvironment{exo}[2]{#2\hfill Difficulté : #1\\newline}{}\n")
            temp.write("\\newenvironment{ind}{Indication\\newline}{}")
            temp.write("\\newenvironment{sol}{Solution\\newline}{}")
            temp.write("\\newenvironment{bigsol}{Solution\\newline}{}")
            with open(path, 'r') as f:
                temp.write(f.read())
            temp.write("\\end{document}")
        os.chdir("C://Temp")
        process = subprocess.Popen(["latex", "C://Temp/temp.tex"])
        process.wait()
        if self.yap != None and self.yap.poll() == None:
            self.yap.kill()
        self.yap = subprocess.Popen(["yap", "C://Temp/temp.dvi"])
        
if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    app = QtGui.QApplication(sys.argv)
    mybuild = Build()
    mybuild.show()
    sys.exit(app.exec_())
