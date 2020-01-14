# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quickexport_option_form.ui'
#
# Created: Fri Apr  4 15:06:30 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from __future__ import absolute_import
from builtins import object
from qgis.PyQt import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_quickexport_option_form(object):
    def setupUi(self, quickexport_option_form):
        quickexport_option_form.setObjectName(_fromUtf8("quickexport_option_form"))
        quickexport_option_form.resize(570, 242)
        self.verticalLayout = QtWidgets.QVBoxLayout(quickexport_option_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtWidgets.QScrollArea(quickexport_option_form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 550, 222))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.cbExportHiddenAttributes = QtWidgets.QCheckBox(self.groupBox_3)
        self.cbExportHiddenAttributes.setText(_fromUtf8(""))
        self.cbExportHiddenAttributes.setObjectName(_fromUtf8("cbExportHiddenAttributes"))
        self.gridLayout_2.addWidget(self.cbExportHiddenAttributes, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gbDelimiter = QtWidgets.QGroupBox(self.groupBox)
        self.gbDelimiter.setTitle(_fromUtf8(""))
        self.gbDelimiter.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gbDelimiter.setFlat(False)
        self.gbDelimiter.setCheckable(False)
        self.gbDelimiter.setObjectName(_fromUtf8("gbDelimiter"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gbDelimiter)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.gbDelimiter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rbDelimiterTab = QtWidgets.QRadioButton(self.gbDelimiter)
        self.rbDelimiterTab.setChecked(True)
        self.rbDelimiterTab.setObjectName(_fromUtf8("rbDelimiterTab"))
        self.horizontalLayout.addWidget(self.rbDelimiterTab)
        self.rbDelimiterComma = QtWidgets.QRadioButton(self.gbDelimiter)
        self.rbDelimiterComma.setObjectName(_fromUtf8("rbDelimiterComma"))
        self.horizontalLayout.addWidget(self.rbDelimiterComma)
        self.rbDelimiterPipe = QtWidgets.QRadioButton(self.gbDelimiter)
        self.rbDelimiterPipe.setObjectName(_fromUtf8("rbDelimiterPipe"))
        self.horizontalLayout.addWidget(self.rbDelimiterPipe)
        self.rbDelimiterSemicolon = QtWidgets.QRadioButton(self.gbDelimiter)
        self.rbDelimiterSemicolon.setObjectName(_fromUtf8("rbDelimiterSemicolon"))
        self.horizontalLayout.addWidget(self.rbDelimiterSemicolon)
        self.verticalLayout_3.addWidget(self.gbDelimiter)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.scrollAreaWidgetContents)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(quickexport_option_form)
        QtCore.QMetaObject.connectSlotsByName(quickexport_option_form)
        quickexport_option_form.setTabOrder(self.scrollArea, self.buttonBox)

    def retranslateUi(self, quickexport_option_form):
        quickexport_option_form.setWindowTitle(_translate("quickexport_option_form", "QuickExport - Settings", None))
        self.groupBox_3.setTitle(_translate("quickexport_option_form", "General settings", None))
        self.label_7.setText(_translate("quickexport_option_form", "Export hidden attributes", None))
        self.groupBox.setTitle(_translate("quickexport_option_form", "CSV export", None))
        self.label.setText(_translate("quickexport_option_form", "Delimiter", None))
        self.rbDelimiterTab.setText(_translate("quickexport_option_form", "tab", None))
        self.rbDelimiterComma.setText(_translate("quickexport_option_form", "comma", None))
        self.rbDelimiterPipe.setText(_translate("quickexport_option_form", "pipe", None))
        self.rbDelimiterSemicolon.setText(_translate("quickexport_option_form", "semicolon", None))

from . import resource_rc
