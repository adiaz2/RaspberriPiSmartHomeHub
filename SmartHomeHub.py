# qhue is used to help construct urls for communicating with bridge
from qhue import Bridge

# PyQt5 is currently being used
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from functools import partial
import time
import collections


def getIterable(x):
    if isinstance(x, collections.Iterable):
        return x
    else:
        return list(x,)

# Custom Classes
from HuePhillipsLight import HuePhillipsLight
from HuePhillipsGroup import HuePhillipsGroup
from HuePhillipsBridge import HuePhillipsBridge

# setup Hue Phillips bridge by adding your IP and username
# visit the Hue Phillips API to obtain these
BRIDGE_IP = "192.168.1.223"
USERNAME = "ySNf3BZsEWqPgcGTg0Vtw9WS4eYEmPV0YMVN2HSU"

LIGHT_CHECKBOX_ORDER = 0
LIGHT_BRIGHTNESS_SLIDER_ORDER = 1
LIGHT_COLOR_DIALOG_BUTTON_ORDER = 2
LIGHT_COLOR_LOOP_BUTTON_ORDER = 3

QCHECKBOX_UNCHECKED_STATE = 0
QCHECKBOX_CHECKED_STATE = 2


class Ui_MainWindow(QObject):
    def __init__(self, MainWindow):
        super().__init__()
        self.widgetToLight = {}
        self.bridge = HuePhillipsBridge(BRIDGE_IP, USERNAME)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.HuePhillipsGroupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.HuePhillipsGroupBoxLayout = QtWidgets.QGridLayout(self.HuePhillipsGroupBox)
        MainWindow.resize(800, 600)

        self.setupHuePhillipsWidgets()
        self.centralLayout.addWidget(self.HuePhillipsGroupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Setting up the UI
    def setupHuePhillipsWidgets(self):
        for zone in self.bridge.zones.values():
            groupBox = QtWidgets.QGroupBox(self.HuePhillipsGroupBox)
            groupBox.setLayout(QtWidgets.QGridLayout())
            self.createLightWidgets(groupBox, 0, zone, name=zone.name)
            self.HuePhillipsGroupBoxLayout.addWidget(groupBox)
        for room in self.bridge.getRooms():
            groupBox = QtWidgets.QGroupBox(self.HuePhillipsGroupBox)
            groupBox.setLayout(QtWidgets.QGridLayout())
            for row, light in enumerate(room.getLights(), 1):
                self.createLightWidgets(groupBox, row, light)
            self.HuePhillipsGroupBoxLayout.addWidget(groupBox)

    def createLightWidgets(self, groupBox, row, light: HuePhillipsLight, name=None):
        # The order for these variables can be adjusted at the top
        self.createLightCheckBox(groupBox, row, LIGHT_CHECKBOX_ORDER, light, name=name)
        self.createLightBrightnessSlider(groupBox, row, LIGHT_BRIGHTNESS_SLIDER_ORDER, light)
        self.createLightColorDialogButton(groupBox, row, LIGHT_COLOR_DIALOG_BUTTON_ORDER, light)
        self.createColorLoopButton(groupBox, row, LIGHT_COLOR_LOOP_BUTTON_ORDER, light)

    def createLightCheckBox(self, groupBox, row, col, lights: HuePhillipsLight, name=None):
        checkBox = QtWidgets.QCheckBox(groupBox)
        text = name if name else lights.name
        checkBox.setText(text)
        self.widgetToLight[checkBox] = lights
        if lights.isOn:
            checkBox.setCheckState(QCHECKBOX_CHECKED_STATE)
        checkBox.stateChanged.connect(self.toggleLight)
        groupBox.layout().addWidget(checkBox, row, col, 1, 1)

    def createLightBrightnessSlider(self, groupBox, row, col, lights: HuePhillipsLight):
        brightnessSlider = QtWidgets.QSlider(groupBox)
        brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        brightnessSlider.setMinimum(1)
        brightnessSlider.setMaximum(254)
        brightnessSlider.setValue(lights.brightness)
        brightnessSlider.valueChanged.connect(self.changeBrightness)
        self.widgetToLight[brightnessSlider] = lights
        groupBox.layout().addWidget(brightnessSlider, row, col, 1, 1)

    def createLightColorDialogButton(self, groupBox, row, col, lights: HuePhillipsLight):
        button = QtWidgets.QPushButton('Open color dialog', groupBox)
        button.setToolTip('Opens color dialog')
        button.clicked.connect(lambda: self.colorPicker(lights))
        self.widgetToLight[button] = lights
        groupBox.layout().addWidget(button, row, col, 1, 1)

    def createColorLoopButton(self, groupBox, row, col, lights: HuePhillipsLight):
        button = QtWidgets.QPushButton('Start Color Loop', groupBox)
        button.setToolTip('Lights loop through all available colors')
        button.clicked.connect(lambda: self.startColorLoop(lights))
        self.widgetToLight[button] = lights
        groupBox.layout().addWidget(button, row, col, 1, 1)

    # Slots connected to widget signals

    @pyqtSlot()
    def toggleLight(self):
        lights = self.widgetToLight[self.sender()]
        lights.isOn = bool(self.sender().isChecked())

    @pyqtSlot(int)
    def changeBrightness(self, bri):
        lights = self.widgetToLight[self.sender()]
        lights.brightness = bri

    @pyqtSlot()
    def colorPicker(self, lights):
        colorDialog = QtWidgets.QColorDialog(self.sender().parent())
        colorDialog.currentColorChanged.connect(partial(self.colorChanged, lights))
        self.sender().parent().layout().addWidget(colorDialog)

    def colorChanged(self, lights, color):
        lights.newColor(color.hue()*182, color.saturation(), color.value())
        # self.sender().parent().setStyleSheet("background-color: rgb(" + str(color.red()) + ", " + str(color.green()) + ", " + str(color.blue()) + ");")
        if isinstance(lights, HuePhillipsGroup):
            self.sender().blockSignals(True)
            time.sleep(.25)
            self.sender().blockSignals(False)

    def startColorLoop(self, lights):
        lights.startColorLoop()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
