# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CVThermoDialog
                                 A QGIS plugin
 Construit les segments de route décrits dans le fichier re0


 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Manuel Collongues
        email                : manuel.collongues@cerema.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox

from qgis.core import QgsMessageLog, Qgis, QgsProject, QgsMapLayer, QgsGeometry, QgsVectorLayer, QgsField, QgsFeature, QgsPointXY

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'CVThermo_dialog_base.ui'))


class CVThermoDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CVThermoDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.pushButton_convertir.clicked.connect(self.convertir_re0)
        self.pb_charger_re1.clicked.connect(self.charger_re1)
        self.pb_charger_csv.clicked.connect(self.charger_csv_zones_a_risque)
        self.pb_zones_a_risque.clicked.connect(self.traitement_zones_a_risque)
    
    def charger_re1(self):
        self.filename_re1, _filter = QFileDialog.getOpenFileName(self, "Selectionner fichier thermoroute", "", "(*.re1)")
        self.line_fichier_re1.setText(self.filename_re1)
        self.nom_court_re1 = self.filename_re1.split("/")[-1].split(".")[0]
        QgsMessageLog.logMessage(f"Fichier {self.filename_re1} sélectionné", "Thermoroute", level=Qgis.Info)
        with open(self.filename_re1, "r", encoding="utf-8") as f:
            self.points = []
            premiereLigne = True
            for ligne in f:
                if not premiereLigne:
                    abd, xdeb, ydeb, zdeb, tsurf, tair, hair, vitesse, altitude, td, prt5 = ligne.split("\n")[0].split("\t")
                    point = {}
                    point["geom"] = QgsPointXY(float(xdeb), float(ydeb))
                    point["absc"] = int(float(abd))
                    self.points.append(point)
                    #QgsMessageLog.logMessage(f"Point à l'abscisse {point['absc']} : coordonnées : {float(xdeb)}, {float(ydeb)}", "Thermoroute", level=Qgis.Info)
                else:
                    premiereLigne = False
            QgsMessageLog.logMessage(f"Lecture du fichier {self.filename_re1} terminée", "Thermoroute", level=Qgis.Info)

    def charger_csv_zones_a_risque(self):
        self.filename_csv, _filter = QFileDialog.getOpenFileName(self, "Selectionner fichier thermoroute", "", "(*.csv)")
        self.line_fichier_risque.setText(self.filename_csv)
        if not self.filename_csv or self.filename_csv == "":
            return
        QgsMessageLog.logMessage(f"Fichier {self.filename_csv} sélectionné", "Thermoroute", level=Qgis.Info)
        with open(self.filename_csv, "r", encoding="ansi") as f:
            self.sections = []
            for ligne in f:
                donnees = ligne.split("\n")[0].split(";")
                if len(donnees) == 15:
                    section = donnees[1]
                    code_risque = donnees[14]
                    debut_section = section.split(" ")[2]
                    fin_section = section.split(" ")[4].split("m")[0]
                    self.sections.append({"debut": int(float(debut_section)), "fin": int(float(fin_section)), "code_risque": int(float(code_risque))})
                    QgsMessageLog.logMessage(f"Section de {debut_section} à {fin_section} m : code risque = {code_risque}", "Thermoroute_detail", level=Qgis.Info)
            QgsMessageLog.logMessage(f"Lecture du fichier {self.filename_csv} terminée", "Thermoroute", level=Qgis.Info)

    def traitement_zones_a_risque(self):
        nouvellesEntites = []
        for i, section in enumerate(self.sections):
            list_vertex = []
            for point in self.points:
                if point["absc"] >= section['debut'] and point["absc"] <= section['fin']:
                    list_vertex.append(point["geom"])
            outFeature = QgsFeature()
            outFeature.setGeometry(QgsGeometry.fromPolylineXY(list_vertex))
            outFeature.setAttributes([i, section['debut'], section['fin'], section['code_risque']])
            nouvellesEntites.append(outFeature)
        QgsMessageLog.logMessage(f"Regroupement des sections par zone de risque terminé", "Thermoroute", level=Qgis.Info)
        
        # Chargement dans une couche mémoire du canvas des polylignes correspondantes à chaque section
        vrisque = QgsVectorLayer("Linestring?crs=EPSG:2154", self.nom_court_re1 + " - zones à risque", "memory")
        prov = vrisque.dataProvider()
        prov.addAttributes([QgsField('num_section', QVariant.Int), 
                            QgsField('debut_section', QVariant.Int), 
                            QgsField('fin_section', QVariant.Int), 
                            QgsField('code_risque', QVariant.Int)])
        vrisque.updateFields()
        prov.addFeatures(nouvellesEntites)
        vrisque.updateExtents()
        QgsProject.instance().addMapLayer(vrisque)

        vrisque.loadNamedStyle(os.path.dirname(__file__) + '/styles/zones_risque.qml')
        vrisque.triggerRepaint()
        QgsMessageLog.logMessage(f"Chemin du style : {os.path.join(os.path.dirname(__file__),'styles', 'zones_risque.qml')}", "Thermoroute", level=Qgis.Info)
        


    def convertir_re0(self):
        self.filename_re0, _filter = QFileDialog.getOpenFileName(self, "Selectionner fichier thermoroute", "", "(*.re0)")
        self.line_fichier_re0.setText(self.filename_re0)
        if not self.filename_re0 or self.filename_re0 == "":
            return
        
        nom_court = self.filename_re0.split("/")[-1].split(".")[0]
        

        nouvellesEntites = []
        with open(self.filename_re0, "r", encoding="utf-8") as f:
            premiereLigne = True
            ind = 0
            for ligne in f:
                if not premiereLigne:
                    abd, xdeb, ydeb, zdeb, tsurf, tair, hair, vitesse, altitude, td, prt5 = ligne.split("\n")[0].split("\t")
                    if ind > 0:
                        if float(abd) - float(abd_prec) == 50:
                            outFeature = QgsFeature()
                            outFeature.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(float(x_prec), float(y_prec)), QgsPointXY(float(xdeb), float(ydeb))]))
                            outFeature.setAttributes([ind, int(float(abd_prec)), float(xdeb), float(ydeb), float(x_prec), float(y_prec), float(tsurf_prec), float(td_prec)])
                            nouvellesEntites.append(outFeature)
                    x_prec = xdeb
                    y_prec = ydeb
                    abd_prec = abd
                    tsurf_prec = tsurf
                    td_prec = td
                    ind += 1
                else:
                    premiereLigne = False

            vl = QgsVectorLayer("Linestring?crs=EPSG:2154", nom_court, "memory")
            prov = vl.dataProvider()
            prov.addAttributes([QgsField('id', QVariant.Int), QgsField('ABD', QVariant.Int), QgsField('XFIN', QVariant.Double), QgsField('YFIN', QVariant.Double), QgsField('XDEB', QVariant.Double), QgsField('YDEB', QVariant.Double), QgsField('TSurf', QVariant.Double), QgsField('TD', QVariant.Double)])
            vl.updateFields()
            prov.addFeatures(nouvellesEntites)
            vl.updateExtents()
            QgsProject.instance().addMapLayer(vl)
        
