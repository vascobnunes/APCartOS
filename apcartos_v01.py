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
    
    self.activeTool = None
    # Required by Qt4 to initialize the UI
    self.setupUi(self)

    # Set the title for the app
    self.setWindowTitle("APCartOS v0.1")
    
    #self.mapArea.setViewMode(QMdiArea.TabbedView)
    ## Create the legend widget
    self.createLegendWidget()

    self.actionOpen.triggered.connect(self.newWindow)
    self.mapArea.subWindowActivated.connect(self.subActive)
    self.actionTile.triggered.connect(self.tileWindows)
    
    #create the actions
    self.actionAddLayer = QAction(QIcon(":/icons/grass_add_map.png"), QString("Add Layer"), self)
    self.actionZoomIn = QAction(QIcon(":/icons/zoom-in.png"), QString("Zoom in"), self)
    self.actionZoomOut = QAction(QIcon(":/icons/zoom-out.png"), "Zoom out", self)
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

    self.toolBar.addAction(self.actionAddLayer)
    self.toolBar.addAction(self.actionZoomIn)
    self.toolBar.addAction(self.actionZoomOut)
    self.toolBar.addAction(self.actionPan)

  def tileWindows(self):
    self.mapArea.tileSubWindows()
    
  def createLegendWidget( self ):
  #Create the map legend widget and associate to the canvas """
    self.legend = Legend ( self )
    #self.legend.setCanvas( self.canvas )
    self.legend.setObjectName( "theMapLegend" )

    self.LegendDock = QDockWidget( "Layers", self )
    self.LegendDock.setObjectName( "legend" )
    self.LegendDock.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )
    self.LegendDock.setWidget( self.legend )
    self.LegendDock.setContentsMargins ( 9, 9, 9, 9 )
    self.addDockWidget( Qt.LeftDockWidgetArea, self.LegendDock )
    
    
  def subActive(self, window):
    
    if window is None:
	return
    
    self.activeCanvas = window.widget()
    self.legend.setMapCanvas( self.activeCanvas )
    #self.legend.updateLayerSet()
    
    if self.activeTool == "ZoomIn":
	self.zoomIn()
    elif self.activeTool == "ZoomOut":
	self.zoomOut()
    elif self.activeTool == "Pan":
	self.span()
    else:
	return
    
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
      return

    
    # Add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer);
    
    # self.layermap=QgsMapLayerRegistry.instance().mapLayers()
    # for (name,layer) in self.layermap.iteritems():
        # QMessageBox.information(self.frame,"debug",str(name))

    # Set extent to the extent of our layer
    self.activeCanvas.setExtent(layer.extent())

    # Set up the map canvas layer set
    cl = QgsMapCanvasLayer(layer)
    layers = [cl]
    self.activeCanvas.setLayerSet(layers)
    print l
    
class MyCanvas(QgsMapCanvas):
    def __init__(self,parent=None):
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

