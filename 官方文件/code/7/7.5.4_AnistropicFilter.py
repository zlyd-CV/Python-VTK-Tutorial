# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 15:45:33 2020

@author: Administrator
"""
import vtk
reader = vtk.vtkPNGReader()
reader.SetFileName("../data/CT_head.png")
reader.Update()
#vtkImageAnisotropicDiffusion2D通过迭代方法实现
diffusion=vtk.vtkImageAnisotropicDiffusion2D()
diffusion.SetInputConnection(reader.GetOutputPort())
#用于设置迭代次数
diffusion.SetNumberOfIterations(10)
#定义了一个阙值
diffusion.SetDiffusionThreshold(20)
diffusion.Update()


originalActor=vtk.vtkImageActor()
originalActor.SetInputData(reader.GetOutput())

diffusionActor=vtk.vtkImageActor()
diffusionActor.SetInputData(diffusion.GetOutput())

leftViewport=[0.0, 0.0, 0.5, 1.0]
rightViewport=[0.5, 0.0, 1.0, 1.0]

camera=vtk.vtkCamera()
leftRenderer =vtk.vtkRenderer()
leftRenderer.SetViewport(leftViewport)
leftRenderer.AddActor(originalActor)
leftRenderer.SetBackground(1.0, 1.0, 1.0)
leftRenderer.SetActiveCamera(camera)
leftRenderer.ResetCamera()

rightRenderer =vtk.vtkRenderer()
rightRenderer.SetViewport(rightViewport)
rightRenderer.AddActor(diffusionActor)
rightRenderer.SetBackground(1.0, 1.0, 1.0)
rightRenderer.ResetCamera()


renderWindow=vtk.vtkRenderWindow()
renderWindow.AddRenderer(leftRenderer)
renderWindow.AddRenderer(rightRenderer)
renderWindow.SetSize(640,320)
renderWindow.Render()
renderWindow.SetWindowName("AnistropicFilteringExample")

renderWindowInteractor=vtk.vtkRenderWindowInteractor()
style=vtk.vtkInteractorStyle()
#定义一个vtkInteractorStyle对象 设置交互对象
renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)

renderWindowInteractor.Initialize()
renderWindowInteractor.Start()














