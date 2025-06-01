# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QSlider, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 760)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: rgb(40, 44, 52);\n"
""
                        "	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
""
                        "/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(40, 44, 52)"
                        ";\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; "
                        "}\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
""
                        "/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	paddi"
                        "ng: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
""
                        "QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
""
                        "    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" Q"
                        "ScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons"
                        "/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width:"
                        " 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
""
                        "    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: rgb(255, 121, "
                        "198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.bgApp.setFont(font)
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFont(font)
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFont(font)
        self.topLogoInfo.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula.png);")
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFont(font)
        self.topLogo.setAutoFillBackground(False)
        self.topLogo.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula.png);")
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftDescription.setFont(font1)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuFrame.sizePolicy().hasHeightForWidth())
        self.leftMenuFrame.setSizePolicy(sizePolicy)
        self.leftMenuFrame.setFont(font)
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFont(font)
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        self.toggleButton.setGeometry(QRect(0, 0, 60, 45))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy1)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFont(font)
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.topMenu)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy1.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy1)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout.addWidget(self.btn_home)

        self.btn_bwd = QPushButton(self.topMenu)
        self.btn_bwd.setObjectName(u"btn_bwd")
        sizePolicy1.setHeightForWidth(self.btn_bwd.sizePolicy().hasHeightForWidth())
        self.btn_bwd.setSizePolicy(sizePolicy1)
        self.btn_bwd.setMinimumSize(QSize(0, 45))
        self.btn_bwd.setFont(font)
        self.btn_bwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_bwd.setLayoutDirection(Qt.LeftToRight)
        self.btn_bwd.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-notes.png);")

        self.verticalLayout.addWidget(self.btn_bwd)

        self.btn_box_spread = QPushButton(self.topMenu)
        self.btn_box_spread.setObjectName(u"btn_box_spread")
        sizePolicy1.setHeightForWidth(self.btn_box_spread.sizePolicy().hasHeightForWidth())
        self.btn_box_spread.setSizePolicy(sizePolicy1)
        self.btn_box_spread.setMinimumSize(QSize(0, 45))
        self.btn_box_spread.setFont(font)
        self.btn_box_spread.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_box_spread.setLayoutDirection(Qt.LeftToRight)
        self.btn_box_spread.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-box.png);")

        self.verticalLayout.addWidget(self.btn_box_spread)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFont(font)
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFont(font)
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFont(font)
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy2)
        self.leftBox.setFont(font)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_header = QLabel(self.leftBox)
        self.label_header.setObjectName(u"label_header")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_header.sizePolicy().hasHeightForWidth())
        self.label_header.setSizePolicy(sizePolicy3)
        self.label_header.setMaximumSize(QSize(160, 45))
        self.label_header.setFont(font)
        self.label_header.setTextFormat(Qt.AutoText)
        self.label_header.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_header)

        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy3.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy3)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setTextFormat(Qt.AutoText)
        self.titleRightInfo.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFont(font)
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setFont(font)
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/cil-window-minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setFont(font)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-window-maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon1)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setFont(font)
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/cil-x.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeAppBtn.setIcon(icon2)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        sizePolicy.setHeightForWidth(self.contentBottom.sizePolicy().hasHeightForWidth())
        self.contentBottom.setSizePolicy(sizePolicy)
        self.contentBottom.setFont(font)
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        sizePolicy.setHeightForWidth(self.content.sizePolicy().hasHeightForWidth())
        self.content.setSizePolicy(sizePolicy)
        self.content.setFont(font)
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setFont(font)
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/images/ibkr_tools_logo.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.stackedWidget.addWidget(self.home)
        self.beta_weighted_deltas = QWidget()
        self.beta_weighted_deltas.setObjectName(u"beta_weighted_deltas")
        sizePolicy.setHeightForWidth(self.beta_weighted_deltas.sizePolicy().hasHeightForWidth())
        self.beta_weighted_deltas.setSizePolicy(sizePolicy)
        self.bwd_frame = QFrame(self.beta_weighted_deltas)
        self.bwd_frame.setObjectName(u"bwd_frame")
        self.bwd_frame.setGeometry(QRect(0, 0, 1401, 641))
        sizePolicy.setHeightForWidth(self.bwd_frame.sizePolicy().hasHeightForWidth())
        self.bwd_frame.setSizePolicy(sizePolicy)
        self.bwd_frame.setFont(font)
        self.bwd_frame.setFrameShape(QFrame.StyledPanel)
        self.bwd_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.bwd_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.bwd_listWidget = QListWidget(self.bwd_frame)
        self.bwd_listWidget.setObjectName(u"bwd_listWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.bwd_listWidget.sizePolicy().hasHeightForWidth())
        self.bwd_listWidget.setSizePolicy(sizePolicy4)
        self.bwd_listWidget.setMinimumSize(QSize(100, 500))
        self.bwd_listWidget.setMaximumSize(QSize(200, 16777215))
        self.bwd_listWidget.setBaseSize(QSize(200, 1245))
        font2 = QFont()
        font2.setFamilies([u"Titillium Web"])
        font2.setPointSize(14)
        font2.setBold(False)
        font2.setItalic(False)
        self.bwd_listWidget.setFont(font2)
        self.bwd_listWidget.setStyleSheet(u"QListWidget::item {\n"
"    padding: 3px;\n"
"}")
        self.bwd_listWidget.setFrameShape(QFrame.NoFrame)
        self.bwd_listWidget.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.bwd_listWidget)

        self.bwd_tableWidget = QTableWidget(self.bwd_frame)
        if (self.bwd_tableWidget.columnCount() < 9):
            self.bwd_tableWidget.setColumnCount(9)
        font3 = QFont()
        font3.setFamilies([u"Titillium Web"])
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font3);
        self.bwd_tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        if (self.bwd_tableWidget.rowCount() < 50):
            self.bwd_tableWidget.setRowCount(50)
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font4);
        self.bwd_tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(16, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(17, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(18, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(19, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(20, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(21, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(22, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(23, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(24, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(25, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(26, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(27, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(28, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(29, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(30, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(31, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(32, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(33, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(34, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(35, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(36, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(37, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(38, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(39, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(40, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(41, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(42, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(43, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(44, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(45, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(46, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(47, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(48, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.bwd_tableWidget.setVerticalHeaderItem(49, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.bwd_tableWidget.setItem(0, 0, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.bwd_tableWidget.setItem(0, 1, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.bwd_tableWidget.setItem(0, 2, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.bwd_tableWidget.setItem(0, 3, __qtablewidgetitem62)
        self.bwd_tableWidget.setObjectName(u"bwd_tableWidget")
        sizePolicy.setHeightForWidth(self.bwd_tableWidget.sizePolicy().hasHeightForWidth())
        self.bwd_tableWidget.setSizePolicy(sizePolicy)
        self.bwd_tableWidget.setMinimumSize(QSize(1000, 0))
        self.bwd_tableWidget.setMaximumSize(QSize(16777215, 16777215))
        palette = QPalette()
        brush = QBrush(QColor(221, 221, 221, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.BrushStyle.NoBrush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        brush3 = QBrush(QColor(221, 221, 221, 128))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush3)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.BrushStyle.NoBrush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush3)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 255))
        brush5.setStyle(Qt.BrushStyle.NoBrush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush3)
#endif
        self.bwd_tableWidget.setPalette(palette)
        self.bwd_tableWidget.setFont(font)
        self.bwd_tableWidget.setFrameShape(QFrame.NoFrame)
        self.bwd_tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.bwd_tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bwd_tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.bwd_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bwd_tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bwd_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bwd_tableWidget.setShowGrid(True)
        self.bwd_tableWidget.setGridStyle(Qt.SolidLine)
        self.bwd_tableWidget.setSortingEnabled(False)
        self.bwd_tableWidget.horizontalHeader().setVisible(True)
        self.bwd_tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.bwd_tableWidget.horizontalHeader().setDefaultSectionSize(90)
        self.bwd_tableWidget.horizontalHeader().setStretchLastSection(True)
        self.bwd_tableWidget.verticalHeader().setVisible(False)
        self.bwd_tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.bwd_tableWidget.verticalHeader().setHighlightSections(False)
        self.bwd_tableWidget.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout_6.addWidget(self.bwd_tableWidget)

        self.stackedWidget.addWidget(self.beta_weighted_deltas)
        self.box_spread = QWidget()
        self.box_spread.setObjectName(u"box_spread")
        self.box_spread.setLayoutDirection(Qt.LeftToRight)
        self.bxs_btn_type = QPushButton(self.box_spread)
        self.bxs_btn_type.setObjectName(u"bxs_btn_type")
        self.bxs_btn_type.setGeometry(QRect(610, 10, 120, 60))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.bxs_btn_type.sizePolicy().hasHeightForWidth())
        self.bxs_btn_type.setSizePolicy(sizePolicy5)
        self.bxs_btn_type.setMinimumSize(QSize(120, 60))
        self.bxs_btn_type.setMaximumSize(QSize(120, 60))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI Historic"])
        self.bxs_btn_type.setFont(font5)
        self.bxs_btn_type.setLayoutDirection(Qt.LeftToRight)
        self.bxs_comboBox_currency = QComboBox(self.box_spread)
        self.bxs_comboBox_currency.setObjectName(u"bxs_comboBox_currency")
        self.bxs_comboBox_currency.setGeometry(QRect(120, 120, 101, 41))
        self.bxs_comboBox_currency.setStyleSheet(u"color: rgb(255, 15, 51);\n"
"background-color: rgb(40, 44, 52);\n"
"")
        self.bxs_label_currency = QLabel(self.box_spread)
        self.bxs_label_currency.setObjectName(u"bxs_label_currency")
        self.bxs_label_currency.setGeometry(QRect(88, 85, 161, 20))
        self.bxs_label_currency.setAlignment(Qt.AlignCenter)
        self.bxs_label_index = QLabel(self.box_spread)
        self.bxs_label_index.setObjectName(u"bxs_label_index")
        self.bxs_label_index.setGeometry(QRect(320, 85, 111, 20))
        self.bxs_label_index.setAlignment(Qt.AlignCenter)
        self.bxs_comboBox_index = QComboBox(self.box_spread)
        self.bxs_comboBox_index.setObjectName(u"bxs_comboBox_index")
        self.bxs_comboBox_index.setGeometry(QRect(310, 120, 141, 41))
        self.bxs_comboBox_index.setAutoFillBackground(False)
        self.bxs_comboBox_index.setStyleSheet(u"color: rgb(255, 15, 51);\n"
"background-color: rgb(40, 44, 52);\n"
"")
        self.bxs_label_expiry = QLabel(self.box_spread)
        self.bxs_label_expiry.setObjectName(u"bxs_label_expiry")
        self.bxs_label_expiry.setGeometry(QRect(1100, 85, 121, 20))
        self.bxs_label_expiry.setAlignment(Qt.AlignCenter)
        self.bxs_comboBox_expiry = QComboBox(self.box_spread)
        self.bxs_comboBox_expiry.setObjectName(u"bxs_comboBox_expiry")
        self.bxs_comboBox_expiry.setGeometry(QRect(1060, 120, 211, 41))
        self.bxs_comboBox_expiry.setLayoutDirection(Qt.LeftToRight)
        self.bxs_comboBox_expiry.setStyleSheet(u"color: rgb(255, 15, 51);\n"
"background-color: rgb(40, 44, 52);\n"
"")
        self.bxs_horizontalSlider_rate = QSlider(self.box_spread)
        self.bxs_horizontalSlider_rate.setObjectName(u"bxs_horizontalSlider_rate")
        self.bxs_horizontalSlider_rate.setGeometry(QRect(60, 378, 1261, 20))
        self.bxs_horizontalSlider_rate.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.bxs_horizontalSlider_rate.setMouseTracking(True)
        self.bxs_horizontalSlider_rate.setTracking(True)
        self.bxs_horizontalSlider_rate.setOrientation(Qt.Horizontal)
        self.bxs_label_lower_rate = QLabel(self.box_spread)
        self.bxs_label_lower_rate.setObjectName(u"bxs_label_lower_rate")
        self.bxs_label_lower_rate.setGeometry(QRect(40, 400, 81, 20))
        self.bxs_label_higher_rate = QLabel(self.box_spread)
        self.bxs_label_higher_rate.setObjectName(u"bxs_label_higher_rate")
        self.bxs_label_higher_rate.setGeometry(QRect(1270, 410, 81, 20))
        self.bxs_label_benchmark_rate = QLabel(self.box_spread)
        self.bxs_label_benchmark_rate.setObjectName(u"bxs_label_benchmark_rate")
        self.bxs_label_benchmark_rate.setGeometry(QRect(630, 328, 121, 20))
        self.bxs_label_selected_rate = QLabel(self.box_spread)
        self.bxs_label_selected_rate.setObjectName(u"bxs_label_selected_rate")
        self.bxs_label_selected_rate.setGeometry(QRect(650, 428, 81, 20))
        self.bxs_label_upper_strike = QLabel(self.box_spread)
        self.bxs_label_upper_strike.setObjectName(u"bxs_label_upper_strike")
        self.bxs_label_upper_strike.setGeometry(QRect(40, 220, 150, 20))
        self.bxs_label_lower_strike = QLabel(self.box_spread)
        self.bxs_label_lower_strike.setObjectName(u"bxs_label_lower_strike")
        self.bxs_label_lower_strike.setGeometry(QRect(40, 270, 150, 20))
        self.bxs_label_spread = QLabel(self.box_spread)
        self.bxs_label_spread.setObjectName(u"bxs_label_spread")
        self.bxs_label_spread.setGeometry(QRect(375, 245, 151, 20))
        self.bxs_label_amount = QLabel(self.box_spread)
        self.bxs_label_amount.setObjectName(u"bxs_label_amount")
        self.bxs_label_amount.setGeometry(QRect(591, 200, 81, 20))
        self.bxs_label_redemption = QLabel(self.box_spread)
        self.bxs_label_redemption.setObjectName(u"bxs_label_redemption")
        self.bxs_label_redemption.setGeometry(QRect(1050, 270, 231, 20))
        self.bxs_lineEdit_amount = QLineEdit(self.box_spread)
        self.bxs_lineEdit_amount.setObjectName(u"bxs_lineEdit_amount")
        self.bxs_lineEdit_amount.setGeometry(QRect(680, 195, 71, 28))
        self.bxs_lineEdit_amount.setAlignment(Qt.AlignCenter)
        self.bxs_label_underlying_price = QLabel(self.box_spread)
        self.bxs_label_underlying_price.setObjectName(u"bxs_label_underlying_price")
        self.bxs_label_underlying_price.setGeometry(QRect(810, 220, 160, 20))
        self.bxs_label_type = QLabel(self.box_spread)
        self.bxs_label_type.setObjectName(u"bxs_label_type")
        self.bxs_label_type.setGeometry(QRect(830, 85, 121, 20))
        self.bxs_label_type.setAlignment(Qt.AlignCenter)
        self.bxs_comboBox_type = QComboBox(self.box_spread)
        self.bxs_comboBox_type.setObjectName(u"bxs_comboBox_type")
        self.bxs_comboBox_type.setGeometry(QRect(800, 120, 201, 41))
        self.bxs_comboBox_type.setStyleSheet(u"color: rgb(255, 15, 51);\n"
"background-color: rgb(40, 44, 52);\n"
"")
        self.bxs_comboBox_upper_strike = QComboBox(self.box_spread)
        self.bxs_comboBox_upper_strike.setObjectName(u"bxs_comboBox_upper_strike")
        self.bxs_comboBox_upper_strike.setGeometry(QRect(190, 210, 141, 41))
        self.bxs_comboBox_upper_strike.setStyleSheet(u"color: rgb(255, 15, 51);\n"
"background-color: rgb(40, 44, 52);\n"
"")
        self.bxs_comboBox_lower_strike = QComboBox(self.box_spread)
        self.bxs_comboBox_lower_strike.setObjectName(u"bxs_comboBox_lower_strike")
        self.bxs_comboBox_lower_strike.setGeometry(QRect(190, 260, 141, 41))
        self.bxs_comboBox_lower_strike.setStyleSheet(u"color: rgb(255, 15, 51);\n"
"background-color: rgb(40, 44, 52);\n"
"")
        self.bxs_label_multiplier = QLabel(self.box_spread)
        self.bxs_label_multiplier.setObjectName(u"bxs_label_multiplier")
        self.bxs_label_multiplier.setGeometry(QRect(810, 270, 160, 20))
        self.bxs_label_principal = QLabel(self.box_spread)
        self.bxs_label_principal.setObjectName(u"bxs_label_principal")
        self.bxs_label_principal.setGeometry(QRect(1050, 220, 231, 20))
        self.stackedWidget.addWidget(self.box_spread)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setEnabled(True)
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFont(font)
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFont(font)
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFont(font)
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFont(font)
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_message = QPushButton(self.topMenus)
        self.btn_message.setObjectName(u"btn_message")
        sizePolicy1.setHeightForWidth(self.btn_message.sizePolicy().hasHeightForWidth())
        self.btn_message.setSizePolicy(sizePolicy1)
        self.btn_message.setMinimumSize(QSize(0, 45))
        self.btn_message.setFont(font)
        self.btn_message.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_message.setLayoutDirection(Qt.LeftToRight)
        self.btn_message.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-envelope-open.png);")

        self.verticalLayout_14.addWidget(self.btn_message)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy1.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy1)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy1.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy1)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFont(font)
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font6 = QFont()
        font6.setFamilies([u"Segoe UI"])
        font6.setBold(False)
        font6.setItalic(False)
        self.creditsLabel.setFont(font6)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setFont(font6)
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFont(font)
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftDescription.setText("")
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_bwd.setText(QCoreApplication.translate("MainWindow", u"Beta Weighted Deltas", None))
        self.btn_box_spread.setText(QCoreApplication.translate("MainWindow", u"Box Spread", None))
        self.label_header.setText(QCoreApplication.translate("MainWindow", u"IBKR Tools", None))
        self.titleRightInfo.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        ___qtablewidgetitem = self.bwd_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Underlying", None));
        ___qtablewidgetitem1 = self.bwd_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u03b2 Beta / Position", None));
        ___qtablewidgetitem2 = self.bwd_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Qty", None));
        ___qtablewidgetitem3 = self.bwd_tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"iVol", None));
        ___qtablewidgetitem4 = self.bwd_tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u03b4 Delta", None));
        ___qtablewidgetitem5 = self.bwd_tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Beta weighted deltas", None));
        ___qtablewidgetitem6 = self.bwd_tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u03b8 Theta", None));
        ___qtablewidgetitem7 = self.bwd_tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u03b3 Gamma (L|S)", None));
        ___qtablewidgetitem8 = self.bwd_tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Notional position", None));
        ___qtablewidgetitem9 = self.bwd_tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem10 = self.bwd_tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem11 = self.bwd_tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem12 = self.bwd_tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem13 = self.bwd_tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem14 = self.bwd_tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem15 = self.bwd_tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem16 = self.bwd_tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem17 = self.bwd_tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem18 = self.bwd_tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem19 = self.bwd_tableWidget.verticalHeaderItem(10)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem20 = self.bwd_tableWidget.verticalHeaderItem(11)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem21 = self.bwd_tableWidget.verticalHeaderItem(12)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem22 = self.bwd_tableWidget.verticalHeaderItem(13)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem23 = self.bwd_tableWidget.verticalHeaderItem(14)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem24 = self.bwd_tableWidget.verticalHeaderItem(15)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem25 = self.bwd_tableWidget.verticalHeaderItem(16)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem26 = self.bwd_tableWidget.verticalHeaderItem(17)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem27 = self.bwd_tableWidget.verticalHeaderItem(18)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem28 = self.bwd_tableWidget.verticalHeaderItem(19)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem29 = self.bwd_tableWidget.verticalHeaderItem(20)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem30 = self.bwd_tableWidget.verticalHeaderItem(21)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem31 = self.bwd_tableWidget.verticalHeaderItem(22)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem32 = self.bwd_tableWidget.verticalHeaderItem(23)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem33 = self.bwd_tableWidget.verticalHeaderItem(24)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem34 = self.bwd_tableWidget.verticalHeaderItem(25)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem35 = self.bwd_tableWidget.verticalHeaderItem(26)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem36 = self.bwd_tableWidget.verticalHeaderItem(27)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem37 = self.bwd_tableWidget.verticalHeaderItem(28)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem38 = self.bwd_tableWidget.verticalHeaderItem(29)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem39 = self.bwd_tableWidget.verticalHeaderItem(30)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem40 = self.bwd_tableWidget.verticalHeaderItem(31)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem41 = self.bwd_tableWidget.verticalHeaderItem(32)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem42 = self.bwd_tableWidget.verticalHeaderItem(33)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem43 = self.bwd_tableWidget.verticalHeaderItem(34)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem44 = self.bwd_tableWidget.verticalHeaderItem(35)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem45 = self.bwd_tableWidget.verticalHeaderItem(36)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem46 = self.bwd_tableWidget.verticalHeaderItem(37)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem47 = self.bwd_tableWidget.verticalHeaderItem(38)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem48 = self.bwd_tableWidget.verticalHeaderItem(39)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem49 = self.bwd_tableWidget.verticalHeaderItem(40)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem50 = self.bwd_tableWidget.verticalHeaderItem(41)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem51 = self.bwd_tableWidget.verticalHeaderItem(42)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem52 = self.bwd_tableWidget.verticalHeaderItem(43)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem53 = self.bwd_tableWidget.verticalHeaderItem(44)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem54 = self.bwd_tableWidget.verticalHeaderItem(45)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem55 = self.bwd_tableWidget.verticalHeaderItem(46)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem56 = self.bwd_tableWidget.verticalHeaderItem(47)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem57 = self.bwd_tableWidget.verticalHeaderItem(48)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        ___qtablewidgetitem58 = self.bwd_tableWidget.verticalHeaderItem(49)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("MainWindow", u"New Row", None));

        __sortingEnabled = self.bwd_tableWidget.isSortingEnabled()
        self.bwd_tableWidget.setSortingEnabled(False)
        self.bwd_tableWidget.setSortingEnabled(__sortingEnabled)

        self.bxs_btn_type.setText(QCoreApplication.translate("MainWindow", u"Lend", None))
        self.bxs_label_currency.setText(QCoreApplication.translate("MainWindow", u"Currency", None))
        self.bxs_label_index.setText(QCoreApplication.translate("MainWindow", u"Index", None))
        self.bxs_label_expiry.setText(QCoreApplication.translate("MainWindow", u"Expiry", None))
        self.bxs_label_lower_rate.setText(QCoreApplication.translate("MainWindow", u"Lower rate", None))
        self.bxs_label_higher_rate.setText(QCoreApplication.translate("MainWindow", u"Higher rate", None))
        self.bxs_label_benchmark_rate.setText(QCoreApplication.translate("MainWindow", u"Benchmark rate ", None))
        self.bxs_label_selected_rate.setText(QCoreApplication.translate("MainWindow", u"Selected rate", None))
        self.bxs_label_upper_strike.setText(QCoreApplication.translate("MainWindow", u"Upper strike:", None))
        self.bxs_label_lower_strike.setText(QCoreApplication.translate("MainWindow", u"Lower strike:", None))
        self.bxs_label_spread.setText(QCoreApplication.translate("MainWindow", u"Spread:", None))
        self.bxs_label_amount.setText(QCoreApplication.translate("MainWindow", u"Amount:", None))
        self.bxs_label_redemption.setText(QCoreApplication.translate("MainWindow", u"Redemption:", None))
        self.bxs_label_underlying_price.setText(QCoreApplication.translate("MainWindow", u"Price:", None))
        self.bxs_label_type.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.bxs_label_multiplier.setText(QCoreApplication.translate("MainWindow", u"Multiplier: ", None))
        self.bxs_label_principal.setText(QCoreApplication.translate("MainWindow", u"Principal:", None))
        self.btn_message.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: rudizabudi", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v0.0.1", None))
    # retranslateUi

