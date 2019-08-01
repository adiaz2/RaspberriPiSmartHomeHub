from qhue import Bridge

# PyQt5 is currently being used
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot

# used for dealing with color conversions
from colors import *  # custom list of values for main colors
import colorsys

# Custom Classes
from HuePhillipsLight import HuePhillipsLight

BRIDGE_IP = "192.168.1.223"
USERNAME = "ySNf3BZsEWqPgcGTg0Vtw9WS4eYEmPV0YMVN2HSU"
b = Bridge(BRIDGE_IP, USERNAME)


