# qhue is used to help construct urls for communicating with bridge
from qhue import Bridge

# PyQt5 is currently being used
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot

# used for dealing with color conversions
from colors import *  # custom list of values for main colors
import colorsys

# Custom Classes
from HuePhillipsLight import HuePhillipsLight

# setup Hue Phillips brige by adding your IP and username
# visit the Hue Phillips API to obtain these
BRIDGE_IP = "192.168.1.223"
USERNAME = "ySNf3BZsEWqPgcGTg0Vtw9WS4eYEmPV0YMVN2HSU"

LIGHT_CHECKBOX_ORDER = 0
LIGHT_BRIGHTNESS_SLIDER_ORDER = 1
LIGHT_COLOR_DIALOG_BUTTON_ORDER = 2


class Ui_MainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.widgetToLight = {}
        self.bridge = Bridge(BRIDGE_IP, USERNAME)

    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.HuePhillipsGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxLayout = QtWidgets.QGridLayout(self.HuePhillipsGroupBox)

        self.setupHuePhillipsWidgets()

        self.centralLayout.addWidget(self.HuePhillipsGroupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.HuePhillipsGroupBox.setTitle(_translate("MainWindow", "Hue Phillips"))

    # Setting up the UI

    def setupHuePhillipsWidgets(self):
        for group in self.bridge()['groups'].keys():
            groupBox = QtWidgets.QGroupBox(self.HuePhillipsGroupBox)
            groupBox.setLayout(QtWidgets.QGridLayout())
            for row, light in enumerate(self.bridge()['groups'][group]['lights']):
                self.createLightWidgets(groupBox, row, light)
            self.groupBoxLayout.addWidget(groupBox)

    def createLightWidgets(self, groupBox, row, light):
        # The order for these variables can be adjusted at the top
        self.createLightCheckBox(groupBox, row, LIGHT_CHECKBOX_ORDER, light)
        self.createLightBrightnessSlider(groupBox, row, LIGHT_BRIGHTNESS_SLIDER_ORDER, light)
        self.createColorDialogButton(groupBox, row, LIGHT_COLOR_DIALOG_BUTTON_ORDER, light)

    def createLightCheckBox(self, groupBox, row, col, light):
        checkBox = QtWidgets.QCheckBox(groupBox)
        checkBox.setText(self.bridge.lights()[light]['name'])
        light = HuePhillipsLight(self.bridge.lights[light])
        self.widgetToLight[checkBox] = light
        if light.isOn:
            checkBox.setCheckState(2)
        checkBox.stateChanged.connect(self.toggleLight)
        groupBox.layout().addWidget(checkBox, row, col, 1, 1)

    def createLightBrightnessSlider(self, groupBox, row, col, light):
        brightnessSlider = QtWidgets.QSlider(groupBox)
        brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        brightnessSlider.setMinimum(1)
        brightnessSlider.setMaximum(255)
        brightnessSlider.setValue(light.brightness)
        brightnessSlider.sliderMoved.connect(self.changeBrightness)
        self.widgetToLight[brightnessSlider] = light
        groupBox.layout().addWidget(brightnessSlider, row, col, 1, 1)

    def createLightColorDialogButton(self, groupBox, row, col, light):
        button = QtWidgets.QPushButton('Open color dialog', groupBox)
        button.setToolTip('Opens color dialog')
        button.clicked.connect(self.colorPicker)
        self.widgetToLight[button] = light
        groupBox.layout().addWidget(button, row, 2, 1, 1)

    # Slots connected to widget signals

    @pyqtSlot()
    def toggleLight(self):
        self.widgetToLight[self.sender()].toggle()

    @pyqtSlot(int)
    def changeBrightness(self, bri):
        if self.widgetToLight[self.sender()].isOn:
            self.widgetToLight[self.sender()].brightness = bri

    @pyqtSlot()
    def colorPicker(self):
        colorDialog = QtWidgets.QColorDialog()
        colorDialog.currentColorChanged.connect(self.colorChanged)
        color = colorDialog.getColor()
        print(color)

    @pyqtSlot(QtGui.QColor)
    def colorChanged(self, color):
        self.widgetToLight[self.sender()].hue = color.hue()
        self.widgetToLight[self.sender()].sat = color.saturation()
        self.widgetToLight[self.sender()].bri = color.value()
        print(color.hue())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
