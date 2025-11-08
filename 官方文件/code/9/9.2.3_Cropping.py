#!/usr/bin/env python

import vtk


def main():
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName("../data/mummy.128.vtk")

    # Create transfer mapping scalar value to opacity.
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(90, 0.0)
    #opacityTransferFunction.AddPoint(150, 0.5)
    opacityTransferFunction.AddPoint(200, 1.0)

    # Create transfer mapping scalar value to gradient opacity.
    GradientopacityTransferFunction = vtk.vtkPiecewiseFunction()
    GradientopacityTransferFunction.AddPoint(10, 0.0)
    #GradientopacityTransferFunction.AddPoint(90, 0.5)
    GradientopacityTransferFunction.AddPoint(100, 1.0)

    # Create transfer mapping scalar value to color.
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.52, 0.30)
    #colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
    colorTransferFunction.AddRGBPoint(190.0, 1.0, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(220.0, 0.2, 0.2, 0.2)

    # The property describes how the data will look.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetGradientOpacity(GradientopacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    # The mapper / ray cast function know how to render the data.
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    #cropping
    volumeMapper.SetCropping(1)
    volumeMapper.SetCroppingRegionPlanes(100,400, 100,400, 0,400)
    volumeMapper.SetCroppingRegionFlags(0x0002000)

    # The volume holds the mapper and the property and
    # can be used to position/orient the volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    ren1 = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren1.AddVolume(volume)
    ren1.SetBackground(0.8,0.8,0.7)
    ren1.GetActiveCamera().Azimuth(45)
    ren1.GetActiveCamera().Elevation(30)
    ren1.ResetCameraClippingRange()
    ren1.ResetCamera()
    renWin.SetWindowName("Cropping")
    renWin.SetSize(600, 600)
    renWin.Render()

    iren.Start()


if __name__ == '__main__':
    main()
