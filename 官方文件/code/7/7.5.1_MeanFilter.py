import vtk

def main():
    reader = vtk.vtkPNGReader()
    reader.SetFileName("../data/CT_head.png")
    reader.Update()

    originalCastFilter=vtk.vtkImageCast()
    originalCastFilter.SetInputConnection(reader.GetOutputPort())
    originalCastFilter.SetOutputScalarTypeToFloat()
    originalCastFilter.Update()

    convolveFilter=vtk.vtkImageConvolve()
    convolveFilter.SetInputConnection(originalCastFilter.GetOutputPort())
    kernel = [0.04,0.04,0.04,0.04,0.04,
		      0.04,0.04,0.04,0.04,0.04,
		      0.04,0.04,0.04,0.04,0.04,
		      0.04,0.04,0.04,0.04,0.04,
		      0.04,0.04,0.04,0.04,0.04 ]
    convolveFilter.SetKernel5x5(kernel)
    convolveFilter.Update()

    convCastFilter=vtk.vtkImageCast()
    convCastFilter.SetInputData(convolveFilter.GetOutput())
    convCastFilter.SetOutputScalarTypeToUnsignedChar()
    convCastFilter.Update()

    originalActor =vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    convolvedActor=vtk.vtkImageActor()
    convolvedActor.SetInputData(convCastFilter.GetOutput())

    leftViewport= [0.0, 0.0, 0.5, 1.0]
    rightViewport= [0.5, 0.0, 1.0, 1.0]

    convolvedRenderer=vtk.vtkRenderer()
    convolvedRenderer.SetViewport(rightViewport)
    convolvedRenderer.AddActor(convolvedActor)
    convolvedRenderer.SetBackground(1.0, 1.0, 1.0)
    convolvedRenderer.ResetCamera()

    originalRenderer=vtk.vtkRenderer()
    originalRenderer.SetViewport(leftViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.SetBackground(1.0, 1.0, 1.0)
    originalRenderer.ResetCamera()

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(convolvedRenderer)
    renderWindow.SetSize(640,320)
    renderWindow.Render()
    renderWindow.SetWindowName("MeanFilter")

    renderWindowInteractor=vtk.vtkRenderWindowInteractor()
    style=vtk.vtkInteractorStyle()
    #定义一个vtkInteractorStyle对象 设置交互对象
    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()




