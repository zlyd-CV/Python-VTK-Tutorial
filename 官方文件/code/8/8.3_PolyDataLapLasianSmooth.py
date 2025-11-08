# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:08:49 2020

@author: Administrator
"""
import vtk
reader=vtk.vtkPolyDataReader()
reader.SetFileName("../data/fran_cut.vtk")
reader.Update()

smoothFilter=vtk.vtkSmoothPolyDataFilter()
smoothFilter.SetInputConnection(reader.GetOutputPort())
smoothFilter.SetNumberOfIterations(200)
smoothFilter.Update()

inputMapper=vtk.vtkPolyDataMapper()
inputMapper.SetInputConnection(reader.GetOutputPort())

inputActor=vtk.vtkActor()
inputActor.SetMapper(inputMapper)

smoothedMapper=vtk.vtkPolyDataMapper()
smoothedMapper.SetInputConnection(smoothFilter.GetOutputPort())

smoothedActor=vtk.vtkActor()
smoothedActor.SetMapper(smoothedMapper)
#两个窗口
leftViewport= [0.0, 0.0, 0.5, 1.0]
rightViewport= [0.5, 0.0, 1.0, 1.0]

leftRenderer=vtk.vtkRenderer()
leftRenderer.SetViewport(leftViewport)
leftRenderer.AddActor(inputActor)
leftRenderer.SetBackground(0.8, 0.8, 0.8)
leftRenderer.ResetCamera()

rightRenderer=vtk.vtkRenderer()
rightRenderer.SetViewport(rightViewport)
rightRenderer.AddActor(smoothedActor)
rightRenderer.SetBackground(0.8, 0.8, 0.8)
rightRenderer.SetActiveCamera(leftRenderer.GetActiveCamera())
rightRenderer.ResetCamera()

renderWindow=vtk.vtkRenderWindow()
renderWindow.AddRenderer(rightRenderer)
renderWindow.AddRenderer(leftRenderer)
renderWindow.SetSize(640, 320)
renderWindow.Render()
renderWindow.SetWindowName("PolyDataLapLasianSmooth")

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)
iren.Initialize()
iren.Start()






