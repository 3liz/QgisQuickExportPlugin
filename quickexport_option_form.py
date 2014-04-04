# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quickexport_option_form.ui'
#
# Created: Fri Apr  4 11:48:05 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_quickexport_option_form(object):
    def setupUi(self, quickexport_option_form):
        quickexport_option_form.setObjectName(_fromUtf8("quickexport_option_form"))
        quickexport_option_form.resize(519, 245)
        self.verticalLayout = QtGui.QVBoxLayout(quickexport_option_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(quickexport_option_form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 499, 225))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.cbExportHiddenAttributes = QtGui.QCheckBox(self.groupBox_3)
        self.cbExportHiddenAttributes.setText(_fromUtf8(""))
        self.cbExportHiddenAttributes.setObjectName(_fromUtf8("cbExportHiddenAttributes"))
        self.gridLayout_2.addWidget(self.cbExportHiddenAttributes, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gbDelimiter = QtGui.QGroupBox(self.groupBox)
        self.gbDelimiter.setTitle(_fromUtf8(""))
        self.gbDelimiter.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gbDelimiter.setFlat(False)
        self.gbDelimiter.setCheckable(False)
        self.gbDelimiter.setObjectName(_fromUtf8("gbDelimiter"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbDelimiter)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.gbDelimiter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rbDelimiterComma = QtGui.QRadioButton(self.gbDelimiter)
        self.rbDelimiterComma.setObjectName(_fromUtf8("rbDelimiterComma"))
        self.horizontalLayout.addWidget(self.rbDelimiterComma)
        self.rbDelimiterTab = QtGui.QRadioButton(self.gbDelimiter)
        self.rbDelimiterTab.setObjectName(_fromUtf8("rbDelimiterTab"))
        self.horizontalLayout.addWidget(self.rbDelimiterTab)
        self.rbDelimiterPipe = QtGui.QRadioButton(self.gbDelimiter)
        self.rbDelimiterPipe.setObjectName(_fromUtf8("rbDelimiterPipe"))
        self.horizontalLayout.addWidget(self.rbDelimiterPipe)
        self.rbDelimiterSemicolon = QtGui.QRadioButton(self.gbDelimiter)
        self.rbDelimiterSemicolon.setObjectName(_fromUtf8("rbDelimiterSemicolon"))
        self.horizontalLayout.addWidget(self.rbDelimiterSemicolon)
        self.verticalLayout_3.addWidget(self.gbDelimiter)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(self.scrollAreaWidgetContents)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
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
        self.rbDelimiterComma.setText(_translate("quickexport_option_form", "comma", None))
        self.rbDelimiterTab.setText(_translate("quickexport_option_form", "tab", None))
        self.rbDelimiterPipe.setText(_translate("quickexport_option_form", "pipe", None))
        self.rbDelimiterSemicolon.setText(_translate("quickexport_option_form", "semicolon", None))

import resource_rc
