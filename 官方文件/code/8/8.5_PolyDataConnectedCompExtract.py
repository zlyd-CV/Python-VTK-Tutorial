# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:35:39 2020

@author: Administrator
"""
import vtk
sphereSource=vtk.vtkSphereSource()
sphereSource.SetRadius(10)
sphereSource.SetThetaResolution(10)
sphereSource.SetPhiResolution(10)
sphereSource.Update()

coneSource=vtk.vtkConeSource()
coneSource.SetRadius(5)
coneSource.SetHeight(10)
coneSource.SetCenter(25,0,0)
coneSource.Update()

appendFilter=vtk.vtkAppendPolyData()
appendFilter.AddInputData(sphereSource.GetOutput())
appendFilter.AddInputData(coneSource.GetOutput())
appendFilter.Update()

connectivityFilter =vtk.vtkPolyDataConnectivityFilter()
connectivityFilter.SetInputConnection(appendFilter.GetOutputPort())
connectivityFilter.SetExtractionModeToCellSeededRegions()
connectivityFilter.AddSeed(100)
#connectivityFilter.SetExtractionModeToAllRegions()
#connectivityFilter.ColorRegionsOn()
connectivityFilter.Update()

originalMapper=vtk.vtkPolyDataMapper()
originalMapper.SetInputConnection(appendFilter.GetOutputPort())
originalMapper.Update()

originalActor=vtk.vtkActor()
originalActor.SetMapper(originalMapper)

extractedMapper=vtk.vtkPolyDataMapper()
extractedMapper.SetInputConnection(connectivityFilter.GetOutputPort())
extractedMapper.Update()

extractedActor=vtk.vtkActor()
extractedActor.SetMapper(extractedMapper)

leftViewport= [0.0, 0.0, 0.5, 1.0]
rightViewport= [0.5, 0.0, 1.0, 1.0]

leftRenderer=vtk.vtkRenderer()
leftRenderer.SetViewport(leftViewport)
leftRenderer.AddActor(originalActor)
leftRenderer.SetBackground(0.8, 0.8, 0.8)

rightRenderer=vtk.vtkRenderer()
rightRenderer.SetViewport(rightViewport)
rightRenderer.AddActor(extractedActor)
rightRenderer.SetBackground(1.0, 1.0, 1.0)

renderWindow=vtk.vtkRenderWindow()
renderWindow.AddRenderer(rightRenderer)
renderWindow.AddRenderer(leftRenderer)
renderWindow.SetSize(640, 320)
renderWindow.Render()
renderWindow.SetWindowName("PolyDataConnectedCompExtract")

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)
iren.Initialize()
iren.Start()











