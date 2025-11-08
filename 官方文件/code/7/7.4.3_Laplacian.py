import vtk


def main():
    reader = vtk.vtkPNGReader()
    reader.SetFileName ("../data/PET.png")
    reader.Update()

    lapFilter = vtk.vtkImageLaplacian()
    lapFilter.SetInputConnection(reader.GetOutputPort())
    lapFilter.SetDimensionality(2)
    lapFilter.Update()

    myRange = lapFilter.GetOutput().GetScalarRange()
    print(myRange)

    ShiftScale = vtk.vtkImageShiftScale()
    ShiftScale.SetOutputScalarTypeToUnsignedChar()
    ShiftScale.SetScale( 255 / (myRange[1]-myRange[0]) )
    ShiftScale.SetShift(245)
    ShiftScale.SetInputConnection(lapFilter.GetOutputPort())
    ShiftScale.Update()

    originalActor = vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())
    originalActor.Update()

    gradActor = vtk.vtkImageActor()
    gradActor.SetInputData(ShiftScale.GetOutput())

    originalViewport = (0.0, 0.0, 0.5, 1.0)
    gradviewport = (0.5, 0.0, 1.0, 1.0)

    originalRenderer = vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    gradRenderer = vtk.vtkRenderer()
    gradRenderer.SetViewport(gradviewport)
    gradRenderer.AddActor(gradActor)
    gradRenderer.ResetCamera()
    gradRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(gradRenderer)
    renderWindow.SetSize(1024, 512)
    renderWindow.Render()
    renderWindow.SetWindowName("LaplacianExample")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
