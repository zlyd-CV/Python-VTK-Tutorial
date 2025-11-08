import vtk

def main():

    imageSource1 =vtk.vtkImageCanvasSource2D()
    imageSource1 .SetScalarTypeToUnsignedChar()
    imageSource1 .SetNumberOfScalarComponents(1)
    imageSource1 .SetExtent(0, 100, 0, 100, 0, 0)
    imageSource1 .SetDrawColor(0.0)
    imageSource1 .FillBox(0,100,0,100)
    imageSource1 .SetDrawColor(255.0)
    imageSource1 .FillBox(20,60,20,60)
    imageSource1 .Update()

    imageSource2=vtk.vtkImageCanvasSource2D()
    imageSource2 .SetScalarTypeToUnsignedChar()
    imageSource2 .SetNumberOfScalarComponents(1)
    imageSource2 .SetExtent(0, 100, 0, 100, 0, 0)
    imageSource2 .SetDrawColor(0.0)
    imageSource2 .FillBox(0,100,0,100)
    imageSource2 .SetDrawColor(255.0)
    imageSource2 .FillBox(40,80,40,80)
    imageSource2 .Update()

    imageLogic=vtk.vtkImageLogic()
    imageLogic.SetInput1Data(imageSource1.GetOutput())
    imageLogic.SetInput2Data(imageSource2.GetOutput())
    imageLogic.SetOperationToXor()
    imageLogic.SetOutputTrueValue(128)
    imageLogic.Update()

    originalActor1=vtk.vtkImageActor()
    originalActor1.SetInputData(imageSource1.GetOutput())

    originalActor2=vtk.vtkImageActor()
    originalActor2.SetInputData(imageSource1.GetOutput())

    logicActor=vtk.vtkImageActor()
    logicActor.SetInputData(imageLogic.GetOutput())

    leftViewport= [0.0, 0.0, 0.33, 1.0]
    midViewport=[0.33, 0.0, 0.66, 1.0]
    rightViewport = [0.66, 0.0, 1.0, 1.0]

    originalRenderer1=vtk.vtkRenderer()
    originalRenderer1.SetViewport(leftViewport)
    originalRenderer1.AddActor(originalActor1)
    originalRenderer1.ResetCamera()
    originalRenderer1.SetBackground(1.0, 1.0, 1.0)

    originalRenderer2=vtk.vtkRenderer()
    originalRenderer2.SetViewport(midViewport)
    originalRenderer2.AddActor(originalActor1)
    originalRenderer2.ResetCamera()
    originalRenderer2.SetBackground(0.8, 0.8, 0.8)

    logicRenderer=vtk.vtkRenderer()
    logicRenderer.SetViewport(rightViewport)
    logicRenderer.AddActor(logicActor)
    logicRenderer.ResetCamera()
    logicRenderer.SetBackground(0.6 ,0.6, 0.6)

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.AddRenderer(originalRenderer1)
    renderWindow.AddRenderer(originalRenderer2)
    renderWindow.AddRenderer(logicRenderer)
    renderWindow.SetSize(640, 320)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageLogic")

    renderWindowInteractor=vtk.vtkRenderWindowInteractor()
    style=vtk.vtkInteractorStyle()
    #定义一个vtkInteractorStyle对象 设置交互对象
    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()