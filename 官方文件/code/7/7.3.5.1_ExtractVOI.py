import vtk

def main():

    reader  = vtk.vtkDICOMImageReader()
    reader.SetFileName("../data/CT_head.dcm")
    reader.Update()

    dims = []
    dims = reader.GetOutput().GetDimensions()
    print(dims[0]/4)

    extractVOI = vtk.vtkExtractVOI()
    extractVOI.SetInputConnection(reader.GetOutputPort())
    extractVOI.SetVOI(int(dims[0]/4),int(3*dims[0]/4),int(dims[1]/4),int(3*dims[1]/4), 0, 0)
    extractVOI.Update()

    originalActor =vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    voiActor = vtk.vtkImageActor()
    voiActor.SetInputData(extractVOI.GetOutput())

    originalViewport = (0.0, 0.0, 0.5, 1.0)
    voiviewport = (0.5, 0.0, 1.0, 1.0)

    originalRenderer = vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    shiftscaleRenderer = vtk.vtkRenderer()
    shiftscaleRenderer.SetViewport(voiviewport)
    shiftscaleRenderer.AddActor(voiActor)
    shiftscaleRenderer.ResetCamera()
    shiftscaleRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(shiftscaleRenderer)
    renderWindow.SetSize(900, 300)
    renderWindow.Render()
    renderWindow.SetWindowName("ExtractVOI")


    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()
if __name__ == "__main__":
    main()