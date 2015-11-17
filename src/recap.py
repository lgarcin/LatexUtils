'''
Created on 15 juil. 2011

@author: Laurent
'''

import sys
import os
import glob
import re
import json
import time
import subprocess
import locale
from PyQt5 import QtCore, QtWidgets, uic

scriptdir = os.path.dirname(__file__)
form_class, base_class = uic.loadUiType(scriptdir + '/recapgui.ui')

class Recap(form_class, base_class):
    def __init__(self, parent=None):
        super(Recap, self).__init__(parent)
        self.setupUi(self)
        self.rootdir = "F:/Documents/ExercicesPrepaSupSpe"
        self.authors = ["BE", "LG", "LK", "OM"]
        os.chdir(self.rootdir)
        listDirModel = QtCore.QStringListModel()
        dirs=next(os.walk('.'))[1]
        listDirModel.setStringList(dirs)
        self.listView.setModel(listDirModel)
        self.dico = {}
        for name in dirs:
            self.dico[name] = {}
            path=self.rootdir + "/" + name
            os.chdir(path)
            try:
                with open('dictionary.json', 'r', encoding='utf-8') as f:
                    self.dico[name] = json.load(f)
            except IOError:
                self.dico[name] = {}
        self.dir = None
        
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_listView_clicked(self, ind):
        self.dir = self.listView.model().data(ind, 0)
        os.chdir(self.rootdir + "/" + self.dir)
        files = set(glob.glob("*[0-9].tex")).difference(set(glob.glob("PB*")))
        filekeys = {re.sub('(' + '|'.join(self.authors) + ')\d{2}.tex', '', file) for file in files}
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(len(filekeys) + 1)
        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Valeurs extensives"))
        self.tableWidget.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem("Titre"))
        if "Titre" in self.dico[self.dir].keys():
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(self.dico[self.dir]["Titre"]))
        row = 1
        for name in filekeys:
            self.tableWidget.setVerticalHeaderItem(row, QtWidgets.QTableWidgetItem(name))
            if name in self.dico[self.dir].keys():
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(self.dico[self.dir][name]))
            else:
                self.dico[self.dir][name] = ""
            row += 1
        for name in set(self.dico[self.dir].keys()).difference(filekeys):
            if name != "Titre":
                del self.dico[self.dir][name]
            
    @QtCore.pyqtSlot(QtWidgets.QTableWidgetItem)
    def on_tableWidget_itemChanged(self, item):
        self.dico[self.dir][self.tableWidget.verticalHeaderItem(item.row()).data(0)] = item.data(0)
        
    @QtCore.pyqtSlot()
    def on_saveButton_clicked(self):
        if self.dir == None:
            QtWidgets.QMessageBox.information(self, "Erreur", "Sélectionner un dossier avant de sauvegarder")
        else:
            os.chdir(self.rootdir + "/" + self.dir)
            with open('dictionary.json', mode='w', encoding='utf-8') as f:
                json.dump(self.dico[self.dir], f, indent=2)
            QtWidgets.QMessageBox.information(self, "Sauvegarde", "Dictionnaire du dossier " + self.dir + " sauvegardé avec succès")

    @QtCore.pyqtSlot()
    def on_buildButton_clicked(self):
        if self.dir == None:
            QtWidgets.QMessageBox.information(self, "Erreur", "Sélectionner un dossier avant de construire un récapitulatif")
        elif "" in self.dico[self.dir].values():
            QtWidgets.QMessageBox.information(self, "Erreur", "Définir toutes les abréviations avant de construire un récapitulatif")
        else:
            self.saveButton.click()
            recapdir = self.rootdir + "/" + self.dir + "/Recapitulatif"
            if not os.access(recapdir, os.F_OK):
                os.mkdir(recapdir)
            os.chdir(recapdir)
            recapfile = "Recap" + self.dir + ".tex"
            with open(recapfile, mode='w',encoding='utf-8') as f:
                f.write("\\documentclass{recapitulatif}\n")
                f.write("\\usepackage{prepa}\n")
                f.write("\\begin{document}\n")
                f.write("\\pagedegarde{" + self.dico[self.dir]["Titre"] + "}{Exercices et problèmes}{version du " + time.strftime("%d %B %Y", time.localtime()) + "}\n")
                f.write("\\Dossier{..}\n")
                f.write("\\Opensolutionfile{indics}\n")
                f.write("\\Opensolutionfile{sols}\n")
                f.write("\\Opensolutionfile{pbsols}\n")
                f.write("\\tableofcontents\n")
                os.chdir(self.rootdir + "/" + self.dir)
                
                f.write("\n\\Partie{Énoncés des exercices}\n")
                for name in self.dico[self.dir].keys():
                    if name != "Titre":
                        f.write("\n\\Chapitre{" + self.dico[self.dir][name] + "}\n")
                        for author in self.authors:
                            files = glob.glob(name + author + "*.tex")
                            if len(files):
                                f.write("\\section{Exercices de " + author + "}\n")
                                (tens, units) = divmod(len(files), 10)
                                for t in range(tens + 1):
                                    if t == 0:
                                        first = 1
                                    else:
                                        first = 0
                                    if t == tens:
                                        last = units
                                    else:
                                        last = 9
                                    f.write("\\lireEnonces." + name + author + str(t) + "([" + str(first) + "-" + str(last) + "])\n")
                            
                problems = glob.glob("PB*.tex")
                f.write("\n\\Partie{Énoncés des problèmes}\n")
                for file in problems:
                    with open(file, mode='r',encoding='utf-8') as ff:
                        f.write("\\Chapitre{" + re.match('(\\\\begin\s*{\s*pb\s*}\s*{\s*)(.*)(\s*})', ff.read(None)).group(2) + "}\n")
                    ind = file.find(".tex")
                    f.write("\lireEnonces." + file[:ind - 1] + "(" + file[ind - 1] + ")\n")
                        
                f.write("\n\\Closesolutionfile{indics}\n")        
                f.write("\\Closesolutionfile{sols}\n")        
                f.write("\\Closesolutionfile{pbsols}\n")        

                f.write("\n\\Partie{Indications pour les exercices}\n")
                f.write("\\Readsolutionfile{indics}\n")

                f.write("\n\\Partie{Solutions des exercices}\n")
                f.write("\\Readsolutionfile{sols}\n")
                
                f.write("\n\\Partie{Solutions des problèmes}\n")
                f.write("\\Readsolutionfile{pbsols}\n")
                    
                f.write("\n\\end{document}")

            QtWidgets.QMessageBox.information(self, "Récapitulatif", "Récapitulatif du dossier " + self.dir + " sauvegardé avec succès dans le fichier " + recapfile)
            os.chdir(recapdir)
            subprocess.Popen(["C:/Program Files/TeXnicCenter/TeXnicCenter.exe", recapfile])
            
if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    app = QtWidgets.QApplication(sys.argv)
    myrecap = Recap()
    myrecap.show()
    sys.exit(app.exec_())
