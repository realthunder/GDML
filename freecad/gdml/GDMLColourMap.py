#**************************************************************************
#*                                                                        *
#*   Copyright (c) 2017 Keith Sloan <keith@sloan-home.co.uk>              *
#*             (c) Dam Lambert 2020                                          *
#*                                                                        *
#*   This program is free software; you can redistribute it and/or modify *
#*   it under the terms of the GNU Lesser General Public License (LGPL)   *
#*   as published by the Free Software Foundation; either version 2 of    *
#*   the License, or (at your option) any later version.                  *
#*   for detail see the LICENCE text file.                                *
#*                                                                        *
#*   This program is distributed in the hope that it will be useful,      *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
#*   GNU Library General Public License for more details.                 *
#*                                                                        *
#*   You should have received a copy of the GNU Library General Public    *
#*   License along with this program; if not, write to the Free Software  *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
#*   USA                                                                  *
#*                                                                        *
#*   Acknowledgements :                                                   *
#*                                                                        *
#**************************************************************************

__title__="FreeCAD GDML Workbench - GDMLColourMap"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

import FreeCAD
import FreeCADGui

#from PySide2 import QtGui, QtCore
from PySide import QtGui, QtCore

def resetGDMLColourMap():
    print('Reset Colour Map')
    global workBenchColourMap
    try :
       del workBenchColourMap
    except NameError:
       pass

    workBenchColourMap = GDMLColourMap(FreeCADGui.getMainWindow())

def showGDMLColourMap():
    print('Display Colour Map')
    workBenchColourMap.show()

def lookupColour(col) :
    global workBenchColourMap
    print('Lookup Colour')
    try :
        mat = workBenchColourMap.lookupColour(col)
     
    except NameError:
        workBenchColourMap = GDMLColourMap(FreeCADGui.getMainWindow())
        mat = workBenchColourMap.lookupColour(col)
      
    return mat

class GDMLColour(QtGui.QWidget):
  
   def __init__(self,colour):
      super().__init__()
      self.setAutoFillBackground(True)
      self.resize(50, 20)

      palette = self.palette()
      palette.setColor(QtGui.QPalette.Window, QtGui.QColor(colour))
      self.setPalette(palette)

class GDMLMaterial(QtGui.QComboBox):
    
   def __init__(self,matList) :
      super().__init__()
      self.addItems(matList)
      self.setEditable(False)

   def getItem(self):
      return str(self.currentText)
 

class GDMLColourMapEntry(QtGui.QWidget) :

   def __init__(self,colour,material) :
      super().__init__()
      print('Map Entry : '+str(colour))
      self.colour = colour
      self.hbox = QtGui.QHBoxLayout()
      self.hbox.addWidget(GDMLColour(colour))
      self.hbox.addWidget(material)
      self.setLayout(self.hbox)

   def dataPicker(self):
      print('DataPicker')

class GDMLColourMapList(QtGui.QScrollArea) :

   def __init__(self,matList) :
      super().__init__()
      # Scroll Area which contains the widgets, set as the centralWidget
      # Widget that contains the collection of Vertical Box
      self.widget = QtGui.QWidget()
      self.matList = matList
      # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
      self.vbox = QtGui.QVBoxLayout()
      self.widget.setLayout(self.vbox)

      #Scroll Area Properties
      self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
      self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.setWidgetResizable(True)
      self.setWidget(self.widget)

   def addEntry(self, colour) :
      print('Add Entry')
      mat = GDMLMaterial(self.matList)
      self.vbox.addWidget(GDMLColourMapEntry(colour,mat))

class GDMLColourMap(QtGui.QDialog) :
#class GDMLColourMap(QtGui.QMainWindow) :
   def __init__(self, parent) :
      super(GDMLColourMap, self).__init__(parent, QtCore.Qt.Tool)
      self.initUI()

   def initUI(self):   
      self.result = userCancelled
      # create our window
      # define window           xLoc,yLoc,xDim,yDim
      self.setGeometry( 250, 450, 550, 550)
      self.setWindowTitle("Map FreeCAD Colours to GDML Materials")
      self.setMouseTracking(True)
      lay = QtGui.QGridLayout(self)
      
      materialList = self.getGDMLMaterials()
      self.mapList = GDMLColourMapList(materialList)
      doc = FreeCAD.ActiveDocument
      print('Active')
      print(doc)
      if doc != None :
         #print(dir(doc))
         if hasattr(doc,'Objects') :
            #print(doc.Objects)
            self.colorList = []
            for obj in doc.Objects :
                #print(dir(obj))
                if hasattr(obj,'ViewObject') :
                   #print(dir(obj.ViewObject))
                   if hasattr(obj.ViewObject,'isVisible') :
                      if obj.ViewObject.isVisible :
                         if hasattr(obj.ViewObject,'ShapeColor') :
                            colour = obj.ViewObject.ShapeColor
                            print(colour)
                            try:
                               col = self.colorList.index(colour)
                            except ValueError:
                               self.colorList.append(colour)
      print(self.colorList)
      for c in self.colorList :
          self.mapList.addEntry(QtGui.QColor(c[0]*255,c[1]*255,c[2]*255))
      # create Labels
      self.label1 = self.mapList 
      lay.addWidget(self.label1,0,0)
      #  cancel button
      cancelButton = QtGui.QPushButton('Cancel', self)
      cancelButton.clicked.connect(self.onCancel)
      cancelButton.setAutoDefault(True)
      lay.addWidget(cancelButton, 2, 1)

      # OK button
      okButton = QtGui.QPushButton('OK', self)
      okButton.clicked.connect(self.onOk)
      lay.addWidget(okButton, 2, 0)
      # now make the window visible
      self.setLayout(lay)
      self.show()
      
   def lookupColour(self, col) :
       print('Lookup Colour')
       idx = self.colorList.index(col)
       print(idx)
       entry = self.mapList.vbox.itemAt(idx).widget()
       print(entry)
       mat = entry.hbox.itemAt(1).widget().currentText()
       print(mat)
       return mat

   def onCancel(self):
       self.result = userCancelled
       self.close()

   def onOk(self):
       self.result = userOK
       self.close()

   def getGDMLMaterials(self):
       matList = []
       doc = FreeCAD.activeDocument()
       try :
          materials = doc.Materials
       except :
          from .importGDML import processXML
          from .init_gui   import joinDir

          print('Load Geant4 Materials XML')
          processXML(doc,joinDir("Resources/Geant4Materials.xml"))
          materials = doc.Materials

       if materials != None :
          for m in materials.OutList :
              matList.append(m.Label)
          #print(matList)

       else :
          print('Materials Not Found')

       return matList      


# Class definitions

# Function definitions

# Constant definitions
global userCancelled, userOK
userCancelled           = "Cancelled"
userOK                  = "OK"

