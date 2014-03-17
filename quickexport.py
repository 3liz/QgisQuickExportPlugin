# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickExport
                                 A QGIS plugin
 This plugin adds a toolbar with buttons to export the selected layer data to CSV, HTML and PDF files
                              -------------------
        begin                : 2014-03-17
        copyright            : (C) 2014 by 3liz
        email                : info@3liz.com
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources
import os.path
from functools import partial

class QuickExport:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'quickexport_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):

        # Add Quick Export toolbar
        self.toolbar = self.iface.addToolBar(u'Quick Export');

        # Add toolbar buttons
        ###
        # CSV
        self.exportAsCsvAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/export-csv.svg"),
            QApplication.translate("quickExport", u"Export table as CSV"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.exportAsCsvAction)
        self.toolbar.setObjectName("quickExportAsCsv");

        # HTML
        self.exportAsHtmlAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/export-html.svg"),
            QApplication.translate("quickExport", u"Export table as HTML"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.exportAsHtmlAction)
        self.toolbar.setObjectName("quickExportAsHtml");

        # Connect each button to corresponding slot
        self.exportButtons = {
            'csv': {'action' : self.exportAsCsvAction},
            'html': {'action' : self.exportAsHtmlAction}
        }
        for key, item in self.exportButtons.items():
            action = item['action']
            slot = partial(self.exportLayer, key)
            action.triggered.connect(slot)


    def chooseExportFilePath(self, etype='csv'):
        '''
        Method to allow the user to choose a file path
        to store the exported attribute table
        '''

        # Get data corresponding to chosen file type
        etypeDic = {
            'csv': {'fileType': 'CSV (*.csv *.txt)', 'lastFileSetting': 'lastExportedCsvFile'},
            'html': {'fileType': 'HTML (*.html *.htm)', 'lastFileSetting': 'lastExportedHtmlFile'},
            'pdf': {'fileType': 'PDF (*.pdf)', 'lastFileSetting': 'lastExportedPdfFile'}
        }

        # Get last exported file path
        s = QSettings()
        lastFile = s.value(
            "quickExport/%s" % etypeDic[etype]['lastFileSetting'],
            '',
            type=str
        )

        # Let the user choose new file path
        ePath = QFileDialog.getSaveFileName (
            None,
            QApplication.translate("quickExport", "Please choose the destination file path."),
            lastFile,
            etypeDic[etype]['fileType']
        )
        if not ePath:
            self.iface.messageBar().pushMessage(
                QApplication.translate("quickExport", "Quick Export Plugin"),
                QApplication.translate("quickExport", "Export has been canceled"),
                QgsMessageBar.INFO,
                3
            )
            return None

        # Delete file if exists (question already asked above)
        if os.path.exists(unicode(ePath)):
            os.remove(unicode(ePath))

        # Save file path in QGIS settings
        s.setValue(
            "quickExport/%s" % etypeDic[etype]['lastFileSetting'],
            str(ePath)
        )

        return ePath



    def exportLayer(self, etype='csv'):
        '''
        Export the attribute table of the selected
        vector layer to the chose file type
        '''
        # Get the active layer
        layer = self.iface.activeLayer()
        msg= None

        # Check if the layer is suitable for data export
        if layer and layer.type() == QgsMapLayer.VectorLayer and hasattr(layer, 'providerType'):

            # Ask the user to choose the path
            ePath = self.chooseExportFilePath(etype)

            # Do the export
            if ePath:
                if etype == 'csv':
                    msg, status = self.exportLayerToCsv(layer, ePath)
                elif etype == 'html':
                    msg, status = self.exportLayerToHtml(layer, ePath)
                #~ elif etype == 'pdf':
                    #~ msg = exportLayerToHtml()

        else:
            msg = QApplication.translate("quickExport", "Please select a vector layer first.")
            status = QgsMessageBar.WARNING

        # Display status in the message bar
        if msg:
            self.iface.messageBar().pushMessage(
                QApplication.translate("quickExport", "Quick Export Plugin"),
                msg,
                status,
                3
            )

    def exportLayerToCsv(self, layer, ePath):
        '''
        Exports the layer to CSV
        '''
        provider = layer.dataProvider()
        writer = QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            ePath,
            provider.encoding(),
            layer.crs(),
            "CSV",
            layer.selectedFeatureCount(),
            None,
            [],
            ['GEOMETRY=AS_WKT', 'SEPARATOR=TAB']
        )

        if writer == QgsVectorFileWriter.NoError:
            msg = QApplication.translate("quickExport", "The layer has been successfully exported.")
            status = QgsMessageBar.INFO
        else:
            msg = QApplication.translate("quickExport", "An error occured during layer export.")
            status = QgsMessageBar.CRITICAL

        return msg, status


    def exportLayerToHtml(self, layer, ePath):
        '''
        Exports the layer to HTML
        '''
        return msg, status

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.mainWindow().removeToolBar(self.toolbar)

