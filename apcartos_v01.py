from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys
import os
import resource

#Import legend class
from legend import Legend

# Import our GUI
from apcartos_v01_gui import Ui_MainWindow

# Environment variable QGISHOME must be set to the install directory
# before running the application
qgis_prefix = os.getenv("QGISHOME")

class ShapeViewer(QMainWindow, Ui_MainWindow):

  
  def __init__(self):
    QMainWindow.__init__(self)
    self.activeCanvas = None
    self.activeTool = None
    # Required by Qt4 to initialize the UI
    self.setupUi(self)

    # Set the title for the app
    self.setWindowTitle("APCartOS v0.2")
    
    # Create the legend widget
    self.createLegendWidget()

    self.actionAdd_new_window.triggered.connect(self.newWindow)
    self.mapArea.subWindowActivated.connect(self.subActive)
    self.actionTile.triggered.connect(self.tileWindows)
    self.actionStart_editing.triggered.connect(self.toogleEditing)
    self.actionStart_editing.setEnabled(False)	
    #self.actionAddWms.triggered.connect(self.addWms)
    
    #create the actions
    self.actionAddLayer = QAction(QIcon(":/icons/grass_add_map.png"), QString("Add Layer"), self)
    self.actionZoomIn = QAction(QIcon(":/icons/zoom-in.png"), QString("Zoom in"), self)
    self.actionZoomOut = QAction(QIcon(":/icons/zoom-out.png"), QString("Zoom out"), self)
    self.actionPan = QAction(QIcon(":/icons/pan.png"), QString("Pan"), self)

    self.actionAddLayer.setCheckable(True)
    self.actionZoomIn.setCheckable(True)
    self.actionZoomOut.setCheckable(True)
    self.actionPan.setCheckable(True)
    
    #This is the new syntax to connect to events (signals) of objects
    self.actionAddLayer.triggered.connect(self.addLayer)
    self.actionZoomIn.triggered.connect(self.zoomIn)
    self.actionZoomOut.triggered.connect(self.zoomOut)
    self.actionPan.triggered.connect(self.pan)
    #self.legend.currentItemChanged(self.enableEditingButton)

    self.toolBar.addAction(self.actionAddLayer)
    self.toolBar.addAction(self.actionZoomIn)
    self.toolBar.addAction(self.actionZoomOut)
    self.toolBar.addAction(self.actionPan)
    self.newWindow()

  def createLegendWidget( self ):
  #Create the map legend widget and associate to the canvas """
      self.legend = Legend( self )
      self.legend.setObjectName( "theMapLegend" )

      self.LegendDock = QDockWidget( "Layers", self )
      self.LegendDock.setObjectName( "legend" )
      self.LegendDock.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )
      self.LegendDock.setWidget( self.legend )
      self.LegendDock.setContentsMargins ( 9, 9, 9, 9 )
      self.addDockWidget( Qt.LeftDockWidgetArea, self.LegendDock )


  
  def tileWindows(self):
    self.mapArea.tileSubWindows()  
   
  def subActive(self, window):
    
    if window is None:
	return
    
    if window.widget() == self.activeCanvas:  
        return

    #Disconnect the last
    if not self.activeCanvas is None:
	self.activeCanvas.extentsChanged.disconnect(self.extentsChanged)
	
    self.activeCanvas = window.widget()
    self.legend.setCanvas(self.activeCanvas)
    self.activeCanvas.extentsChanged.connect(self.extentsChanged)
    
    self.legend.clear()
    for layer in reversed(self.activeCanvas.layers()):
      self.legend.addLayerToLegend(layer)
       	
    if self.activeTool == "ZoomIn":
	self.zoomIn()
    elif self.activeTool == "ZoomOut":
	self.zoomOut()
    elif self.activeTool == "Pan":
	self.pan()
    else:
	return
  
  def extentsChanged(self):
    for window in self.mapArea.subWindowList():
      if not window.widget() == self.activeCanvas:
        extent = self.activeCanvas.extent()
        can = window.widget()
        can.setExtent(extent)
        can.refresh()	
        
     
  def newWindow(self): 
    canvas = MyCanvas()
    canvas.useImageToRender(False)
    self.mapArea.addSubWindow(canvas)
    
    zoomIn = QgsMapToolZoom(canvas, False)
    zoomIn.setAction(self.actionZoomIn)
    canvas.setZoomInTool(zoomIn)
    
    zoomOut = QgsMapToolZoom(canvas, True)
    zoomOut.setAction(self.actionZoomOut)
    canvas.setZoomOutTool(zoomOut)
    
    panTool = QgsMapToolPan(canvas)
    panTool.setAction(self.actionPan)
    canvas.setPanTool(panTool)
    canvas.show()
    self.tileWindows()    

  def zoomIn(self): 
    self.activeCanvas.setMapTool(self.activeCanvas.getZoomInTool())
    self.activeTool = "ZoomIn"

  def zoomOut(self):
    self.activeCanvas.setMapTool(self.activeCanvas.getZoomOutTool())
    self.activeTool = "ZoomOut"

  def pan(self):
    self.activeCanvas.setMapTool(self.activeCanvas.getPanTool())
    self.activeTool = "Pan"

  def addLayer(self):
    # layout is set - open a layer
    # Add an OGR layer to the map
    file = QFileDialog.getOpenFileName(self, 
    			   "Open File", ".", "Shapefile (*.shp);; Raster (*.tif)")
    fileInfo = QFileInfo(file)
    
    # Add the layer
    extn = os.path.splitext(str(file))[1]
    if extn.lower() == '.shp':
        layer = QgsVectorLayer(file, fileInfo.fileName(), "ogr")
    else:
        layer = QgsRasterLayer(file, fileInfo.fileName())

    if not layer.isValid():
      tryagain = QMessageBox.question(self, "APCartOS","Layer failed to load! Try again?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) 
      if tryagain == QMessageBox.Yes:
        self.addLayer()
      else:		
        return

    # Add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer);
    #QgsMapLayerRegistry.instance().layerWasAdded.connect(self.addLayerToLegend)
    
    # Set extent to the extent of our layer
    self.activeCanvas.setExtent(layer.extent())

    # Set up the map canvas layer set
    cl = QgsMapCanvasLayer(layer)
    self.activeCanvas.innerlayers.append(cl)
    self.activeCanvas.setLayerSet(self.activeCanvas.innerlayers)
    self.enableEditingButton()

    # print layers
	
  def enableEditingButton(self):
    layer = self.legend.activeLayer().layer()
    if not layer.isEditable():
      self.actionStart_editing.setEnabled(1)
    elif layer.isEditable():
      self.actionStart_editing.setEnabled(0)
	  

  def toogleEditing(self):
    layer = self.legend.activeLayer().layer()
    if not layer.isEditable():	
      layer.startEditing()
      self.activeCanvas.refresh()
      self.actionStart_editing.setText("Stop editing") 
    else:
      if not layer.isModified():
        layer.commitChanges()
      else:
        reply = QMessageBox.question(self, "APCartOS","Save changes?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            layer.commitChanges()
        else:
            layer.rollBack()      
      self.actionStart_editing.setText("Start editing")

	
	  
class MyCanvas(QgsMapCanvas):
    def __init__(self,parent=None):
	self.innerlayers = []
	QgsMapCanvas.__init__(self,parent)

    def setZoomInTool(self, tool):
	self.zoomInTool = tool
    
    def getZoomInTool(self):
	return self.zoomInTool
    
    def setZoomOutTool(self, tool):
	self.zoomOutTool = tool
    
    def getZoomOutTool(self):
	return self.zoomOutTool
    
    def setPanTool(self,tool):
	self.panTool = tool
	
    def getPanTool(self):
	return self.panTool

def main(argv):
  # create Qt application
  app = QApplication(argv)

  # Initialize qgis libraries
  QgsApplication.setPrefixPath(qgis_prefix, True)
  QgsApplication.initQgis()

  # create main window
  wnd = ShapeViewer()
  # Move the app window to upper left
  wnd.move(100,100)
  wnd.show()

  # run!
  retval = app.exec_()
  
  # exit
  QgsApplication.exitQgis()
  sys.exit(retval)


if __name__ == "__main__":
  main(sys.argv)

