import vtk

def main():

    reader  = vtk.vtkDICOMImageReader()
    reader.SetFileName("../data/CT_head.dcm")

    colorTable =vtk.vtkLookupTable()
    colorTable.SetRange( 0.0, 255 )
    colorTable.SetHueRange( 0.1, 0.5 )
    colorTable.SetValueRange( 0.6, 1.0 )
    colorTable.Build()

    colorMap = vtk.vtkImageMapToColors()
    colorMap.SetInputConnection( reader.GetOutputPort() )
    colorMap.SetLookupTable( colorTable )
    colorMap.Update()

    originalActor =vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    shiftscaleActor = vtk.vtkImageActor()
    shiftscaleActor.SetInputData(colorMap.GetOutput())

    originalViewport = (0.0, 0.0, 0.5, 1.0)
    shiftscaleViewport = (0.5, 0.0, 1.0, 1.0)

    originalRenderer = vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    shiftscaleRenderer = vtk.vtkRenderer()
    shiftscaleRenderer.SetViewport(shiftscaleViewport)
    shiftscaleRenderer.AddActor(shiftscaleActor)
    shiftscaleRenderer.ResetCamera()
    shiftscaleRenderer.SetBackground(1.0, 1.0, 0.8)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer);
    renderWindow.AddRenderer(shiftscaleRenderer);
    renderWindow.SetSize(900, 300);
    renderWindow.Render();
    renderWindow.SetWindowName("Gray2ColorImage");

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
