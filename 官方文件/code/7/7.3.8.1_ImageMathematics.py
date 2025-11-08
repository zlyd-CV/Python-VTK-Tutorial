import vtk

def main():
    imageSource=vtk.vtkImageCanvasSource2D()
    imageSource.SetNumberOfScalarComponents(3)
    imageSource.SetExtent(0,4,0,4,0,0)
    imageSource.SetDrawColor(50.0,0,0)
    imageSource.FillBox(0, 4, 0, 4)
    imageSource.Update()

    imageMath =vtk.vtkImageMathematics()
    imageMath.SetOperationToMultiplyByK()
    imageMath.SetConstantK(4)
    imageMath.SetInputConnection(imageSource.GetOutputPort())
    imageMath.Update()

    originalActor=vtk.vtkImageActor()
    originalActor.SetInputData(imageSource.GetOutput())

    mathActor=vtk.vtkImageActor()
    mathActor.SetInputData(imageMath.GetOutput())

    leftViewport=[0.0, 0.0, 0.5, 1.0]
    rightViewport=[0.5, 0.0, 1.0, 1.0]

    originalRenderer =vtk.vtkRenderer()
    originalRenderer.SetViewport(leftViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    gradientMagnitudeRenderer=vtk.vtkRenderer()
    gradientMagnitudeRenderer.SetViewport(rightViewport)
    gradientMagnitudeRenderer.AddActor(mathActor)
    gradientMagnitudeRenderer.ResetCamera()
    gradientMagnitudeRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(gradientMagnitudeRenderer)
    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageMathematics")

    renderWindowInteractor=vtk.vtkRenderWindowInteractor()
    style=vtk.vtkInteractorStyle()
    #定义一个vtkInteractorStyle对象 设置交互对象
    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()






