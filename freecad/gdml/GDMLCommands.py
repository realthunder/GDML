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

__title__="FreeCAD GDML Workbench - GUI Commands"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

'''
This Script includes the GUI Commands of the GDML module
'''

import FreeCAD,FreeCADGui
from PySide import QtGui, QtCore

class importPrompt(QtGui.QDialog):
    def __init__(self, *args):
        super(importPrompt, self).__init__()
        self.initUI()
                
    def initUI(self):
        importButton = QtGui.QPushButton('Import')
        importButton.clicked.connect(self.onImport)
        scanButton = QtGui.QPushButton('Scan Vol')
        scanButton .clicked.connect(self.onScan)
        #
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setFixedWidth(400)
        #buttonBox = Qt.QDialogButtonBox(QtCore.Qt.Vertical)
        buttonBox.addButton(importButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(scanButton, QtGui.QDialogButtonBox.ActionRole)
        #
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
	# define window		xLoc,yLoc,xDim,yDim
        self.setGeometry(	650, 650, 0, 50)
        self.setWindowTitle("Choose an Option    ")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.retStatus = 0

    def onImport(self):
        self.retStatus = 1
        self.close()

    def onScan(self):
        self.retStatus = 2
        self.close()

def getSelectedMaterial() :
    from .exportGDML import nameFromLabel
    from .GDMLObjects import GDMLmaterial

    list = FreeCADGui.Selection.getSelection()
    if list != None :
       for obj in list :
          if hasattr(obj,'Proxy') :
             if isinstance(obj.Proxy,GDMLmaterial) == True :
                return nameFromLabel(obj.Label)

    return 0

def getSelectedPM() :
    from .exportGDML import nameFromLabel
    from .GDMLObjects import GDMLmaterial

    objPart = None
    material = 0
    list = FreeCADGui.Selection.getSelection()
    if list != None :
       for obj in list :
          if hasattr(obj,'Proxy') :
             if isinstance(obj.Proxy,GDMLmaterial) == True and \
                   material == 0 :
                material = nameFromLabel(obj.Label)

          if obj.TypeId == 'App::Part' and objPart is None :
                objPart = obj

          if objPart is not None and material !=0 :
                return objPart, material

    return objPart, material

class ColourMapFeature:

  def Activated(self):
      from PySide import QtGui, QtCore
      #import sys
      from .GDMLColourMap import resetGDMLColourMap, showGDMLColourMap

      print('Add colour Map')
      resetGDMLColourMap()
      showGDMLColourMap()
      return      

      #myWidget = QtGui.QDockWidget()
      #mainWin = FreeCADGui.getMainWindow()
      #mainWin.addDockWidget(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.TopDockWidgetArea, \
      mainWin.addDockWidget(QtCore.Qt.LeftDockWidgetArea or QtCore.Qt.TopDockWidgetArea, \
         myWidget)
      #mainWin.addDockWidget(Qt::LeftDockWidgetArea or Qt::TopDockWidgetArea, myWidget)
      #myWidget.setObjectName("ColourMap")
      #myWidget.resize(QtCore.QSize(300,100))
      #title = QtGui.QLabel("Colour Mapping to GDML Materials")
      #title.setIndent(100)
      #myWidget.setTitleBarWidget(title)
      #label = QtGui.QLabel("Colour Mapping to GDML Materials",myWidget)

  def IsActive(self):
      if FreeCAD.ActiveDocument == None:
         return False
      else:
         return True

  def GetResources(self):
      return {'Pixmap'  : 'GDMLColourMapFeature', 'MenuText': \
              QtCore.QT_TRANSLATE_NOOP('GDMLColourMapFeature',\
             'Add Colour Map'), 'ToolTip': \
              QtCore.QT_TRANSLATE_NOOP('GDMLColourMapFeature',\
              'Add Colour Map')}

class BooleanCutFeature :

    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        import Part

        sel = FreeCADGui.Selection.getSelectionEx()
        if len(sel) == 2 :
           print(sel)
           selObj = 'Gui::SelectionObject'
           if sel[0].TypeId == selObj and sel[1].TypeId == selObj :
              if sel[0].Object.TypeId == 'App::Part' and \
                 sel[1].Object.TypeId == 'App::Part' :
                 print('Boolean Cut')
                 if len(sel[0].Object.InList) > 0  :
                    parent = sel[0].Object.InList[0]
                    print('Parent : '+parent.Label)
                    baseVol = sel[0].Object
                    print('Base Vol : '+baseVol.Label)
                    toolVol = sel[1].Object
                    print('Tool Vol : '+toolVol.Label)
                    print(sel[0].Object.OutList)
                    base = sel[0].Object.OutList[1]
                    print('Base : '+base.Label)
                    tool = sel[1].Object.OutList[1]
                    print('Tool : '+tool.Label)
                    print('Remove Base')
                    baseVol.removeObject(base)
                    print('Adjust Base Links')
                    base.adjustRelativeLinks(baseVol)
                    toolVol.removeObject(tool)
                    tool.adjustRelativeLinks(toolVol)
                    boolVol = parent.newObject('App::Part','Bool-Cut')
                    boolVol.addObject(base)
                    boolVol.addObject(tool)
                    boolObj = boolVol.newObject('Part::Cut','Cut')
                    boolObj.Placement = sel[0].Object.Placement
                    boolObj.Base = base
                    boolObj.Tool = tool
                    boolObj.Tool.Placement.Base = sel[1].Object.Placement.Base \
                                             - sel[0].Object.Placement.Base
                    boolObj.Tool.setEditorMode('Placement',0)
                    print('Remove Base Vol')
                    FreeCAD.ActiveDocument.removeObject(baseVol.Label)
                    FreeCAD.ActiveDocument.removeObject(toolVol.Label)
                    boolObj.recompute()
                 else :
                    print('No Parent Volume/Part')

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Cut', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('gdmlBooleanFeature',\
                'GDML Cut'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('gdmlBooleanFeature',\
                'GDML Cut')}

class BooleanIntersectionFeature :

    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        import Part

        sel = FreeCADGui.Selection.getSelectionEx()
        if len(sel) == 2 :
           print(sel)
           selObj = 'Gui::SelectionObject'
           if sel[0].TypeId == selObj and sel[1].TypeId == selObj :
              if sel[0].Object.TypeId == 'App::Part' and \
                 sel[1].Object.TypeId == 'App::Part' :
                 print('Boolean Intersection')
                 if len(sel[0].Object.InList) > 0 :
                    parent = sel[0].Object.InList[0]
                    print('Parent : '+parent.Label)
                    baseVol = sel[0].Object
                    print('Base Vol : '+baseVol.Label)
                    toolVol = sel[1].Object
                    print('Tool Vol : '+toolVol.Label)
                    baseVol = sel[0].Object
                    print(sel[0].Object.OutList)
                    base = sel[0].Object.OutList[1]
                    print('Base : '+base.Label)
                    tool = sel[1].Object.OutList[1]
                    print('Tool : '+tool.Label)
                    print('Remove Base')
                    baseVol.removeObject(base)
                    print('Adjust Base Links')
                    base.adjustRelativeLinks(baseVol)
                    toolVol.removeObject(tool)
                    tool.adjustRelativeLinks(toolVol)
                    boolVol = parent.newObject('App::Part','Bool-Intersection')
                    boolVol.addObject(base)
                    boolVol.addObject(tool)
                    boolObj = boolVol.newObject('Part::Common','Common')
                    boolObj.Placement = sel[0].Object.Placement
                    boolObj.Base = base
                    boolObj.Tool = tool
                    boolObj.Tool.Placement.Base = sel[1].Object.Placement.Base \
                                             - sel[0].Object.Placement.Base
                    boolObj.Tool.setEditorMode('Placement',0)
                    FreeCAD.ActiveDocument.removeObject(baseVol.Label)
                    FreeCAD.ActiveDocument.removeObject(toolVol.Label)
                    boolObj.recompute()
                 else :
                    print('No Parent Volume/Part')

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Intersection', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('gdmlBooleanFeature',\
                'GDML Intersection'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('gdmlBooleanFeature',\
                'GDML Intersection')}

class BooleanUnionFeature :

    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        import Part

        sel = FreeCADGui.Selection.getSelectionEx()
        if len(sel) == 2 :
           print(sel)
           selObj = 'Gui::SelectionObject'
           if sel[0].TypeId == selObj and sel[1].TypeId == selObj :
              if sel[0].Object.TypeId == 'App::Part' and \
                 sel[1].Object.TypeId == 'App::Part' :
                 print('Boolean Union')
                 if len(sel[0].Object.InList) > 0 :
                    print(sel[0].Object.InList)
                    parent = sel[0].Object.InList[0]
                    print('Parent : '+parent.Label)
                    baseVol = sel[0].Object
                    print('Base Vol : '+baseVol.Label)
                    toolVol = sel[1].Object
                    print('Tool Vol : '+toolVol.Label)
                    baseVol = sel[0].Object
                    print(sel[0].Object.OutList)
                    base = sel[0].Object.OutList[1]
                    print('Base : '+base.Label)
                    tool = sel[1].Object.OutList[1]
                    print('Tool : '+tool.Label)
                    print('Remove Base')
                    baseVol.removeObject(base)
                    print('Adjust Base Links')
                    base.adjustRelativeLinks(baseVol)
                    toolVol.removeObject(tool)
                    tool.adjustRelativeLinks(toolVol)
                    boolVol = parent.newObject('App::Part','Bool-Union')
                    boolVol.addObject(base)
                    boolVol.addObject(tool)
                    boolObj = boolVol.newObject('Part::Fuse','Union')
                    boolObj.Placement = sel[0].Object.Placement
                    boolObj.Base = base
                    boolObj.Tool = tool
                    boolObj.Tool.Placement.Base = sel[1].Object.Placement.Base \
                                             - sel[0].Object.Placement.Base
                    boolObj.Tool.setEditorMode('Placement',0)
                    FreeCAD.ActiveDocument.removeObject(baseVol.Label)
                    FreeCAD.ActiveDocument.removeObject(toolVol.Label)
                    boolObj.recompute()
                 else :
                    print('No Parent Volume')

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Union', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('gdmlBooleanFeature',\
                'GDML Union'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('gdmlBooleanFeature',\
                'GDML Union')}


class BoxFeature:
    #    def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLBox, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-Box")
        else :
           vol=objPart.newObject("App::Part","LV-Box")
        obj=vol.newObject("Part::FeaturePython","GDMLBox_Box")
        #print("GDMLBox Object - added")
        # obj, x, y, z, lunits, material
        GDMLBox(obj,10.0,10.0,10.0,"mm",material)
        #print("GDMLBox initiated")
        ViewProvider(obj.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLBoxFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLBoxFeature',\
                'Box Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLBoxFeature',\
                'Box Object')}

class ConeFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLCone, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-Cone")
        else :
           vol=objPart.newObject("App::Part","LV-Cone")      
        obj=vol.newObject("Part::FeaturePython","GDMLCone_Cone")
        #print("GDMLCone Object - added")
        #  obj,rmin1,rmax1,rmin2,rmax2,z,startphi,deltaphi,aunit,lunits,material
        GDMLCone(obj,1,3,4,7,10.0,0,2,"rads","mm",material)
        #print("GDMLCone initiated")
        ViewProvider(obj.ViewObject)
        #print("GDMLCone ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLConeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLConeFeature',\
                'Cone Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLConeFeature',\
                'Cone Object')}

class EllispoidFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLEllipsoid, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-Ellipsoid")
        else :
           vol=objPart.newObject("App::Part","LV-Ellipsoid")
        obj=vol.newObject("Part::FeaturePython","GDMLEllipsoid_Ellipsoid")
        #print("GDMLEllipsoid Object - added")
        #  obj,ax, by, cz, zcut1, zcut2, lunit,material
        GDMLEllipsoid(obj,10,20,30,0,0,"mm",material)
        #print("GDMLEllipsoid initiated")
        ViewProvider(obj.ViewObject)
        #print("GDMLEllipsoid ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLEllipsoidFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLEllipsoidFeature',\
                'Ellipsoid Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLEllipsoidFeature',\
                'Ellipsoid Object')}

class ElliTubeFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLElTube, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-EllipticalTube")
        else :
           vol=objPart.newObject("App::Part","LV-EllipticalTube")
        obj=vol.newObject("Part::FeaturePython","GDMLElTube_Eltube")
        #print("GDMLElTube Object - added")
        #  obj,dx, dy, dz, lunit, material
        GDMLElTube(obj,10,20,30,"mm",material)
        #print("GDMLElTube initiated")
        ViewProvider(obj.ViewObject)
        #print("GDMLElTube ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLElTubeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLElTubeFeature',\
                'ElTube Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLElTubeFeature',\
                'ElTube Object')}

class SphereFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLSphere, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-Sphere")
        else :
           vol=objPart.newObject("App::Part","LV-Sphere")
        obj=vol.newObject("Part::FeaturePython","GDMLSphere_Sphere")
        #print("GDMLSphere Object - added")
        # obj, rmin, rmax, startphi, deltaphi, starttheta, deltatheta,
        #       aunit, lunits, material
        GDMLSphere(obj,10.0, 20.0, 0.0, 2.02, 0.0, 2.02,"rad","mm",material) 
        #print("GDMLSphere initiated")
        ViewProvider(obj.ViewObject)
        #print("GDMLSphere ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLSphereFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLSphereFeature',\
                'Sphere Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLSphereFeature',\
                'Sphere Object')}

class TrapFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLTrap, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-Trap")
        else :
           vol=objPart.newObject("App::Part","LV-Trap")
        obj=vol.newObject("Part::FeaturePython","GDMLTrap_Trap")
        print("GDMLTrap Object - added")
        # obj z, theta, phi, x1, x2, x3, x4, y1, y2,
        # pAlp2, aunits, lunits, material
        GDMLTrap(obj,10.0,0.0,0.0,6.0,6.0,6.0,6.0,7.0,7.0,0.0,"rad","mm", \
                 material)
        print("GDMLTrap initiated")
        ViewProvider(obj.ViewObject)
        print("GDMLTrap ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLTrapFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTrapFeature',\
                'Trap Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTrapFeature',\
                'Trap Object')}


class TubeFeature:
    #def IsActive(self):
    #    return FreeCADGui.Selection.countObjectsOfType('Part::Feature') > 0

    def Activated(self):
        from .GDMLObjects import GDMLTube, ViewProvider
        objPart, material = getSelectedPM()
        if objPart is None :
           vol=FreeCAD.ActiveDocument.addObject("App::Part","LV-Tube")
        else :
           vol=objPart.newObject("App::Part","LV-Tube")
        obj=vol.newObject("Part::FeaturePython","GDMLTube_Tube")
        #print("GDMLTube Object - added")
        # obj, rmin, rmax, z, startphi, deltaphi, aunit, lunits, material
        GDMLTube(obj,5.0,8.0,10.0,0.52,1.57,"rad","mm",material)
        #print("GDMLTube initiated")
        ViewProvider(obj.ViewObject)
        #print("GDMLTube ViewProvided - added")
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
           return False
        else:
           return True

    def GetResources(self):
        return {'Pixmap'  : 'GDMLTubeFeature', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTubeFeature',\
                'Tube Object'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDMLTubeFeature',\
                'Tube Object')}

class PolyHedraFeature :
      
    def Activated(self) :

        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            print('Action Poly')
            if hasattr(obj,'Shape') :
               print(obj.Shape.ShapeType)
               if hasattr(obj.Shape,'Vertexes') :
                  numVert = len(obj.Shape.Vertexes)
                  print('Number of Vertex : '+str(numVert))
                  #print(obj.Shape.Vertexes)
               if hasattr(obj.Shape,'Faces') :
                  print('Faces')
                  print(dir(obj.Shape.Faces[0]))
                  print(obj.Shape.Faces)
                  planar = self.checkPlanar(obj.Shape.Faces)
                  print(planar)
               if hasattr(obj.Shape,'Edges') :
                  print('Edges')
                  #print(dir(obj.Shape.Edges[0]))
                  #print(obj.Shape.Edges)

    def checkPlanar(self,faces):
        import Part
        print('Check Planar')
        for f in faces :
            if not isinstance(f.Surface, Part.Plane) :
               return False
        return True

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Polyhedra', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_PolyGroup',\
                'Poly Group'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDML_PolyGroup', \
                'PolyHedra Selected Object')}    

class TessellateFeature :
      
    def Activated(self) :
        import Mesh
        import MeshPart
        from .GDMLObjects import GDMLTessellated, GDMLTriangular, \
                  ViewProvider, ViewProviderExtension

        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            print('Action Tessellate')
            if hasattr(obj,'Shape') :
               shape = obj.Shape.copy(False)
               mesh = MeshPart.meshFromShape(Shape=shape,Fineness=2,\
                      SecondOrder=0,Optimize=1,AllowQuad=0)
               print('Points : '+str(mesh.CountPoints))
               #print(mesh.Points)
               print('Facets : '+str(mesh.CountFacets))
               #print(mesh.Facets)
               parent = None
               name ='GDMLTessellate_Tess_'+obj.Name
               if hasattr(obj,'InList') :
                  if len(obj.InList) > 0 :
                     parent = obj.InList[0]
                     myTess = parent.newObject('Part::FeaturePython',name)
               if parent == None :
                  myTess = FreeCAD.ActiveDocument.addObject( \
                           'Part::FeaturePython',name)
               GDMLTessellated(myTess,mesh.Topology[0],mesh.Topology[1], \
                      "mm", getSelectedMaterial())
               myTess.Placement = obj.Placement
               FreeCAD.ActiveDocument.recompute()
               if FreeCAD.GuiUp :
                  ViewProvider(myTess.ViewObject)
                  obj.ViewObject.Visibility = False
                  myTess.ViewObject.DisplayMode = 'Flat Lines'
                  FreeCADGui.SendMsgToActiveView("ViewFit")
    
    def GetResources(self):
        return {'Pixmap'  : 'GDML_Tessellate', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup',\
                'GDML Tessellate Selected Object'), 'Tessellate_Planar': \
                QtCore.QT_TRANSLATE_NOOP('GDML_PolyGroup', \
                'Tesselate Selected Planar Object')}    

class TessellateGmshFeature :
     
    def Activated(self) :
    
        import ObjectsFem
        from .GmshUtils import initialize, meshObj, \
              getVertex, getFacets, getMeshLen, printMeshInfo, printMyInfo

        from femmesh.gmshtools import GmshTools
 
        from .GDMLObjects import GDMLGmshTessellated, GDMLTriangular, \
                  ViewProvider, ViewProviderExtension

        for obj in FreeCADGui.Selection.getSelection():
            initialize()
            parent = None
            if meshObj(obj,2) == True :
               facets = getFacets()
               vertex = getVertex()
               name ='GDMLTessellate_'+obj.Name
               if hasattr(obj,'InList') :
                  if len(obj.InList) > 0 :
                     parent = obj.InList[0]
                     myTes = parent.newObject('Part::FeaturePython',name)
               if parent == None :
                  myTes = FreeCAD.ActiveDocument.addObject( \
                           'Part::FeaturePython',name)
               GDMLGmshTessellated(myTes,obj,getMeshLen(obj),vertex, facets, \
                  "mm", getSelectedMaterial())
               if FreeCAD.GuiUp :
                  obj.ViewObject.Visibility = False
                  ViewProvider(myTes.ViewObject)
                  myTes.ViewObject.DisplayMode = "Wireframe"
                  FreeCAD.ActiveDocument.recompute()
                  FreeCADGui.SendMsgToActiveView("ViewFit")
               
    def GetResources(self):
        return {'Pixmap'  : 'GDML_Tessellate_Gmsh', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup',\
                'Gmsh & Tessellate'), 'Tessellate_Gmsh': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup', \
                'Mesh & Tesselate Selected Planar Object')}    

class Mesh2TessFeature :
     
    def Activated(self) :
 
        from .GDMLObjects import GDMLTessellated, GDMLTriangular, \
                  ViewProvider, ViewProviderExtension

        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            print(obj.TypeId)
            if hasattr(obj,'Mesh') :
               # Mesh Object difficult to determine parent
               print('Action Mesh 2 Tessellate')
               print('Points : '+str(obj.Mesh.CountPoints))
               print('Facets : '+str(obj.Mesh.CountFacets))
               #print(obj.Mesh.Topology[0])
               #print(obj.Mesh.Topology[1])
               a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython", \
                        "GDMLTessellate_Mesh2Tess")
               #a = parent.newObject('Part::FeaturePython', \
               #                    'GDMLTessellate_Mesh2Tess')
               GDMLTessellated(a,obj.Mesh.Topology[0],obj.Mesh.Topology[1], \
                              "mm",getSelectedMaterial())
               if FreeCAD.GuiUp :
                  obj.ViewObject.Visibility = False
                  #print(dir(obj.ViewObject))
                  ViewProvider(a.ViewObject)

               FreeCAD.ActiveDocument.recompute()
               FreeCADGui.SendMsgToActiveView("ViewFit")
               
    def GetResources(self):
        return {'Pixmap'  : 'GDML_Mesh2Tess', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup',\
                'Mesh 2 Tess'), 'Mesh 2 Tess': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessyGroup', \
                'Create GDML Tessellate from FC Mesh')}    

class Tess2MeshFeature :
     
    def Activated(self) :
 
        from .GDMLObjects import GDMLTessellated, GDMLTriangular, \
                  ViewProvider, ViewProviderExtension

        from .GmshUtils import Tessellated2Mesh, Tetrahedron2Mesh

        for obj in FreeCADGui.Selection.getSelection():
            print('Action Tessellate 2 Mesh')
            print(dir(obj.Proxy))
            print(obj.Proxy.Type)
            mesh = None
            if obj.Proxy.Type == 'GDMLTessellated' :
               print('Tessellated2Mesh')
               mesh = Tessellated2Mesh(obj)
    
            if obj.Proxy.Type == 'GDMLGmshTessellated' :
               print('GmshTessellated2Mesh')
               mesh = Tessellated2Mesh(obj)
    
            if obj.Proxy.Type == 'GDMLTetrahedron' :
               print('Tetrahedron2Mesh')
               mesh = Tetrahedron2Mesh(obj)

            if mesh != None :
               print('Add Mesh')
               parent = None
               if hasattr(obj,'InList') :
                  if len(obj.InList) > 0 :
                     parent = obj.InList[0]
                     mshObj = parent.newObject('Mesh::Feature',obj.Name)
               if parent == None :
                     mshObj = FreeCAD.ActiveDocument.addObject( \
                           'Mesh::Feature',obj.Name)
               mshObj.Mesh = mesh
               if FreeCAD.GuiUp :
                  obj.ViewObject.Visibility = False
                  mshObj.ViewObject.DisplayMode = "Wireframe"
                  FreeCAD.ActiveDocument.recompute()
                  FreeCADGui.SendMsgToActiveView("ViewFit")
    
    def GetResources(self):
        return {'Pixmap'  : 'GDML_Tess2Mesh', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup',\
                'Tess2Mesh'), 'Tess 2 Mesh': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup', \
                'Create FC Mesh from GDML Tessellate')}    

class TetrahedronFeature :
     
    def Activated(self) :
 
        from .GDMLObjects import GDMLTetrahedron, ViewProvider
        from .GmshUtils import initialize, meshObj, \
              getTetrahedrons, printMeshInfo, printMyInfo

        for obj in FreeCADGui.Selection.getSelection():
            print('Action Tetrahedron')
            initialize()
            parent = None
            if meshObj(obj,3) == True :
               tetraheds = getTetrahedrons()
               if tetraheds != None :
                  print('tetraheds : '+str(len(tetraheds)))
                  name ='GDMLTetrahedron_'+obj.Name
                  if hasattr(obj,'InList') :
                     if len(obj.InList) > 0 :
                        parent = obj.InList[0]
                        myTet = parent.newObject('Part::FeaturePython',name)
                  if parent == None :
                     myTet = FreeCAD.ActiveDocument.addObject( \
                           'Part::FeaturePython',name)
                  GDMLTetrahedron(myTet,tetraheds,"mm",getSelectedMaterial())
                  if FreeCAD.GuiUp :
                     obj.ViewObject.Visibility = False
                     ViewProvider(myTet.ViewObject)
                     myTet.ViewObject.DisplayMode = "Wireframe"
                     FreeCAD.ActiveDocument.recompute()
                     FreeCADGui.SendMsgToActiveView("ViewFit")
                  else :
                     FreeCAD.Console.PrintMessage('Not able to produce quandrants for this shape')

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Tetrahedron', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup',\
                'Tetrahedron'), 'Tetrehedron': \
                QtCore.QT_TRANSLATE_NOOP('GDML_TessGroup', \
                'Create Tetrahedron from FC Shape')}    

class CycleFeature :

    def Activated(self) :
       
        def toggle(obj) :
            #print ("Toggle "+obj.Label)
            #print (obj.ViewObject.DisplayMode)
            #print (obj.ViewObject.Visibility)
            if obj.ViewObject.Visibility == False :
               try :
                  obj.ViewObject.DisplayMode = 'Shaded'
               except :
                  print(obj.Label+' No Shaded')
               obj.ViewObject.Visibility = True
            else :
               if obj.ViewObject.DisplayMode == 'Shaded' :
                  obj.ViewObject.DisplayMode = 'Wireframe'
               else :
                  obj.ViewObject.Visibility = False 

        def cycle(obj) :
            #print ("Toggle : "+ obj.Label)
            #print (dir(obj))
            #print("TypeId : "+str(obj.TypeId))
            if obj.TypeId == "App::Part" :
               for i in obj.OutList :
                   #print(i)
                   #print(dir(i))
                   #print (i.TypeId)
                   if i.TypeId != "App::Origin" :
                      cycle(i) 
            elif obj.TypeId =="App::Origin" :
                return
            #print obj.isDerivedFrom('App::DocumentObjectGroupPython')
            # Is this a genuine group i.e. Volumes
            # Not Parts with Groups i.e. GDMLPolycone
            elif obj.isDerivedFrom('App::DocumentObjectGroupPython') :
               #print "Toggle Group" 
               for s in obj.Group :
                   #print s
                   cycle(s)

            # Cycle through display options
            elif hasattr(obj,'ViewObject') :
               toggle(obj)

            if hasattr(obj,'Base') and hasattr(obj,'Tool') :
               print ("Boolean") 
               cycle(obj.Base)
               cycle(obj.Tool)
            

        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            cycle(obj)


    def GetResources(self):
        return {'Pixmap'  : 'GDML_Cycle', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_CycleGroup',\
                'Cycle Group'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDML_CycleGroup', \
                'Cycle Object and all children display')}    

def expandFunction(obj, eNum) :
    from .importGDML import expandVolume
    print('Expand Function')
    # Get original volume name i.e. loose _ or _nnn
    name = obj.Label[13:]
    if hasattr(obj,'VolRef') :
       volRef = obj.VolRef
    else :
       volRef = name
    if obj.TypeId != 'App::Link' :
       expandVolume(obj,volRef,eNum,3)
       obj.Label = name


class ExpandFeature :

    def Activated(self) :
      
        print('Expand Feature') 
        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            # add check for Part i.e. Volume
            print("Selected")
            print(obj.Label[:13])
            if obj.Label[:13] == "NOT_Expanded_" :
               expandFunction(obj,0) 
            if obj.Label[:5] == "Link_" :
               if hasattr(obj,'LinkedObject') :
                  if obj.LinkedObject.Label[0:13] == 'NOT_Expanded_' :
                     expandFunction(obj.LinkedObject,0)

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Expand_One', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_Expand_One',\
                'Expand Volume'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDML_Expand_One', \
                'Expand Volume')}    

class ExpandMaxFeature :

    def Activated(self) :
       
        for obj in FreeCADGui.Selection.getSelection():
            #if len(obj.InList) == 0: # allowed only for for top level objects
            # add check for Part i.e. Volume
            print("Selected")
            print(obj.Label[:13])
            if obj.Label[:13] == "NOT_Expanded_" :
               expandFunction(obj,-1)
            if obj.Label[:5] == "Link_" :
               if hasattr(obj,'LinkedObject') :
                  if obj.LinkedObject.Label[0:13] == 'NOT_Expanded_' :
                     expandFunction(obj.LinkedObject,-1)

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Expand_Max', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_Expand_Max',\
                'Max Expand Volume'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDML_Expand_Max', \
                'Max Expand Volume')}    

class CompoundFeature :
    
    def Activated(self) :

        from .GDMLObjects import GDMLcommon
        import ObjectsFem
   
        def allocateMaterial(doc, analObj, materials, material) :
            print("Allocate Material : ",material)
            for n in materials.OutList :
                if n.Label == material :
                   print("Found Material") 
                   matObj = ObjectsFem.makeMaterialSolid(doc, material)
                   mat = matObj.Material
                   mat['Name'] = material
                   mat['Density'] = str(n.density) + " kg/m^3"
                   mat['ThermalConductivity'] = str(n.conduct) + " W/m/K"
                   mat['ThermalExpansionCoefficient'] = str(n.expand) + " m/m/K"
                   mat['SpecificHeat'] = str(n.specific) + " J/kg/K"
                   print(mat)
                   print(mat['Density'])
                   matObj.Material = mat
                   analObj.addObject(matObj)

        def addToList(objList, matList, obj) :
            print(obj.Name) 
            if hasattr(obj,'Proxy') :
               #print("Has proxy")
               #material_object = ObjectsFem.makeMaterialSolid \
               #                  (doc,obj.Name+"-Material")
               #allocateMaterial(material_object, obj.Material)
               if isinstance(obj.Proxy,GDMLcommon) :
                  objList.append(obj)
                  if obj.material not in matList :
                     matList.append(obj.material) 
       
            if obj.TypeId == 'App::Part' and hasattr(obj,'OutList') :
               #if hasattr(obj,'OutList') :
               #print("Has OutList + len "+str(len(obj.OutList)))
               for i in obj.OutList : 
                  #print('Call add to List '+i.Name)
                  addToList(objList, matList, i)

        def myaddCompound(obj,count) :
            # count == 0 World Volume
            print ("Add Compound "+obj.Label)
            volList = []
            matList = []
            addToList(volList, matList, obj)
            if count == 0 :
               del volList[0]
               del matList[0]
            # DO not delete World Material as it may be repeat
            print('vol List')   
            print(volList)
            print('Material List')
            print(matList)
            doc = FreeCAD.activeDocument()
            analysis_object = ObjectsFem.makeAnalysis(doc,"Analysis")
            materials = FreeCAD.ActiveDocument.Materials
            for m in matList :
                allocateMaterial(doc, analysis_object, materials, m)
            comp = obj.newObject("Part::Compound","Compound")
            comp.Links = volList
            FreeCAD.ActiveDocument.recompute()


        objs = FreeCADGui.Selection.getSelection()
        #if len(obj.InList) == 0: # allowed only for for top level objects
        print(len(objs))
        if len(objs) > 0 :
           obj = objs[0]
           if obj.TypeId == 'App::Part' :
              myaddCompound(obj,len(obj.InList))

    def GetResources(self):
        return {'Pixmap'  : 'GDML_Compound', 'MenuText': \
                QtCore.QT_TRANSLATE_NOOP('GDML_Compound',\
                'Add compound to Volume'), 'ToolTip': \
                QtCore.QT_TRANSLATE_NOOP('GDML_Compound', \
                'Add a Compound of Volume')}    

FreeCADGui.addCommand('CycleCommand',CycleFeature())
FreeCADGui.addCommand('ExpandCommand',ExpandFeature())
FreeCADGui.addCommand('ExpandMaxCommand',ExpandMaxFeature())
FreeCADGui.addCommand('ColourMapCommand',ColourMapFeature())
FreeCADGui.addCommand('BooleanCutCommand',BooleanCutFeature())
FreeCADGui.addCommand('BooleanIntersectionCommand',BooleanIntersectionFeature())
FreeCADGui.addCommand('BooleanUnionCommand',BooleanUnionFeature())
FreeCADGui.addCommand('BoxCommand',BoxFeature())
FreeCADGui.addCommand('EllipsoidCommand',EllispoidFeature())
FreeCADGui.addCommand('ElTubeCommand',ElliTubeFeature())
FreeCADGui.addCommand('ConeCommand',ConeFeature())
FreeCADGui.addCommand('SphereCommand',SphereFeature())
FreeCADGui.addCommand('TrapCommand',TrapFeature())
FreeCADGui.addCommand('TubeCommand',TubeFeature())
FreeCADGui.addCommand('PolyHedraCommand',PolyHedraFeature())
FreeCADGui.addCommand('AddCompound',CompoundFeature())
FreeCADGui.addCommand('TessellateCommand',TessellateFeature())
FreeCADGui.addCommand('TessellateGmshCommand',TessellateGmshFeature())
FreeCADGui.addCommand('Mesh2TessCommand',Mesh2TessFeature())
FreeCADGui.addCommand('Tess2MeshCommand',Tess2MeshFeature())
FreeCADGui.addCommand('TetrahedronCommand',TetrahedronFeature())
