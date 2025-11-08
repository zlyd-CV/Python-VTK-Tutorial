# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 11:28:15 2021

@author: HP
"""

import vtk

def main():

    reader = vtk.vtkBMPReader()
    reader.SetFileName('../data/vtk.bmp')

    imageviewer = vtk.vtkImageViewer2()
    imageviewer.SetInputConnection(reader.GetOutputPort())
    iren = vtk.vtkRenderWindowInteractor()
    imageviewer.SetupInteractor(iren)
    imageviewer.SetSize(500,500)

    imageviewer.GetRenderer().ResetCamera()
    imageviewer.GetRenderWindow().SetWindowName("ReadSingleImage")

    imageviewer.Render()
    iren.Start()

if __name__ == "__main__":
    main()