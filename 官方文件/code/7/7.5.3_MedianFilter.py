import vtk

def main():
    reader=vtk.vtkPNGReader()
    reader.SetFileName("../data/PET.png")
    reader.Update()

    hybridMedian=vtk.vtkImageHybridMedian2D()
    hybridMedian.SetInputData(reader.GetOutput())
    hybridMedian.Update()

    originalActor=vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    hybridMedianActor=vtk.vtkImageActor()
    hybridMedianActor.SetInputData(hybridMedian.GetOutput())

    originalViewport= [0.0, 0.0, 0.5, 1.0]
    hybridMedianViewport= [0.5, 0.0, 1.0, 1.0]

    originalRenderer=vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    hybridMedianRenderer=vtk.vtkRenderer()
    hybridMedianRenderer.SetViewport(hybridMedianViewport)
    hybridMedianRenderer.AddActor(hybridMedianActor)
    hybridMedianRenderer.ResetCamera()
    hybridMedianRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(hybridMedianRenderer)
    renderWindow.SetSize(640,320)
    renderWindow.Render()
    renderWindow.SetWindowName("MedianFilter")

    renderWindowInteractor=vtk.vtkRenderWindowInteractor()
    style=vtk.vtkInteractorStyle()
    #定义一个vtkInteractorStyle对象 设置交互对象
    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()

