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
# Initialize Qt resources from file resources.py
import resource_rc
import os
from functools import partial
import shutil
import datetime
import locale
import tempfile
import sys
import subprocess
import csv

class QuickExport:


    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # Qgis version
        self.QgisVersion = QGis.QGIS_VERSION_INT

        # initialize locale
        if self.QgisVersion > 10900:
            locale = QSettings().value("locale/userLocale")[0:2]
        else:
            locale = QSettings().value("locale/userLocale").toString()[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'quickexport_%s.qm' % locale)

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.exportedFile = None
        self.etype = 'csv'

        # PDF print options
        self.maxLinesPerPage = 20
        self.maxAttributesBeforeSmallFontSize = 15
        self.orientation = QPrinter.Landscape
        self.pageSize = QPrinter.A4

        # CSS template file
        self.cssPath = os.path.join(
            self.plugin_dir,
            "templates/table.css"
        )


        # Get options from settings
        self.exportHiddenAttributes = False
        self.csvDelimiter = '\t'
        self.getSettings()

        # Csv hard-coded options
        self.csvQuotechar = '"'
        self.csvQuoting = csv.QUOTE_MINIMAL

        # Check if QgsMessageBar is available
        try:
            from qgis.gui import QgsMessageBar
            self.hasMessageBar = True
            self.mbStatusRel = {
                'info': QgsMessageBar.INFO,
                'critical': QgsMessageBar.CRITICAL,
                'warning': QgsMessageBar.WARNING
            }
        except:
            self.hasMessageBar = False
            # print "no message bar available - use QMessageBox"


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

        # Printer
        self.openOptionDialog = QAction(
            QIcon(os.path.dirname(__file__) +"/icons/option-dialog.png"),
            QApplication.translate("quickExport", u"Open option dialog"),
            self.iface.mainWindow()
        )
        self.toolbar.addAction(self.openOptionDialog)
        self.toolbar.setObjectName("quickexportOptionDialog");
        self.openOptionDialog.triggered.connect(self.open_option_dialog)


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


    def getSettings(self):
        '''
        Get options values from QSettings
        and set corresponding class properties
        '''
        # Options from QSettings
        s = QSettings()
        exportHiddenAttributes = s.value("quickexport/exportHiddenAttributes", False, type=bool)
        self.exportHiddenAttributes = exportHiddenAttributes

        # CSV options
        csvDelimiter = s.value("quickexport/csvDelimiter", 0, type=int)
        self.csvDelimiterMap = {
            0: '\t',
            1: ',',
            2: '|',
            3: ';'
        }
        self.csvDelimiter = self.csvDelimiterMap[csvDelimiter]



    def chooseExportFilePath(self, etype='csv'):
        '''
        Method to allow the user to choose a file path
        to store the exported attribute table
        '''
        msg = ''
        status = 'info'
        abort = False

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
        if not ePath and self.hasMessageBar:
            msg = QApplication.translate("quickExport", "Export has been canceled")
            status = 'info'
            abort = True
            return msg, status, abort

        # Delete file if exists (question already asked above)
        if os.path.exists(unicode(ePath)):
            try:
                os.remove(unicode(ePath))
            except OSError, e:
                msg = QApplication.translate("quickExport", "The file cannot be deleted. ")
                if sys.platform == "win32":
                    # it seems the return error is not unicode in windows !
                    errorMsg = e.strerror.decode('mbcs')
                else:
                    errorMsg = e.strerror
                msg+= QApplication.translate("quickExport", "Error: {}").format(errorMsg)
                status = 'critical'
                abort = True
                return msg, status, abort

        # Save file path in QGIS settings
        s.setValue(
            "quickExport/%s" % etypeDic[etype]['lastFileSetting'],
            str(ePath)
        )
        self.exportedFile = ePath

        return msg, status, abort



    def exportLayer(self, etype='csv'):
        '''
        Export the attribute table of the selected
        vector layer to the chose file type
        '''
        # set the type property
        self.etype = etype

        # Set settings from QSettings
        self.getSettings()

        # Get the active layer
        layer = self.iface.activeLayer()
        msg= None

        # Check if the layer is suitable for data export
        if layer and layer.type() == QgsMapLayer.VectorLayer and hasattr(layer, 'providerType'):

            # Ask the user to choose the path
            if etype != 'printer':
                msg, status, abort = self.chooseExportFilePath(etype)
                if not abort:
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
            status = 'warning'

        # Display status in the message bar
        if msg:
            self.displayMessage( msg, status )


    def displayMessage(self, msg, status):
        '''
        Display a message to the user.
        Uses the new message bar if available
        or QgsMessageBox instead
        '''
        etype = self.etype

        # Since QGIS 2.0, a message bar is available
        if self.hasMessageBar:
            widget = self.iface.messageBar().createMessage(msg)
            # Add a button to open the file
            if self.exportedFile and status == 'info' and etype != 'printer':
                btOpen = QPushButton(widget)
                btOpen.setText(QApplication.translate("quickExport", "Open file"))
                btOpen.pressed.connect(self.openFile)
                widget.layout().addWidget(btOpen)
            # Display message bar
            self.iface.messageBar().pushWidget(
                widget,
                self.mbStatusRel[status],
                6
            )
        # Use old QgsMessageBox instead
        else:
            if self.exportedFile and status == 'info' and etype != 'printer':
                openIt = QMessageBox.question(
                    self.toolbar,
                    u'Quick Export',
                    msg + '\n\n' + QApplication.translate("quickExport", "Open file"),
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if openIt == QMessageBox.Yes:
                    self.openFile()
            else:
                QMessageBox.information(
                    self.toolbar,
                    u"Quick Export",
                    msg,
                    QMessageBox.Ok
            )



    def displayAttributeValue(self, value):
        '''
        Convert QGIS attribute data into readable values
        '''
        # QGIS version
        isQgis2 = self.QgisVersion > 10900

        # Get locale date representation
        locale.setlocale(locale.LC_TIME,'')
        if hasattr(locale, 'nl_langinfo'):
            date_format = locale.nl_langinfo(locale.D_FMT)
            datetime_format = locale.nl_langinfo(locale.D_T_FMT)
        else:
            date_format = "%x"
            datetime_format = "%x %X"

        # Convert value depending of type
        if hasattr(value, 'toPyDate'):
            output = value.toPyDate().strftime(date_format)
        elif hasattr(value, 'toPyDateTime'):
            output = value.toPyDateTime().strftime(datetime_format)
        else:
            output = u"%s" % value if isQgis2 else u"%s" % value.toString()

        return output


    def getLayerData(self, layer):
        '''
        Get fields and data from
        a vector layer
        '''
        data = []

        # Get layer fields names
        fields = layer.pendingFields()
        if self.QgisVersion > 10900:
            fieldNames = [
                field.name() for i, field in enumerate(fields)
                if layer.editType(i) != QgsVectorLayer.Hidden
                or self.exportHiddenAttributes
            ]
        else:
            fieldNames = [
                str(fields[i].name()) for i in fields
                if layer.editType(i) != QgsVectorLayer.Hidden
                or self.exportHiddenAttributes
            ]
        data.append(fieldNames)

        # Get selected features or all features
        if layer.selectedFeatureCount():
            nb = layer.selectedFeatureCount()
        else:
            nb = layer.featureCount()



        # Get layer fields data

        # QGIS >= 2.0
        if self.QgisVersion > 10900:
            if layer.selectedFeatureCount():
                features = layer.selectedFeatures()
            else:
                features = layer.getFeatures()
            for feat in features:
                # Get attribute data
                values = [
                    self.displayAttributeValue(a) for i, a in enumerate(feat.attributes())
                    if layer.editType(i) != QgsVectorLayer.Hidden
                    or self.exportHiddenAttributes
                ]
                data.append(values)

        # QGIS 1.8
        else:
            provider = layer.dataProvider()
            allAttrs = provider.attributeIndexes()
            provider.select(allAttrs, QgsRectangle(), False)
            layer.select(allAttrs, QgsRectangle(), False)
            if layer.selectedFeatureCount():
                items = layer.selectedFeatures()
            else:
                items = layer
            for feat in items:
                attrs = feat.attributeMap()
                values = [
                    self.displayAttributeValue(v) for k,v in attrs.iteritems()
                    if layer.editType(k) != QgsVectorLayer.Hidden
                    or self.exportHiddenAttributes
                ]
                data.append(values)

        return data, nb


    def exportLayerToCsv(self, layer):
        '''
        Exports the layer to CSV

        '''
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Get layer data
        data, nb = self.getLayerData(layer)

        # Export data to CSV
        try:
            with open(self.exportedFile, 'wb') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=self.csvDelimiter, quotechar=self.csvQuotechar, quoting=self.csvQuoting
                )
                writer.writerows(data)
            msg = QApplication.translate("quickExport", "The layer has been successfully exported.")
            status = 'info'
        except OSError, e:
            msg = QApplication.translate("quickExport", "An error occured during layer export." + str(e.error))
            status = 'critical'
        finally:
            QApplication.restoreOverrideCursor()

        return msg, status


    def exportLayerToHtml(self, layer, ePath=None, cutPages=False):
        '''
        Exports the layer to HTML
        using a template and reading the data
        from the selected layer
        '''
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Read template file
        tplPath = os.path.join(
            self.plugin_dir,
            "templates/htmlTemplate.tpl"
        )
        fin = open(tplPath)
        data = fin.read().decode('utf-8')
        fin.close()

        # Get layer data
        layerData, nb = self.getLayerData(layer)

        # Layer fields names
        fieldNames = layerData[0]
        nbAttr = len(fieldNames)

        # Create thead with attribute names
        thead = '                <tr>\n'
        for field in fieldNames:
            thead+= '                    <th>%s</th>\n' % field
        thead+= '                </tr>\n\n'

        # Create tbody content with feature attribute data
        tbody = ''
        i = 0
        page = 1
        attrValues = layerData[1:]

        # Write table content in HTML syntax
        for values in attrValues:
            tbody+= '                <tr>\n'
            tbody+= '                    <td>'
            tbody+= '</td>\n                    <td>'.join(values)
            tbody+= '                    </td>\n'
            tbody+= '                </tr>\n\n'
            i+=1
            if i == self.maxLinesPerPage and cutPages and self.QgisVersion > 10900:
                i = 0
                tbody+= '</table>\n\n'
                tbody+= '<span>Page %s</span>' % page
                tbody+= '<div style="page-break-after:always;border: 0px solid white;"></div>\n\n'
                tbody+= '<table><thead>' + thead + '</thead><tbody>'
                page+=1

        # Get creation date
        locale.setlocale(locale.LC_TIME,'')
        if hasattr(locale, 'nl_langinfo'):
            date_format = locale.nl_langinfo(locale.D_T_FMT)
        else:
            date_format = "%x %X"
        today = datetime.datetime.today()
        date = today.strftime(date_format)
        dt_date = unicode(QApplication.translate("quickExport", "Generated by QGIS QuickExport plugin"))

        # Title, abstract, and line count
        dt_title = unicode(QApplication.translate("quickExport", "Layer"))
        title = layer.title() and layer.title() or layer.name()
        dt_abstract = unicode(QApplication.translate("quickExport", "Abstract"))
        abstract = layer.abstract() and str(layer.abstract()) or '-'
        dt_info = unicode(QApplication.translate("quickExport", "Information"))
        info = unicode(QApplication.translate("quickExport", "{} lines exported")).format(str(nb))

        # Adapt style if needed
        style = ''
        # Get CSS style from table.css
        with open(self.cssPath, 'r') as content_file:
            style = content_file.read()
        if nbAttr > self.maxAttributesBeforeSmallFontSize:
            style+= 'th, td {font-size:small;}'
            self.maxLinesPerPage = 30

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
            status = 'critical'
        finally:
            msg = QApplication.translate("quickExport", "The layer has been successfully exported.")
            status = 'info'

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

            # Print only when HTML content is loaded
            def printIt():
                #~ web.show()
                # Open the printer dialog if needed
                if doPrint:
                    dialog = QPrintDialog()
                    if dialog.exec_() == QDialog.Accepted:
                        printer = dialog.printer()
                    else:
                        return
                # No print, only PDF export
                else:
                    # Set page options for PDF
                    printer = QPrinter()
                    printer.setPageSize(self.pageSize)
                    printer.setOrientation(self.orientation)
                    printer.setFontEmbeddingEnabled(True)
                    printer.setColorMode(QPrinter.Color)
                    # set output file name in case of PDF export
                    printer.setOutputFileName(self.exportedFile)

                # Set some metadata
                printer.setCreator(u"QGIS - Plugin QuickExport")
                printer.setDocName(u"Export - %s" % layer.title() and layer.title() or layer.name())

                # Print
                web.print_(printer)

                # Try to remove temporary html file created before
                try:
                    os.remove(tPath)
                except OSError, e:
                    print "Error while deleted temporary files: %s)" % tPath

            # Only print when the HTML content has been loaded in the QWebView
            web.loadFinished[bool].connect(printIt)

        except:
            msg = QApplication.translate("quickExport", "An error occured during layer export.")
            status = 'critical'
        finally:
            # Automatically cleans up the file
            temp.close()
            msg = QApplication.translate("quickExport", "The layer has been successfully exported.")
            status = 'info'


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


    def open_option_dialog(self):
        '''
        Config dialog
        '''
        dialog = quickexport_option_dialog(self.iface)
        dialog.exec_()


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.mainWindow().removeToolBar(self.toolbar)



# --------------------------------------------------------
#        Option - Let the user configure options
# --------------------------------------------------------

from quickexport_option_form import *

class quickexport_option_dialog(QDialog, Ui_quickexport_option_form):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)

        # Signals/Slot Connections
        self.rejected.connect(self.onReject)
        self.buttonBox.rejected.connect(self.onReject)
        self.buttonBox.accepted.connect(self.onAccept)

        # Set initial widget values
        self.getValuesFromSettings()

        self.csvDelimiterMap = {
            0: '\t',
            1: ',',
            2: '|',
            3: ';'
        }


    def getValuesFromSettings(self):
        '''
        Get values from QGIS Settings
        and apply them to dialog items
        '''
        s = QSettings()

        # Export hidden attributes
        exportHiddenAttributes = s.value("quickexport/exportHiddenAttributes", False, type=bool)
        if exportHiddenAttributes:
            self.cbExportHiddenAttributes.setChecked(exportHiddenAttributes)

        # CSV delimiter
        csvDelimiter = s.value("quickexport/csvDelimiter", 0, type=int)
        if csvDelimiter:
            delimiterRadioButtons =  self.gbDelimiter.findChildren(QRadioButton)
            for i, radio in enumerate(delimiterRadioButtons):
                radio.setChecked(csvDelimiter == i)



    def onAccept(self):
        '''
        Save options into QSettings when pressing OK button
        '''

        s = QSettings()

        # Export hidden attributes
        s.setValue("quickexport/exportHiddenAttributes", self.cbExportHiddenAttributes.isChecked())

        # CSV delimiter
        delimiterRadioButtons =  self.gbDelimiter.findChildren(QRadioButton)
        csvDelimiter = s.value("quickexport/csvDelimiter", 0, type=int)
        for i, radio in enumerate(delimiterRadioButtons):
            if radio.isChecked():
                csvDelimiter = i
        s.setValue("quickexport/csvDelimiter", csvDelimiter)

        self.accept()

    def onReject(self):
        '''
        Run some actions when
        the user closes the dialog
        '''
        string = "quickexport option dialog closed"
        self.close()
