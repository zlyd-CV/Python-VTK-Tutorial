import vtk

def main():
    reader=vtk.vtkPolyDataReader()
    reader.SetFileName("../data/fran_cut.vtk")
    reader.Update()


    original=reader.GetOutput()

    print("抽取前")
    print("There are {original.GetNumberOfPoints()} points.")
    print("There are {original.GetNumberOfPolys()} polygons.")

    decimate=vtk.vtkDecimatePro()
    decimate.SetInputData(original)
    decimate.SetTargetReduction(.60);
    decimate.Update()

    decimated=decimate.GetOutput()
    print("抽取后")
    print("There are {decimated.GetNumberOfPoints()} points.")
    print("There are {decimated.GetNumberOfPolys()} polygons.")

    origianlMapper=vtk.vtkPolyDataMapper()
    origianlMapper.SetInputData(original)
    origianlMapper.Update()

    origianlActor=vtk.vtkActor()
    origianlActor.SetMapper(origianlMapper)

    decimatedMapper =vtk.vtkPolyDataMapper()
    decimatedMapper.SetInputData(decimated)

    decimatedActor=vtk.vtkActor()
    decimatedActor.SetMapper(decimatedMapper)

    leftViewport= [0.0, 0.0, 0.5, 1.0]
    rightViewport = [0.5, 0.0, 1.0, 1.0]

    leftRenderer=vtk.vtkRenderer()
    leftRenderer.SetViewport(leftViewport)
    leftRenderer.AddActor(origianlActor)
    leftRenderer.SetBackground(0.8, 0.8, 0.8)

    rightRenderer=vtk.vtkRenderer()
    rightRenderer.SetViewport(rightViewport)
    rightRenderer.AddActor(decimatedActor)
    rightRenderer.SetBackground(1.0,1.0,1.0)

    leftRenderer.GetActiveCamera().SetPosition(0, -1, 0)
    leftRenderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
    leftRenderer.GetActiveCamera().SetViewUp(0, 0, 1)
    leftRenderer.GetActiveCamera().Azimuth(30)
    leftRenderer.GetActiveCamera().Elevation(30)
    leftRenderer.ResetCamera()
    rightRenderer.SetActiveCamera(leftRenderer.GetActiveCamera())

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.AddRenderer(rightRenderer)
    renderWindow.AddRenderer(leftRenderer)
    renderWindow.SetSize(640, 320)
    renderWindow.Render()
    renderWindow.SetWindowName("PolyDataDecimation")

    iren=vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    iren.Initialize()
    iren.Start()

if __name__ == '__main__':
    main()









