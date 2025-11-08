#!/usr/bin/env python


import vtk


def main():

    # Read the CT data of the human head.
    reader = vtk.vtkPNGReader()
    reader.SetFileName("../data/CT_head.png")
    reader.Update()

    il = vtk.vtkImageLuminance()
    il.SetInputConnection(reader.GetOutputPort())
    il.Update()

    ic =vtk.vtkImageCast()
    ic.SetOutputScalarTypeToFloat()
    ic.SetInputConnection(il.GetOutputPort())
    ic.Update()

    gradientFilter = vtk.vtkImageGradient()
    gradientFilter.SetInputConnection(ic.GetOutputPort())
    gradientFilter.SetDimensionality(2);
    gradientFilter.Update()

    # Magnify the image.
    magnitudeFilter = vtk.vtkImageMagnitude()
    magnitudeFilter.SetInputConnection(gradientFilter.GetOutputPort())
    magnitudeFilter.Update()

    myrange= magnitudeFilter.GetOutput().GetScalarRange()
    print(myrange)

    ShiftScale = vtk.vtkImageShiftScale()
    ShiftScale.SetOutputScalarTypeToUnsignedChar()
    ShiftScale.SetScale(255 / myrange[1])
    ShiftScale.SetInputConnection(magnitudeFilter.GetOutputPort())
    ShiftScale.Update()

    originalActor = vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    gradActor = vtk.vtkImageActor()
    gradActor.SetInputData(ShiftScale.GetOutput())

    originalViewport = (0.0, 0.0, 0.5, 1.0)
    gradviewport = (0.5, 0.0, 1.0, 1.0)

    originalRenderer =vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor);
    originalRenderer.ResetCamera();
    originalRenderer.SetBackground(1.0, 1.0, 1.0);

    gradRenderer = vtk.vtkRenderer();
    gradRenderer.SetViewport(gradviewport);
    gradRenderer.AddActor(gradActor);
    gradRenderer.ResetCamera();
    gradRenderer.SetBackground(1.0, 1.0, 1.0);

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(gradRenderer)
    renderWindow.SetSize( 640, 320 )
    renderWindow.Render()
    renderWindow.SetWindowName("ImageGradientExample")

    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    style =vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()
