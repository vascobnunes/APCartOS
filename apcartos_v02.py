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
    
    # Required by Qt4 to initialize the UI
    self.setupUi(self)

    # Set the title for the app
    self.setWindowTitle("APCartOS v0.2")
    
    #self.mapArea.setViewMode(QMdiArea.TabbedView)
	
    # Create the legend widget
    self.createLegendWidget()

    self.actionOpen.triggered.connect(self.newWindow)
    self.mdiArea.subWindowActivated.connect(self.subActive)
    
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
    
  def createLegendWidget( self ):
  #Create the map legend widget and associate to the canvas """
    self.legend = Legend( self )
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
    self.legend.setCanvas(self.activeCanvas)
    
    self.toolPan = QgsMapToolPan(window.widget())
    if self.toolPan.action() is None:
	self.toolPan.setAction(self.actionPan)
    
    self.toolZoomIn = QgsMapToolZoom(window.widget(), False) # false = in
    if self.toolZoomIn.action() is None:
	self.toolZoomIn.setAction(self.actionZoomIn)
    
    self.toolZoomOut = QgsMapToolZoom(window.widget(), True) # true = out
    if self.toolZoomOut.action() is None:
        self.toolZoomOut.setAction(self.actionZoomOut)
    
  def newWindow(self): 
    canvas = QgsMapCanvas()
    canvas.useImageToRender(False)
    self.mdiArea.addSubWindow(canvas)
    canvas.show()    

  def zoomIn(self):
    self.activeCanvas.setMapTool(self.toolZoomIn)

  def zoomOut(self):
    self.activeCanvas.setMapTool(self.toolZoomOut)

  def pan(self):
    self.activeCanvas.setMapTool(self.toolPan)
	
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

    # Change the color of the layer to gray
    #symbols = layer.renderer().symbols()
    #ymbol = symbols[0]
    #ymbol.setFillColor(QColor.fromRgb(192,192,192))
    
    # Add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer);

    # Set extent to the extent of our layer
    self.activeCanvas.setExtent(layer.extent())

    # Set up the map canvas layer set
    cl = QgsMapCanvasLayer(layer)
    layers = [cl]
    self.activeCanvas.setLayerSet(layers)
	
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