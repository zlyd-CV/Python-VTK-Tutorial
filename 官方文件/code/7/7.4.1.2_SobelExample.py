import vtk


def main():
    reader = vtk.vtkPNGReader()
    reader.SetFileName("../data/CT_head.png")
    reader.Update()
    sobelFilter = vtk.vtkImageSobel2D()
    sobelFilter.SetInputConnection(reader.GetOutputPort())

    extractXFilter = vtk.vtkImageExtractComponents()
    extractXFilter.SetComponents(0)
    extractXFilter.SetInputConnection(sobelFilter.GetOutputPort())
    extractXFilter.Update()

    xRange = extractXFilter.GetOutput().GetScalarRange()

    xImageAbs = vtk.vtkImageMathematics()
    xImageAbs.SetOperationToAbsoluteValue()
    xImageAbs.SetInputConnection(extractXFilter.GetOutputPort())
    xImageAbs.Update()

    xShiftScale = vtk.vtkImageShiftScale()
    xShiftScale.SetOutputScalarTypeToUnsignedChar()
    xShiftScale.SetScale( 255 / xRange[1] )
    xShiftScale.SetInputConnection(xImageAbs.GetOutputPort())
    xShiftScale.Update()

    extractYFilter = vtk.vtkImageExtractComponents()
    extractYFilter.SetComponents(1)
    extractYFilter.SetInputConnection(sobelFilter.GetOutputPort())
    extractYFilter.Update()

    yRange = extractYFilter.GetOutput().GetScalarRange()

    yImageAbs = vtk.vtkImageMathematics()
    yImageAbs.SetOperationToAbsoluteValue()
    yImageAbs.SetInputConnection(extractYFilter.GetOutputPort())
    yImageAbs.Update()

    yShiftScale = vtk.vtkImageShiftScale()
    yShiftScale.SetOutputScalarTypeToUnsignedChar()
    yShiftScale.SetScale( 255 / yRange[1] )
    yShiftScale.SetInputConnection(yImageAbs.GetOutputPort())
    yShiftScale.Update()

    originalActor = vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    xActor = vtk.vtkImageActor()
    xActor.SetInputData(xShiftScale.GetOutput())

    yActor = vtk.vtkImageActor()
    yActor.SetInputData(yShiftScale.GetOutput())

    originalViewport = (0.0, 0.0, 0.33, 1.0)
    xViewport = (0.33, 0.0, 0.66, 1.0)
    yViewport = (0.66, 0.0, 1.0, 1.0)

    originalRenderer = vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    xRenderer = vtk.vtkRenderer()
    xRenderer.SetViewport(xViewport)
    xRenderer.AddActor(xActor)
    xRenderer.ResetCamera()
    xRenderer.SetBackground(1.0, 1.0, 1.0)

    yRenderer = vtk.vtkRenderer()
    yRenderer.SetViewport(yViewport)
    yRenderer.AddActor(yActor)
    yRenderer.ResetCamera()
    yRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1200, 300)
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(xRenderer)
    renderWindow.AddRenderer(yRenderer)
    renderWindow.Render()
    renderWindow.SetWindowName("SobelExample")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()

