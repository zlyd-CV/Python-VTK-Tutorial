import vtk

def main():
    red = vtk.vtkImageCanvasSource2D()
    red.SetScalarTypeToUnsignedChar()
    red.SetNumberOfScalarComponents(1)
    red.SetExtent(0, 100, 0, 100, 0, 0)
    red.SetDrawColor(0, 0, 0, 0)
    red.FillBox(0,100,0,100)
    red.SetDrawColor(255, 0, 0, 0)
    red.FillBox(20,40,20,40)
    red.Update()

    green = vtk.vtkImageCanvasSource2D()
    green.SetScalarTypeToUnsignedChar()
    green.SetNumberOfScalarComponents(1)
    green.SetExtent(0, 100, 0, 100, 0, 0)
    green.SetDrawColor(0, 0, 0, 0)
    green.FillBox(0,100,0,100)
    green.SetDrawColor(255, 0, 0, 0)
    green.FillBox(30,50,30,50)
    green.Update()

    blue = vtk.vtkImageCanvasSource2D()
    blue.SetScalarTypeToUnsignedChar()
    blue.SetNumberOfScalarComponents(1)
    blue.SetExtent(0, 100, 0, 100, 0, 0)
    blue.SetDrawColor(0, 0, 0, 0)
    blue.FillBox(0,100,0,100)
    blue.SetDrawColor(255, 0, 0, 0)
    blue.FillBox(40,60,40,60)
    blue.Update()

    appendFilter = vtk.vtkImageAppendComponents()
    appendFilter.SetInputConnection(0, red.GetOutputPort())
    appendFilter.AddInputConnection(0, green.GetOutputPort())
    appendFilter.AddInputConnection(0, blue.GetOutputPort())
    appendFilter.Update()

    redActor = vtk.vtkImageActor()
    redActor.SetInputData(red.GetOutput())

    greenActor = vtk.vtkImageActor()
    greenActor.SetInputData(green.GetOutput())

    blueActor = vtk.vtkImageActor()
    blueActor.SetInputData(blue.GetOutput())

    combinedActor = vtk.vtkImageActor()
    combinedActor.SetInputData(appendFilter.GetOutput())

    # Define viewport ranges
    # (xmin, ymin, xmax, ymax)
    redViewport = (0.0, 0.0, 0.25, 1.0)
    greenViewport = (0.25, 0.0, 0.5, 1.0)
    blueViewport = (0.5, 0.0, 0.75, 1.0)
    combinedViewport = (0.75, 0.0, 1.0, 1.0)

    # Setup renderers
    redRenderer =vtk.vtkRenderer()
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

    combinedRenderer = vtk.vtkRenderer()
    combinedRenderer.SetViewport(combinedViewport)
    combinedRenderer.AddActor(combinedActor)
    combinedRenderer.ResetCamera()
    combinedRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(redRenderer)
    renderWindow.AddRenderer(greenRenderer)
    renderWindow.AddRenderer(blueRenderer)
    renderWindow.AddRenderer(combinedRenderer)
    renderWindow.SetSize(1200, 300)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageAppendComponents")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()