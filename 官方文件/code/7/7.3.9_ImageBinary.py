import vtk

def main():
    reader  = vtk.vtkDICOMImageReader()
    reader.SetFileName("../data/CT_head.dcm")
    reader.Update()

    thresholdFilter = vtk.vtkImageThreshold()
    thresholdFilter.SetInputConnection(reader.GetOutputPort())
    thresholdFilter.ThresholdByUpper(100)
    thresholdFilter.SetInValue(255)
    thresholdFilter.SetOutValue(0)
    thresholdFilter.Update()     #有时此处与C++不同

    originalActor = vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    binaryActor = vtk.vtkImageActor()
    binaryActor.SetInputData(thresholdFilter.GetOutput())

    originalViewport = [0.0, 0.0, 0.5, 1.0]
    binaryViewport = [0.5, 0.0, 1.0, 1.0]

    originalRenderer = vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    binaryRenderer = vtk.vtkRenderer()
    binaryRenderer.SetViewport(binaryViewport)
    binaryRenderer.AddActor(binaryActor)
    binaryRenderer.ResetCamera()
    binaryRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(binaryRenderer)
    renderWindow.SetSize(640, 320)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageBinary")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()