# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:38:17 2020

@author: a
"""


import vtk

points=vtk.vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(2.0, 0.0, 0.0)

polygon=vtk.vtkPolygon()
polygon.GetPointIds().SetNumberOfIds(4)
polygon.GetPointIds().SetId(0, 0)
polygon.GetPointIds().SetId(1, 1)
polygon.GetPointIds().SetId(2,2)
polygon.GetPointIds().SetId(3,3)

trianle=vtk.vtkTriangle()
trianle.GetPointIds().SetId(0, 1)
trianle.GetPointIds().SetId(1, 2)
trianle.GetPointIds().SetId(2, 4)

cells=vtk.vtkCellArray()
cells.InsertNextCell(polygon)
cells.InsertNextCell(trianle)

polygonPolyData = vtk.vtkPolyData()
polygonPolyData.SetPoints(points)
polygonPolyData.SetPolys(cells)

red=[255,0,0]
green=[0,255,0]
blue=[0,0,255]
pointColors = vtk.vtkUnsignedCharArray()
pointColors.SetNumberOfComponents(3)
pointColors.InsertNextTuple(red)
pointColors.InsertNextTuple(green)
pointColors.InsertNextTuple(blue)
pointColors.InsertNextTuple(green)
pointColors.InsertNextTuple(red)
#polygonPolyData.GetPointData().SetScalars(pointColors)

cellColors = vtk.vtkUnsignedCharArray()
cellColors.SetNumberOfComponents(3)
cellColors.InsertNextTuple(red)
cellColors.InsertNextTuple(green)
polygonPolyData.GetCellData().SetScalars(cellColors)

pointfield = vtk.vtkIntArray()
pointfield.SetName("Field")
pointfield.SetNumberOfComponents(3)
pointfield.InsertNextTuple3(1,0,0)
pointfield.InsertNextTuple3(2,0,0)
pointfield.InsertNextTuple3(3,0,0)
pointfield.InsertNextTuple3(4,0,0)
pointfield.InsertNextTuple3(5,0,0)
polygonPolyData.GetPointData().AddArray(pointfield)

lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(10)
lut.Build()
lut.SetTableValue(0     , 0     , 0     , 0, 1)
lut.SetTableValue(1, 0.8900, 0.8100, 0.3400, 1)
lut.SetTableValue(2, 1.0000, 0.3882, 0.2784, 1)
lut.SetTableValue(3, 0.9608, 0.8706, 0.7020, 1)
lut.SetTableValue(4, 0.9020, 0.9020, 0.9804, 1)
lut.SetTableValue(5, 1.0000, 0.4900, 0.2500, 1)
lut.SetTableValue(6, 0.5300, 0.1500, 0.3400, 1)
lut.SetTableValue(7, 0.9804, 0.5020, 0.4471, 1)
lut.SetTableValue(8, 0.7400, 0.9900, 0.7900, 1)
lut.SetTableValue(9, 0.2000, 0.6300, 0.7900, 1)

mapper=vtk.vtkPolyDataMapper()
mapper.SetInputData(polygonPolyData)
mapper.SetLookupTable(lut)



actor=vtk.vtkActor()
actor.SetMapper(mapper)

renderer=vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize( 640, 480 )
renderWindow.Render()
renderWindow.SetWindowName("PolyDataColor")

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)

iren.Initialize()
iren.Start()




















