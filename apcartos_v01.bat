@echo off
set OSGEO4W_ROOT=C:\OSGeo4W
PATH=%OSGEO4W_ROOT%\bin;%PATH%
set PATH=C:\OSGeo4W\apps\qgis\bin;%PATH%
set PYTHONPATH=C:\OSGeo4W\apps\qgis\python
Set PATH=C:\OSGeo4W\apps\qgis\plugins;%PATH%
set QGISHOME=C:\OSGeo4W\apps\qgis

for %%f in (%OSGEO4W_ROOT%\etc\ini\*.bat) do call %%f

@echo on

python apcartos_v01.py

REM python C:\Documents and Settings\dsigigDSIGIG\My Documents\Downloads\tutorials\4_adding_rasters_to_canvas\mainwindow.py


