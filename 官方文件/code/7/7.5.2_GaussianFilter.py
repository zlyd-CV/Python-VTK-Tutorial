import vtk

def main():
    reader=vtk.vtkPNGReader()
    reader.SetFileName("../data/PET.png")
    reader.Update()
    
    gaussianSmoothFilter =vtk.vtkImageGaussianSmooth()
    gaussianSmoothFilter.SetInputConnection(reader.GetOutputPort())
    gaussianSmoothFilter.SetDimensionality(2)          #根据设置相应的维数 
    gaussianSmoothFilter.SetRadiusFactor(5)            #用于设置高斯模板的大小，当超过范围，系数取0
    gaussianSmoothFilter.SetStandardDeviation(3)       #用于设置高斯分布函数的标准差
    gaussianSmoothFilter.Update()
    
    #Write a Gaussian PNG Image
    writer = vtk.vtkPNGWriter()
    writer.SetFileName("../data/PET_Gaussian.png")
    writer.SetInputData(gaussianSmoothFilter.GetOutput())
    writer.Write()

    originalActor=vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    smoothedActor=vtk.vtkImageActor()
    smoothedActor.SetInputData(gaussianSmoothFilter.GetOutput())
    

    originalViewport = [0.0, 0.0, 0.5, 1.0]
    smoothedViewport=[0.5, 0.0, 1.0, 1.0]

    originalRenderer=vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    gradientMagnitudeRenderer=vtk.vtkRenderer()
    gradientMagnitudeRenderer.SetViewport(smoothedViewport)
    gradientMagnitudeRenderer.AddActor(smoothedActor)
    gradientMagnitudeRenderer.ResetCamera()
    gradientMagnitudeRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(gradientMagnitudeRenderer)
    renderWindow.SetSize(1024,512)
    renderWindow.Render()
    renderWindow.SetWindowName("GaussianFilter")

    renderWindowInteractor=vtk.vtkRenderWindowInteractor()
    style=vtk.vtkInteractorStyle()
    #定义一个vtkInteractorStyle对象 设置交互对象
    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()









