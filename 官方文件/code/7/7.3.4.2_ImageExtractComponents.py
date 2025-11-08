import vtk

def main():
    reader = vtk.vtkPNGReader()
    reader.SetFileName ("../data/CT.png")
    reader.Update()

    extractRed =vtk.vtkImageExtractComponents()
    extractRed.SetInputConnection(reader.GetOutputPort())
    extractRed.SetComponents(0)
    extractRed.Update()

    extractGreen = vtk.vtkImageExtractComponents()
    extractGreen.SetInputConnection(reader.GetOutputPort())
    extractGreen.SetComponents(1)
    extractGreen.Update()

    extractBlue = vtk.vtkImageExtractComponents()
    extractBlue.SetInputConnection(reader.GetOutputPort())
    extractBlue.SetComponents(2)
    extractBlue.Update()

    # Create actors
    inputActor = vtk.vtkImageActor()
    inputActor.SetInputData(reader.GetOutput())

    redActor =vtk.vtkImageActor()
    redActor.SetInputData(extractRed.GetOutput())

    greenActor =vtk.vtkImageActor()
    greenActor.SetInputData(extractGreen.GetOutput())

    blueActor = vtk.vtkImageActor()
    blueActor.SetInputData(extractBlue.GetOutput())

    inputViewport = (0.0, 0.0, 0.25, 1.0)
    redViewport = (0.25, 0.0, 0.5, 1.0)
    greenViewport = (0.5, 0.0, 0.75, 1.0)
    blueViewport = (0.75, 0.0, 1.0, 1.0)

    inputRenderer = vtk.vtkRenderer()
    inputRenderer.SetViewport(inputViewport)
    inputRenderer.AddActor(inputActor)
    inputRenderer.ResetCamera()
    inputRenderer.SetBackground(1.0, 1.0, 1.0)

    redRenderer = vtk.vtkRenderer()
    redRenderer.SetViewport(redViewport)
    redRenderer.AddActor(redActor)
    redRenderer.ResetCamera()
    redRenderer.SetBackground(1.0, 1.0, 1.0)

    greenRenderer = vtk.vtkRenderer()
    greenRenderer.SetViewport(greenViewport)
    greenRenderer.AddActor(greenActor)
    greenRenderer.ResetCamera()
    greenRenderer.SetBackground(1.0, 1.0, 1.0)

    blueRenderer = vtk.vtkRenderer()
    blueRenderer.SetViewport(blueViewport)
    blueRenderer.AddActor(blueActor)
    blueRenderer.ResetCamera()
    blueRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(inputRenderer)
    renderWindow.AddRenderer(redRenderer)
    renderWindow.AddRenderer(greenRenderer)
    renderWindow.AddRenderer(blueRenderer)

    renderWindow.SetSize(1200, 300)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageExtractComponents")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()