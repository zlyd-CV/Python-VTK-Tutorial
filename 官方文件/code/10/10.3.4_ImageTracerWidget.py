import vtk

def CallbackFunction(caller,eventId):
     tracerWidget =caller
     path = vtk.vtkPolyData()
     tracerWidget.GetPath(path)
     for i in range(path.GetNumberOfPoints()):
         print(path.GetPoint(i))

def main():
    drawColor1=(1, 0, 0)
    drawColor2=(0, 0.5, 1)
    
    imageSource=vtk.vtkDICOMImageReader()
    imageSource.SetFileName("../data/CT_head.dcm")    
    imageSource.Update()

    actor=vtk.vtkImageActor()
    actor.GetMapper().SetInputConnection(imageSource.GetOutputPort())

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(0, 0.2, 0)
    ren.ResetCamera();
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetWindowName("ImageTracer Widget")

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    style = vtk.vtkInteractorStyleImage()
    iren.SetInteractorStyle(style)

    tracer = vtk.vtkImageTracerWidget()
    tracer.GetLineProperty().SetLineWidth(1)
    tracer.SetCaptureRadius(100)
    tracer.SetInteractor(iren)
    tracer.SetViewProp(actor)
    tracer.SetAutoClose(1)
    tracer.AddObserver('EndInteractionEvent',CallbackFunction)
    tracer.On()

    iren.Start()
if __name__ == '__main__':
    main()

