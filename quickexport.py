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
from PyQt4.QtWebKit import *
from qgis.core import *
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources
import os
from functools import partial
import shutil
import datetime
import locale
import tempfile
import sys
import subprocess
import apicompat

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

        self.exportedFile = None

        # PDF print options
        self.maxLinesPerPage = 25
        self.maxAttributesBeforeSmallFontSize = 15
        self.orientation = QPrinter.Landscape
        self.pageSize = QPrinter.A4


    def initGui(self):

        # Add Quick Export toolbar
        self.toolbar = self.iface.addToolBar(u'Quick Export');

        # Add toolbar buttons
        ###
        # CSV
        self.exportToCsvAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/export-csv.png"),
            QApplication.translate("quickExport", u"Export table as CSV"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.exportToCsvAction)
        self.toolbar.setObjectName("quickexportToCsv");

        # HTML
        self.exportToHtmlAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/export-html.png"),
            QApplication.translate("quickExport", u"Export table as HTML"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.exportToHtmlAction)
        self.toolbar.setObjectName("quickexportToHtml");

        # PDF
        self.exportToPdfAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/export-pdf.png"),
            QApplication.translate("quickExport", u"Export table as PDF"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.exportToPdfAction)
        self.toolbar.setObjectName("quickexportToPdf");

        # Printer
        self.exportToPrinterAction = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/export-printer.png"),
            QApplication.translate("quickExport", u"Export table to printer"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.exportToPrinterAction)
        self.toolbar.setObjectName("quickexportToPrinter");

        # Connect each button to corresponding slot
        self.exportButtons = {
            'csv': {'action' : self.exportToCsvAction},
            'html': {'action' : self.exportToHtmlAction},
            'pdf': {'action' : self.exportToPdfAction},
            'printer': {'action' : self.exportToPrinterAction}
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

        self.exportedFile = ePath
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
            if etype != 'printer':
                self.chooseExportFilePath(etype)
                if self.exportedFile:
                    if etype == 'csv':
                        msg, status = self.exportLayerToCsv(layer)
                    elif etype == 'html':
                        msg, status = self.exportLayerToHtml(layer)
                    elif etype == 'pdf':
                        msg, status = self.exportLayerToPdf(layer)

            else:
                msg, status = self.exportLayerToPdf(layer, True)

        else:
            msg = QApplication.translate("quickExport", "Please select a vector layer first.")
            status = QgsMessageBar.WARNING

        # Display status in the message bar
        if msg:
            widget = self.iface.messageBar().createMessage(msg)
            # Add a button to open the file
            if self.exportedFile and status == QgsMessageBar.INFO and etype != 'printer':
                btOpen = QPushButton(widget)
                btOpen.setText(QApplication.translate("quickExport", "Open file"))
                btOpen.pressed.connect(self.openFile)
                widget.layout().addWidget(btOpen)
            # Display message bar
            self.iface.messageBar().pushWidget(
                widget,
                status,
                6
            )


    def exportLayerToCsv(self, layer):
        '''
        Exports the layer to CSV

        '''
        QApplication.setOverrideCursor(Qt.WaitCursor)
        provider = layer.dataProvider()
        writer = QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            self.exportedFile,
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

        QApplication.restoreOverrideCursor()

        return msg, status


    def exportLayerToHtml(self, layer, ePath=None, cutPages=False):
        '''
        Exports the layer to HTML
        using a template and reading the data
        from the selected layer
        '''
        # Get template file path
        tplPath = os.path.join(
            self.plugin_dir,
            "templates/htmlTemplate.tpl"
        )
        cssPath = os.path.join(
            self.plugin_dir,
            "templates/table.css"
        )

        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Read template file
        fin = open(tplPath)
        data = fin.read().decode('utf-8')
        fin.close()

        # Get layer fields names
        fieldNames = [field.name() for field in layer.pendingFields() ]

        # Create thead with attribute names
        thead = '                <tr>\n'
        for field in fieldNames:
            thead+= '                    <th>%s</th>\n' % field
        thead+= '                </tr>\n\n'

        # Get selected features or all features
        if layer.selectedFeatureCount():
            features = layer.selectedFeatures()
            nb = layer.selectedFeatureCount()
        else:
            features = layer.getFeatures()
            nb = layer.featureCount()

        # Create tbody content with feature attribute data
        tbody = ''
        nbAttr = 0
        i = 0
        page = 1
        for feat in features:
            tbody+= '                <tr>\n'
            # Get attribute data
            attrs = feat.attributes()
            nbAttr = len(attrs)
            tbody+= '                    <td>'
            tbody+= '</td>\n                    <td>'.join([u"%s" % a for a in attrs])
            tbody+= '                    </td>\n'
            tbody+= '                </tr>\n\n'
            i+=1
            if i == self.maxLinesPerPage and cutPages:
                i = 0
                tbody+= '</table>\n\n'
                tbody+= '<span style="float:right;">Page %s</span>' % page
                tbody+= '<div style="page-break-before:always;"></div>\n\n'
                tbody+= '<table><thead>' + thead + '</thead><tbody>'
                page+=1


        # Date
        locale.setlocale(locale.LC_TIME,'')
        date_format = locale.nl_langinfo(locale.D_T_FMT)
        today = datetime.datetime.today()
        date = today.strftime(date_format)
        dt_date = QApplication.translate("quickExport", "Generated by QGIS QuickExport plugin")

        # Title, abstract, and line count
        dt_title = QApplication.translate("quickExport", "Layer")
        title = layer.title() and layer.title() or layer.name()
        dt_abstract = QApplication.translate("quickExport", "Abstract")
        abstract = layer.abstract() and str(layer.abstract()) or '-'
        dt_info = QApplication.translate("quickExport", "Information")
        info = QApplication.translate("quickExport", "{} lines exported").format(str(nb))

        # Adapt style if needed
        style = ''
        if nbAttr > self.maxAttributesBeforeSmallFontSize:
            style = 'th, td {font-size:small;}'
            self.maxLinesPerPage = 40

        # Replace values
        data = data.replace('$dt_title', dt_title)
        data = data.replace('$title', title)
        data = data.replace('$dt_abstract', dt_abstract)
        data = data.replace('$abstract', abstract)
        data = data.replace('$dt_info', dt_info)
        data = data.replace('$info', info)
        data = data.replace('$thead', thead)
        data = data.replace('$tbody', tbody)
        data = data.replace('$dt_date', dt_date)
        data = data.replace('$date', date)
        data = data.replace('$style', style)
        data = data.replace('$totalPages', "Page %s" % page)

        # File path
        if not ePath:
            ePath = self.exportedFile

        try:
            # write html content
            f = open(ePath, 'w')
            f.write(data.encode('utf-8'))
            f.close()

        except IOError, e:
            msg = QApplication.translate("quickExport", "An error occured during layer export.")
            status = QgsMessageBar.CRITICAL
        finally:
            msg = QApplication.translate("quickExport", "The layer has been successfully exported.")
            status = QgsMessageBar.INFO

        # copy css file in the exported file folder
        try:
            shutil.copy2(cssPath, os.path.dirname(ePath))
        except IOError, e:
            print "CSS not available"

        QApplication.restoreOverrideCursor()

        return msg, status


    def exportLayerToPdf(self, layer, doPrint=False):
        '''
        Exports the layer to PDF
        First export to HTML then convert to PDF.
        If not output file given, send directly to the printer
        '''

        # Create temporary file path
        temp = tempfile.NamedTemporaryFile()
        try:
            # Create temporary HTML file
            tPath = "%s.html" % temp.name
            msg, status = self.exportLayerToHtml(layer, tPath, True)

            # Create a web view and fill it with the html file content
            web = QWebView()
            web.load(QUrl(tPath))

            # Set page options
            printer = QPrinter()
            printer.setPageSize(self.pageSize)
            printer.setOrientation(self.orientation)
            printer.setFontEmbeddingEnabled(True)
            printer.setColorMode(QPrinter.Color)
            printer.setCreator(u"QGIS - Plugin QuickExport")
            printer.setDocName(u"Export - %s" % layer.title() and layer.title() or layer.name())

            # Only set output file name in case of PDF export
            if not doPrint:
                printer.setOutputFileName(self.exportedFile)

            # Print only when HTML content is loaded
            def printIt():
                #~ web.show()
                web.print_(printer)
                os.remove(tPath)
                os.remove(os.path.join(os.path.dirname(tPath), 'table.css'))
            web.loadFinished[bool].connect(printIt)

        except:
            msg = QApplication.translate("quickExport", "An error occured during layer export.")
            status = QgsMessageBar.CRITICAL
        finally:
            # Automatically cleans up the file
            temp.close()
            msg = QApplication.translate("quickExport", "The layer has been successfully exported.")
            status = QgsMessageBar.INFO


        return msg, status


    def openFile(self):
        '''
        Opens a file with default system app
        '''
        if sys.platform == "win32":
            os.startfile(self.exportedFile)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, self.exportedFile])


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.mainWindow().removeToolBar(self.toolbar)

