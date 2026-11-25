# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProfilerAssistant_handin.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(804, 814)
        Widget.setMinimumSize(QSize(804, 814))
        Widget.setMaximumSize(QSize(804, 814))
        self.rootLayout = QVBoxLayout(Widget)
        self.rootLayout.setSpacing(8)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(12, 12, 12, 12)
        self.chartSection = QVBoxLayout()
        self.chartSection.setSpacing(4)
        self.chartSection.setObjectName(u"chartSection")
        self.chartView = QWidget(Widget)
        self.chartView.setObjectName(u"chartView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.chartView.sizePolicy().hasHeightForWidth())
        self.chartView.setSizePolicy(sizePolicy)
        self.chartView.setMinimumSize(QSize(0, 200))

        self.chartSection.addWidget(self.chartView)

        self.lbl_cause = QLabel(Widget)
        self.lbl_cause.setObjectName(u"lbl_cause")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_cause.sizePolicy().hasHeightForWidth())
        self.lbl_cause.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(10)
        self.lbl_cause.setFont(font)

        self.chartSection.addWidget(self.lbl_cause)


        self.rootLayout.addLayout(self.chartSection)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_top1 = QPushButton(Widget)
        self.btn_top1.setObjectName(u"btn_top1")
        sizePolicy1.setHeightForWidth(self.btn_top1.sizePolicy().hasHeightForWidth())
        self.btn_top1.setSizePolicy(sizePolicy1)
        self.btn_top1.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.btn_top1)

        self.btn_top2 = QPushButton(Widget)
        self.btn_top2.setObjectName(u"btn_top2")
        sizePolicy1.setHeightForWidth(self.btn_top2.sizePolicy().hasHeightForWidth())
        self.btn_top2.setSizePolicy(sizePolicy1)
        self.btn_top2.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.btn_top2)

        self.btn_top3 = QPushButton(Widget)
        self.btn_top3.setObjectName(u"btn_top3")
        sizePolicy1.setHeightForWidth(self.btn_top3.sizePolicy().hasHeightForWidth())
        self.btn_top3.setSizePolicy(sizePolicy1)
        self.btn_top3.setMinimumSize(QSize(0, 40))

        self.horizontalLayout.addWidget(self.btn_top3)


        self.rootLayout.addLayout(self.horizontalLayout)

        self.line_1 = QFrame(Widget)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.HLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.rootLayout.addWidget(self.line_1)

        self.lbl_profileSection = QLabel(Widget)
        self.lbl_profileSection.setObjectName(u"lbl_profileSection")
        font1 = QFont()
        font1.setBold(True)
        self.lbl_profileSection.setFont(font1)

        self.rootLayout.addWidget(self.lbl_profileSection)

        self.startFrameLayout = QHBoxLayout()
        self.startFrameLayout.setSpacing(8)
        self.startFrameLayout.setObjectName(u"startFrameLayout")
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 0))
        self.label_2.setMaximumSize(QSize(110, 16777215))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.startFrameLayout.addWidget(self.label_2)

        self.txt_startFrame = QLineEdit(Widget)
        self.txt_startFrame.setObjectName(u"txt_startFrame")
        self.txt_startFrame.setMaximumSize(QSize(113, 16777215))

        self.startFrameLayout.addWidget(self.txt_startFrame)

        self.spacer_start = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.startFrameLayout.addItem(self.spacer_start)


        self.rootLayout.addLayout(self.startFrameLayout)

        self.endFrameLayout = QHBoxLayout()
        self.endFrameLayout.setSpacing(8)
        self.endFrameLayout.setObjectName(u"endFrameLayout")
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(110, 0))
        self.label_3.setMaximumSize(QSize(110, 16777215))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.endFrameLayout.addWidget(self.label_3)

        self.txt_endFrame = QLineEdit(Widget)
        self.txt_endFrame.setObjectName(u"txt_endFrame")
        self.txt_endFrame.setMaximumSize(QSize(113, 16777215))

        self.endFrameLayout.addWidget(self.txt_endFrame)

        self.spacer_end = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.endFrameLayout.addItem(self.spacer_end)


        self.rootLayout.addLayout(self.endFrameLayout)

        self.folderLayout = QHBoxLayout()
        self.folderLayout.setSpacing(8)
        self.folderLayout.setObjectName(u"folderLayout")
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))
        self.label.setMaximumSize(QSize(110, 16777215))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.folderLayout.addWidget(self.label)

        self.txt_folderPath = QPlainTextEdit(Widget)
        self.txt_folderPath.setObjectName(u"txt_folderPath")
        sizePolicy1.setHeightForWidth(self.txt_folderPath.sizePolicy().hasHeightForWidth())
        self.txt_folderPath.setSizePolicy(sizePolicy1)
        self.txt_folderPath.setMaximumSize(QSize(16777215, 31))
        self.txt_folderPath.setFrameShadow(QFrame.Sunken)
        self.txt_folderPath.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_folderPath.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_folderPath.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.folderLayout.addWidget(self.txt_folderPath)

        self.btn_folder = QPushButton(Widget)
        self.btn_folder.setObjectName(u"btn_folder")
        self.btn_folder.setMaximumSize(QSize(31, 16777215))
        self.btn_folder.setIconSize(QSize(40, 40))

        self.folderLayout.addWidget(self.btn_folder)


        self.rootLayout.addLayout(self.folderLayout)

        self.btn_profiling = QPushButton(Widget)
        self.btn_profiling.setObjectName(u"btn_profiling")
        sizePolicy1.setHeightForWidth(self.btn_profiling.sizePolicy().hasHeightForWidth())
        self.btn_profiling.setSizePolicy(sizePolicy1)
        self.btn_profiling.setMinimumSize(QSize(0, 28))

        self.rootLayout.addWidget(self.btn_profiling)

        self.line_2 = QFrame(Widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.rootLayout.addWidget(self.line_2)

        self.lbl_evaluateSection = QLabel(Widget)
        self.lbl_evaluateSection.setObjectName(u"lbl_evaluateSection")
        self.lbl_evaluateSection.setFont(font1)

        self.rootLayout.addWidget(self.lbl_evaluateSection)

        self.filePathLayout = QVBoxLayout()
        self.filePathLayout.setSpacing(4)
        self.filePathLayout.setObjectName(u"filePathLayout")
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")

        self.filePathLayout.addWidget(self.label_5)

        self.list_selectedFiles = QListWidget(Widget)
        self.list_selectedFiles.setObjectName(u"list_selectedFiles")
        sizePolicy1.setHeightForWidth(self.list_selectedFiles.sizePolicy().hasHeightForWidth())
        self.list_selectedFiles.setSizePolicy(sizePolicy1)
        self.list_selectedFiles.setMinimumSize(QSize(0, 60))
        self.list_selectedFiles.setMaximumSize(QSize(16777215, 60))

        self.filePathLayout.addWidget(self.list_selectedFiles)

        self.btnAlignRight = QHBoxLayout()
        self.btnAlignRight.setObjectName(u"btnAlignRight")
        self.spacer_btn = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.btnAlignRight.addItem(self.spacer_btn)

        self.btn_folder_2 = QPushButton(Widget)
        self.btn_folder_2.setObjectName(u"btn_folder_2")
        self.btn_folder_2.setMinimumSize(QSize(36, 36))
        self.btn_folder_2.setMaximumSize(QSize(36, 36))

        self.btnAlignRight.addWidget(self.btn_folder_2)


        self.filePathLayout.addLayout(self.btnAlignRight)


        self.rootLayout.addLayout(self.filePathLayout)

        self.bar_evaluationProgress = QProgressBar(Widget)
        self.bar_evaluationProgress.setObjectName(u"bar_evaluationProgress")
        self.bar_evaluationProgress.setValue(24)

        self.rootLayout.addWidget(self.bar_evaluationProgress)

        self.btn_evaluate = QPushButton(Widget)
        self.btn_evaluate.setObjectName(u"btn_evaluate")
        sizePolicy1.setHeightForWidth(self.btn_evaluate.sizePolicy().hasHeightForWidth())
        self.btn_evaluate.setSizePolicy(sizePolicy1)
        self.btn_evaluate.setMinimumSize(QSize(0, 28))

        self.rootLayout.addWidget(self.btn_evaluate)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.lbl_cause.setText(QCoreApplication.translate("Widget", u"[No data]", None))
        self.btn_top1.setText(QCoreApplication.translate("Widget", u"TOP 1", None))
        self.btn_top2.setText(QCoreApplication.translate("Widget", u"TOP 2", None))
        self.btn_top3.setText(QCoreApplication.translate("Widget", u"TOP 3", None))
        self.lbl_profileSection.setText(QCoreApplication.translate("Widget", u"Profile Scene", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Start frame:", None))
        self.txt_startFrame.setPlaceholderText(QCoreApplication.translate("Widget", u"1.000", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"End frame:", None))
        self.txt_endFrame.setPlaceholderText(QCoreApplication.translate("Widget", u"10.000", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Output folder:", None))
        self.txt_folderPath.setPlaceholderText(QCoreApplication.translate("Widget", u"Select a foder to save the profiling results to", None))
        self.btn_folder.setText("")
        self.btn_profiling.setText(QCoreApplication.translate("Widget", u"Profile Scene", None))
        self.lbl_evaluateSection.setText(QCoreApplication.translate("Widget", u"Evaluate Scene", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Files to evaluate:", None))
        self.btn_folder_2.setText("")
        self.btn_evaluate.setText(QCoreApplication.translate("Widget", u"Evaluate Scene", None))
    # retranslateUi

