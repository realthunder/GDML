## **** VERY IMPORTANT - Upgrade FreeCAD 0.19 to 22665 or later ****

**Changes to Placement ( GDML Position & Rotation )**

In order to support copies of GDML Volumes the following changes have been made

  * As per GDML one GDML Volume(FreeCAD Part) containes one Solid
  * GDML position and Rotation as defined in PhysVol are now transfered to the associated FreeCAD Part
  * The only time you can change a GDML Objects Placement is when it is part of a Boolean
  * Copies are implemented as App::Links i.e. Link to Volume being copied.
  * Copies of Volumes require function only available since FreeCAD 0.19
  
There was a regression in FreeCAD 0.19 that affected the above changes, so you need to
update to a later version of FreeCAD 0.19. You are therefore advised to update to at least FreeCAD 0.19 - 22665.

For latest versions of FreeCAD 0.19 see the Assets section of https://github.com/FreeCAD/FreeCAD/releases

## **** New experimental export for GEMC ****

## **** Wiki Under Construction ****

## Installable FreeCAD Python Workbench

FreeCAD's python Importer & Exporter for GDML files.

## Installation of FreeCAD
see https://wiki.freecadweb.org/Installing#Choose_Your_Operating_System

## Installation of Workbench

GDML can be installed via the Addon Manager 
https://wiki.freecadweb.org/Std_AddonMgr

Install by use of FreeCAD Addon Manager ==> GDML ==> update

## Required python libraries - lxml & gmsh

### lxml - python library

lxml which should be installed as part of FreeCAD

   * FreeCAD_0.19.19424 and above.
   * FreeCAD_0.19.19409_x64_Conda_Py3QT5-WinVS2015.7z and above.
   

#### Checking required python libraries available to FreeCAD

To check path FreeCAD uses from a command line/window.

    freecad -c
    import sys
    print(sys.path)

#### Manual install of lxml

    pip3 install lxml -t < directory >
  
#### Check lxml correctly installed

    freecad -c
    import lxml
    from lxml import etree
    print(etree.LXML_VERSION)

#### FreeCAD version 0.18

There are known limitations with FreeCAD 0.18 and **lxml**  it is recommended that you use FreeCAD 0.19 as above.
( Note: You can install both versions 0.18 & 0.19 and still use 0.18 for non GDML related work )   

### gmsh - python library

Must be installed in a location that FreeCAD sees to check path FreeCAD uses from a command line/window.

    freecad -c
    import sys
    print(sys.path)

In a command window / line

    pip install --upgrade --target <Full path to directory> gmsh
  
Windows: if no --target option upgrade pip   

    python -m pip install -U pip
        
For example on Windows system where FreeCAD is installed on the D drive

    pip install --target="D:\FreeCAD 0.19\FreeCAD_0.19\bin\Lib\site-packages" gmsh
    
will create 

    D:\FreeCAD 0.19\FreeCAD_0.19\bin\Lib\site-packages\gmsh-4.6.0-py3.8.egg-info
    D:\FreeCAD 0.19\FreeCAD_0.19\bin\Lib\site-packages\Lib\site-packages\gmsh-4.6.0-Windows64-sdk
     
## Details of GDML

For more information on GDML see

[GDML User Guide](https://gdml.web.cern.ch/GDML/doc/GDMLmanual.pdf)

[GDML Solids](http://geant4-userdoc.web.cern.ch/geant4-userdoc/UsersGuides/ForApplicationDeveloper/html/Detector/Geometry/geomSolids.html)

## Usage

### GDML Solids

GDML Solids are implemented as FreeCAD Python Objects and have the same properties as defined by GDML. By selecting an Object the properties can be changed via the FreeCAD properties windows and the resulting changes displayed.

### FreeCAD View settings

It is suggested that you have the **View** | **Toolbars**
set to

* Workbench
* Structure

and when GDML workbench active

* GDMLTools
* GDML Part tools

### Create a new GDML design

1. Start FreeCAD
2. Select the **GDML workbench** from the workbench dropdown menu.
3. Select **File > New**  
   Result: This will load the default GDML File with materials and creates a World Volume.  
4. Create `1-n Volumes` in the World Volume by
   * Click on the Part icon (image: yellow blockish icon)
   * Drag the created **Part** to the World Volume in the **Tree** window
   * **Part** maybe renamed via right click context menu  
5. Create GDML Solids by:  
   * Clicking on the corresponding icon of the workbench, this will create a Part(GDML Volume) which contains the GDMLsolid
   * You can then change the attributes by selecting the GDMLObject in the **Tree** window and changing the properties in the **Property View**
   * You can alter the position and rotation by changing the Placement parameters in the Part(GDML Volume)
   * You can select and drag the Part(GDML Volume) to the appropriate part of the overall model strcuture
      
  So a valid structure for a GDML file is:  
   * Single World Volume (Part)
   * A number of Volumes (Parts) under the World Volume
 
6. To Export to GDML
    1. Select the 'World' Volume ( Default Name WorldVol )
    2. File export
    3. Select filetype as GDML ( Bottom Box of **Export file** window)
    4. Select Destination and file name with **GDML** as file extension 

**Important Notes:**  
* Opening a new file when the GDML workbench is active will load a Default file.
* The Default file is defined in `GDML/Mod/Resources/Default.gdml`.
* If a material is selected in 'Labels & Attributes window at the time a new GDML objects is created
  then this will set the material of the new Object. If no material is selected the objects material is set to the
  first material in the Defaults file i.e. `SSteel0x56070ee87d10`
  
## GDML Object Creation

Upon switching to the GDML workbench, one will notice a number of icons that become available on the Workbench bar.

* Clicking on one of the icons will create a Part(GDMLvolume) containing the GDML object

  If at the time a material is selected e.g. in the 'Labels & Attributes' window,
  then the object will be created with that material, otherwise the material will be set to the first material in the list.
  
* You can then alter the Objects properties via the properties window. The parameters should be the same as in the [GDML user guide]().
* Note: If you toggle values via your mouse, you then need to hit enter for the changes to show in the main view.
* If the Object is part of a Boolean you will have to use the **recompute** facility of FreeCAD to see the change to the Boolean. This can be achieved through the right clicking on the context menu or clicking the **Recompute** icon in the toolbar.
* If a Part(GDML Volume) is selected at the time of clicking on the icon, then the new Part(GDML volume ) and GDML object will be created as
a subvolume of the one selected, otherwise the created Part can then be dragged to the appropriate part of model structure

### GDML Objects Currently Supported for creation via the GUI are

#### GDMLBox 
![GDML_Box-Icon](Source_Icon_Designs/GDML_Box_mauve_blackline.svg)
_Short decription_

#### GDMLCone
![GDML_Clone-Icon](Source_Icon_Designs/GDML_Polycone_Mauve_blackline.svg)
_Short decription_

#### GDMLElTube
![GDML_EllipticalTube-Icon](Source_Icon_Designs/GDML_EllipticalTube_Mauve_blackline.svg)
_Short decription_

#### GDMLEllipsoid
![GDML_Ellipsoid-Icon](Source_Icon_Designs/GDML_Ellipsoid_Mauve_blackline.svg)
_Short decription_

#### GDMLSphere
![GDML_Sphere-Icon](Source_Icon_Designs/GDML_Sphere_mauve.svg)
_Short decription_

#### GDMLTrap
![GDML_Trapezoid-Icon](Source_Icon_Designs/GDML_Trapezoid_Mauve_blackline.svg)
_Short decription_

#### GDMLTube
![GDML_Tube-Icon](Source_Icon_Designs/GDML_Tube_mauve_blackline.svg)
_Short decription_

Given a lot more solids are supported for import, it is not too difficult to add more,
so if you feel you need a particular solid to be added please contact me.

### Boolean Operations

Select two Parts/Logical Volumes and then click on the appropriate boolean icon


## GDML Tessellated Objects

The following icons are available for Tessellated operations

### Tessellate
![GDML Tessellate-Icon](freecad/gdml/Resources/icons/GDML_Tessellate.svg) Tessellate

If the selected FreeCAD object has a Shape then a GDML Tesselated Object is created by using the Meshing
Workbench default options. If a material is also selected this will determine the GDML material of the
created GDML Tessellated Object

### Tessellate with Gmsh
![GDML Tessellate_Gmsh](freecad/gdml/Resources/icons/GDML_Tessellate_Gmsh.svg)

If the selected FreeCAD object has a Shape or Mesh then a GDML Tesselated Object is created by using gmsh.

The initial mesh size is determined by the shapes bounding box divided by 10.

You can **remesh** a copy of the original object by changing the properties of the created GDMLTesselate Object
    
    m_max Length - CharacteristicLengthMax
    m_curve Len  - CharacteristicLengthFromCurvature
    m_point Len  - CharacteristicLengthFromPoints
    
and then changing the **m_Remesh** property to True.

Note: For some reason there appears to be a delay in updating the new number of vertex. facets counts displayed.

### FC Mesh to GDML Tessellated
![GDML FC-Mesh2Tess-Icon](freecad/gdml/Resources/icons/GDML_Mesh2Tess.svg) Mesh to GDML Tessellated

If the selected FreeCAD object is a mesh then a GDML Tessellated Object is created. Again if a material is
also selected then this will set the GDML material of the GDML Tessellated Object.

   1) FreeCAD Supports a large number of mesh file formats including stl, ply, etc
      so **Mesh 2 Tessellate** allows these to be converted to a GDML Tessellate object
      
   2) The Mesh Workbench offers a range of meshing facilites with options ( Meshes | create mesh from Shape )
   
      * Standard
      * Mefisto
      * Netgen
      * Gmsh ( Requires FreeCAD 0.19+ )
      * Gmsh also offers a **Remesh** facility ( Meshes | Refinement )
      
      So having created a mesh using the Mesh workbench, one can then switch to the GDML Workbench to
      create GDML Tessellated objects from these.
      
### GDML Tessellated to FC Mesh
![GDML Tess2FC-Mesh](freecad/gdml/Resources/icons/GDML_Tess2Mesh.svg) GDML Tessellated to FC Mesh

If the selected FreeCAD object is a GDML Tessellated Object a FreeCAD Mesh is created.      

### GDML Tetrahedron (GDML Assembly of GDML Tetra)
![GDML_Tetrahedron](freecad/gdml/Resources/icons/GDML_Tetrahedron.svg) GDML Tetrahedron

If the selected FreeCAD object has a Shape or is a Mesh then a Tetrahedera Object is created by using gmsh.
This can then be exported as a GDML Assembly of GDML Tetra

If you would like to see support of remeshing of Tetrahedra the same as Tessellated then please contact me or raise as an issue.

## GDML Import

A lot more GDML solids are supported for import. For example all Solids
used by the CERN Alice.gdml are defined.

On import or open of a GDML file a Dialog box will open with two options

- Import
- Scan Vol

Import will do a straight import of GDML Objects.

Scan Vol is for large files like Alice.GDML that take far too long to process. 

Volumes are only processed to a limit depth i.e. volume names are determined but not processed
For unprocessed volume the names are preceded by **`NOT_Expanded`** so an example volume name would be: `NOT_Expanded_<VolumeName>`

#### Expansion of Scanned Volume

Unexpanded Volumes can be expanded by:  
1. Switching to the GDML workbench.
2. Selecting a volume in the **_labels & attributes_** window
3. Clicking on the experimental Expand Volume icon **'E'**

On opening of a GDML file the appropriate FreeCAD implemented python Object is created for each solid

## Viewing Volumes

The first icon on the workbench bar is different. If you select a object by one of the following methods  

1. A volume via the Combo view - Model - Labels & Attributes.

   Then click on the icon it will cycle the display mode of the selected Volume and all its children.
   The cycle is Solid -> WireFrame -> Not Displayed -> Solid

2. In the main display - select a face by <ctrl> <left mouse>
   
   Then click on the icon it will cycle the display mode of the selected object
   
## SampleFiles

[SampleFiles](SampleFiles/) directory contains some sample gdml files. 

One in particular is lhcbvelo.gdml. This file takes a LONG LONG time to import/open, over a minute on my system, but does eventually load. On my system I have to okay one wait. When it finally does display you will want to zoom in.

If when it is displayed you go down the Volumes tree to VelovVelo under the World volume then click on the toggle icon ( 1st GDML icon in the workbench) Again wait patiently and the display will change to wireframe. You can
then decend further down the Volumes tree, select one and again use the toggle icon and that volume and children will change to Solid. In this way various parts in different volumes can be examined.

## GDML Objects Exporter 

To export to GDML 

1. Select the 'world' Volume, should be first Part in Design
2. File export
3. Select GDML as filetype
4. Make sure file has GDML as file extension

### GDML Objects

GDMLObjects are output as straight GDML solids

### FreeCAD Objects

The following FreeCAD objects are output as GDML equivalents

| FreeCAD   |   GDML     |
| :-----:   |  :----:    |
| Cube      |  Box       |
| Cone      |  Cone      |
| Cylinder  |  Tube      |
| Sphere    |  Sphere    |

If not handled as above then objects shapes are checked  to see if planar,
if yes converts to Tessellated Solid with 3 or 4 vertex as appropriate.
If not creates a mesh and then a Tessellated solid with 3 vertex.

### Export of STEP version

Standard FreeCAD export facilities are available which includes the ability to create a STEP version

### Export/Import of Materials as an XML file.

If you select the Materials Group in Tree view and then use the standard FreeCAD export,
the export will create an xml file of the material definitions. You can then import this
file and the material definitions into a separate FreeCAD document. Note: The file extension
used should be xml NOT gdml

The Materials directory contains a number of Materials XML files including NIST Database
that can be imported.

## GEMC

This is still at an early stage of development and has some rough edges, extra support will be added over time

### Import of STEP file for GEMC

The FreeCAD default settings for Import of a STEP file is to create a single Compound,
so the FreeCAD Import/Export Preferences for STEP Import should be set as follows

![Import STEP](/Images/Step-import-Options.png)

1) Make sure Import/Export Preferences are set. (Avoid Compound and LinkGroup)
2) Open the STEP File

#### To access FreeCAD STEP Preferences

 1) Select **FreeCAD-version-number** from the Tool bar
 2) Then **Preference**
 3) In left hand column select Import/Export
 
 ![Import Export|30x30.20%](/Images/Import-Export.png)
 
 4) Then from top TAB = STEP
 5) This displays the Export options followed by the Import Options

### Export for GEMC

1) Switch to the GDML workbench if not the current workbench
2) Click on colourMap Icon ![GDML ColourMap-Icon](freecad/gdml/Resources/icons/GDMLColourMapFeature.svg) ColourMap
3) Allocate Materials to Colours
4) Select Export on the Toolbar
5) Enter directory path ( No file extension )
6) Select the Export type ( Note: Filetype is Not used )

   * Selecting GEMC lower case option GEMC - stp (*.gemc) 
       
     This creates a directory structure for a CAD Factory - Where all FreeCAD Objects with Shapes are exported as stl files

   * Selecting GEMC upper case otion GEMC - gdml (*.GEMC)
     
     Then GDML objects and FreeCAD Object that directly convert are output in a GDML file of a GDML Factory,
     Other Objects with a Shape are output as STL files in a CAD Factory.
       
### Constants / Isotopes / Elements / Materials

Importing a GDML will create FreeCAD objects for the above and export should
create the same GDML definitions as imported.

The Ability to change to change these maybe implemented in the future.
 
## Preferences

There is now an option to toggle `Printverbose` flag to reduce printing to the python console.

## Compound & FEM - Finite Element Analysis

### Use of `compound` icon     ![GDML_MakeCompund ](freecad/gdml/Resources/icons/GDML_Compound.svg)   GDML Compound
to facilitate preperation for FEM analysis

#### Usage

* **Select** a volume/Part i.e. the first Part which is the GDML world volume and **click on** the `compound` icon **'C'**
  1. Creates an object named **Compound** under the selected Volume
  2. Create an FEM Analysis Object.
  3. All the materials of the objects in the Volume/Part/Compound are added to the Analysis Object.
  
* You can then switch to the **FEM Workbench** (_Finite Element Analysis_) and proceed with an analysis which would include:
  
  1. Double click on each of the materials to edit their properties
  2. From the FEM workbench select the Compound Object and click on the icon to create a Mesh.
  3. Rest would depend on what analysis and what solver it is intended to use.
  
  Also as an experiment: thermal parameters have been added to the `GDMLmaterial` object so these could
  be changed before creating a compound. One option to be would be to add elements to GDML files to enable
  loading and exporting, but then they would **NOT** be standard GDML files (maybe a different file extension?)  
  
## Standalone Utilities

The standalone utilities and documentation are now in a submodule repository https://github.com/KeithSloan/GDML_Command_Line_Utils  

  In directory **Utils** You will find a python script **gdml2step.py** for creating a step file from a gdml file.
  
  syntax is
   
         python3 gdml2step.py <input gdml file> <output step file>
         
         The step file should be given a .step extension.
         
         In theory other file extension should produce a file of the appropriate type,
         e.g. iges, but this is untested.
         
## Citing information
[![DOI](https://zenodo.org/badge/223232841.svg)](https://zenodo.org/badge/latestdoi/223232841)

![DOI_image](Documentation/DOImage.png)

## Roadmap

  - [ ] Change structure of xml handing to use Python class rather than global variables
  - [ ] Check handling of different Positioning between GDML & FreeCAD
  - [ ] Add support for quantity
  - [ ] Add further GDML Objects
  - [ ] Add facility to edit Materials
  - [ ] Add facility to edit Isotopes
  - [ ] Add facility to edit Elements 
  - [ ] Documentation
  - [ ] Investigate handling of Materials
  - [ ] Need to sort out AIR definition

**Workbench**

  - [ ] Workbench Dialog for initial GDML Object values(?)
  - [ ] Analyze FreeCAD file for direct conversion of object to GDML solid
  - [ ] Display mesh for objects that will not directly convert
  - [ ] Provide options to control meshing objects that will be Tessellated
  - [ ] Icons to Analize and Export

**Note:**
For NIST Materials database see http://physics.nist.gov/PhysRefData

## Development Notes
 
 based on gdml.xsd
 
 * 'Volumes'
 
    * **Must** have **solid & material ref**
 
 * PhysVol 
 
     * Must contain **volref** ( or file ) 
     * volref **must not** be same as current volume name
     * May contain **position** or **position ref**
     * May contain **rotation** or **rotation ref**
 
## Acknowledgements 

**Developers**

  * Keith Sloan
  * Damian Lambert

**Graphic Icons** 

* GDML Shapes designed by Jim Austin (jmaustpc)  
* Cycle icon by Flaticon see www.flaticon.com

**Thank you also to:** 

  * Louis Helary
  * Emmanuel Delage
  * Wouter Deconnick
  * Hilden Timo
  * Atanu Quant
  
* FreeCAD forum members (Applogies if I left anybody off ) :

  * wmayer
  * Joel_graff
  * chrisb
  * DeepSOIC
  * ickby
  * looooo
  * easyw-fc
  * bernd
  * vocx
  * sgrogan
  * onekk (Carlo D)
  * OpenBrain

* OpenCascade Forum members:
  *  Sergey Slyadnev
  
* Stack Overflow

  * Daniel Haley
    
## For NIST Materials database see http://physics.nist.gov/PhysRefData

## Need to sort out AIR definition

## Feedback

Please report bugs by opening a ticket in the  [FreeCAD_Python_GDML issue queue](https://github.com/KeithSloan/FreeCAD_Python_GDML/issues)

**Note: I am always on the look out for test gdml files (small to medium size)XXXX# FreeCAD_Python_GDML**

To contact the author via email: keith[at]sloan-home[dot]co[dot]uk 
