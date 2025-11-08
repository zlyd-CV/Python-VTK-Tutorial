# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:44:16 2021

@author: HP
"""

import vtk

def main():
    canvas = vtk.vtkImageCanvasSource2D()
    canvas.SetScalarTypeToUnsignedChar()
    #canvas.SeNumberOfScalarComponents(1)
    canvas.SetExtent(0,100,0,100,0,0)
    canvas.SetDrawColor(0,0,0,0)
    canvas.FillBox(0,100,0,100)

    canvas.SetDrawColor(255,0,0,0)
    canvas.FillBox(10,60,10,60)
    canvas.Update()

    image_data = canvas.GetOutput()
    actor = vtk.vtkImageActor()
    actor.SetInputData(image_data)

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(500,500)
    renWin.AddRenderer(ren)

    renWin.Render()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()

if __name__ == '__main__':
    main()