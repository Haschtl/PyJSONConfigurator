from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
import json
# import touch_messages as QMessages
from functools import partial
import sys

class ConfigGUI(QtWidgets.QDialog):
    def __init__(self, filepath="config.json", stylesheet=""):
        super(ConfigGUI, self).__init__()
        uic.loadUi("configGUI.ui", self)
        self.config = self.load_config(filepath)
        self.filepath = filepath
        self.stylesheet = stylesheet
        self.abortButton.clicked.connect(self.abort)
        self.saveButton.clicked.connect(self.save_config)
        self.resetButton.clicked.connect(self.reset_defaults)
        self.setStyleSheet(self.stylesheet)
        self.dispConfig()
        self.ok = False

    def dispConfig(self):
        for key, configGroup in self.config.items():
            # create Tabs
            w = QtWidgets.QScrollArea()
            w.setWidget(QtWidgets.QWidget())
            tab = QtWidgets.QVBoxLayout(w.widget())
            #w.setLayout(tab)
            w.setWidgetResizable(True)
            self.tabWidget.addTab(w, str(key))
            # self.tabWidget.setTabIcon(idx, str(configGroup))
            self.dispConfigGroup(tab, key, configGroup)
            verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            tab.addItem(verticalSpacer)

    def dispConfigGroup(self, layout, groupKey, configGroup):
        for key, configElement in configGroup.items():
            if type(configElement) == dict:
                # create subGroup
                sublayout = QtWidgets.QVBoxLayout()
                groupEdit = QtWidgets.QLabel(str(configElement))
                sublayout.addWidget(groupEdit)
                self.dispConfigGroup(sublayout, configElement)
            elif type(configElement) in [int, float]:
                configQElement = self.dispNumber(groupKey, key, configElement)
            elif type(configElement) == str:
                configQElement = self.dispString(groupKey, key, configElement)
            elif type(configElement) == bool:
                configQElement = self.dispBool(groupKey, key, configElement)
            layout.addLayout(configQElement)


    def dispNumber(self, group, key, configElement):
        element = QtWidgets.QHBoxLayout()
        configLabel = QtWidgets.QLabel(self.translateString(str(key)))
        configLabel.setFixedHeight(30)
        # configButton = QtWidgets.QPushButton(str(configElement))
        # configButton.setFixedHeight(30)
        # configButton.clicked.connect(partial(self.floatButtonCallback, configButton, group, key, configElement))
        configElement = QtWidgets.QDoubleSpinBox()
        configElement.setFixedHeight(30)
        configElement.setMaximum(16777215)
        configElement.setMinimum(-16777215)
        element.addWidget(configLabel)
        # element.addWidget(configButton)
        element.addWidget(configElement)
        return element

    # def floatButtonCallback(self, configButton, group, key, configElement):
    #     ok, value = QMessages.easy_float_message(self, configElement, -16777215, 16777215)
    #     if ok:
    #         configButton.setText(str(value))
    #         self.config[str(group)][key] = value

    def dispString(self, group, key, configElement):
        element = QtWidgets.QHBoxLayout()
        configLabel = QtWidgets.QLabel(self.translateString(str(key)))
        configLabel.setFixedHeight(30)
        configLineEdit = QtWidgets.QLineEdit(configElement)
        configLineEdit.textChanged.connect(partial(self.stringCallback, configLineEdit, group, key, configElement))
        configLineEdit.setFixedHeight(30)
        element.addWidget(configLabel)
        element.addWidget(configLineEdit)
        return element

    def stringCallback(self, lineEdit, group, key, configElement):
        print("string changed")
        value = lineEdit.text()
        self.config[str(group)][key] = value

    def dispBool(self, group, key, configElement):
        element = QtWidgets.QHBoxLayout()

        configLabel = QtWidgets.QLabel(self.translateString(str(key)))
        configLabel.setFixedHeight(30)
        configCheckbox = QtWidgets.QCheckBox()
        configCheckbox.setFixedHeight(30)
        configCheckbox.setChecked(configElement)
        configCheckbox.stateChanged.connect(partial(self.boolCallback, configCheckbox, group, key, configElement))
        element.addWidget(configLabel)
        element.addWidget(configCheckbox)
        return element

    def boolCallback(self, checkbox, group, key, configElement):
        print("bool changed")
        value = checkbox.isChecked()
        self.config[str(group)][key] = value

    def load_config(self, path="config.json"):
        with open(path, encoding="UTF-8") as jsonfile:
            config = json.load(jsonfile, encoding="UTF-8")
        return config

    def save_config(self):
        with open(self.filepath, 'w', encoding="utf-8") as fp:
            json.dump(self.config, fp)
        self.ok = True
        self.accept()

    def abort(self):
        self.ok = False
        self.accept()

    def reset_defaults(self):
        self.config = self.load_config("config-default.json")
        self.tabWidget.clear()
        self.dispConfig()

    def exec_(self):
        super(ConfigGUI, self).exec_()
        return self.ok, self.config

    def translateString(self, string):
        english = ["global","address","apikey","hotendmin","hotendmax","heatbedmin","heatbedmax","fullscreen","extruders","filamentprice", "filamentdensity", "extrudeMinTemp", "isRaspberry", "debug_level", "manualLink", "filamentsLink", "cameraLink", "autoPlot", "homingoffset","x","y","z", "movement", "xmax", "ymax", "zmax", "maxFeerateXY", "maxFeerateZ", "maxFeerateE", "touchtest", "xmin", "ymin", "changeFilament", "retractd", "temp", "controller", "shutdownEnabled", "tempShutdown", "tempCooldown", "enableTempHistory", "tempHistoryLength", "updateRate", "relaisGPIO", "enclosureGPIO", "enablePowerControl", "enableEnclosureControl", "displayTimeOut","powerprice"]
        deutsch = ["Global","OctoPrint-Adresse","API-Key","Hotend Mintemp","hotend Maxtemp","Heizbett Mintemp","Heizbett Maxtemp","Vollbild","Extruderanzahl","Filamentpreis/kg", "Filamentdichte", "Minimaltemperatur für Extruder", "Raspberry?", "Debug Level", "Link zur Anleitung", "Link zu Filamenten", "Link zur Kamera", "Automatischer Plot aktiviert", "Home-Offset","X [mm]","Y [mm]","Z [mm]", "Bewegungsraum", "max.X [mm]", "max.Y [mm]", "max.Z [mm]", "max. XY Feedrate [mm/s]", "max. Z Feedrate [mm/s]", "max. Extruder Feedrate [mm/s]", "TouchTest", "min.X [mm]", "min.Y [mm]", "Filamentwechsel", "Retract-Distanz [mm]", "Retract-Temperatur", "OctoControl", "ThermalShutdown", "ThermalShutdown Temperatur", "Abkühltemperatur", "Temperaturverlauf", "Temperaturverlauf Dauer [s]", "Display-Updaterate [s]", "PowerRelais GPIO", "EnclosureButton GPIO", "RelaisControl", "EnclosureControl", "Display AutoOff [s]","Stromkosten [/kWh]"]
        #print(string)
        if string in english:
            string = deutsch[english.index(string)]

        return string
		
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = ConfigGUI()
    dialog.exec_()
