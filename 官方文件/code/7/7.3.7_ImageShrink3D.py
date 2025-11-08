import vtk

def main():
    reader  = vtk.vtkDICOMImageReader()
    reader.SetFileName("../data/CT_head.dcm")
    reader.Update()

    shrinkFilter =vtk.vtkImageShrink3D()
    shrinkFilter.SetInputConnection(reader.GetOutputPort())
    shrinkFilter.SetShrinkFactors(20,20,1)
    shrinkFilter.Update()

    originalDims = []
    originalDims.append(reader.GetOutput().GetDimensions())
    originalSpace = []
    originalSpace.append(reader.GetOutput().GetSpacing())
    shrinkDims = [];
    shrinkDims.append(shrinkFilter.GetOutput().GetDimensions())
    shrinkSpace = []
    shrinkSpace.append(shrinkFilter.GetOutput().GetSpacing())
    print(originalDims)
    print(originalSpace)
    print(shrinkDims)
    print(shrinkSpace)


    originalActor =vtk.vtkImageActor()
    originalActor.SetInputData( reader.GetOutput())

    shrinkActor = vtk.vtkImageActor()
    shrinkActor.SetInputData(shrinkFilter.GetOutput())

    originalViewport = [0.0, 0.0, 0.5, 1.0]
    shrinkViewport= [0.5, 0.0, 1.0, 1.0]

    originalRenderer =vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    shrinkRenderer =vtk.vtkRenderer()
    shrinkRenderer.SetViewport(shrinkViewport)
    shrinkRenderer.AddActor(shrinkActor)
    shrinkRenderer.ResetCamera()
    shrinkRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(shrinkRenderer)
    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageShrink3D")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()