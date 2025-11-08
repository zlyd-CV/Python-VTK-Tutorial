import vtk


def main():
    sphereSource = vtk.vtkSphereSource()
    sphereSource.Update()
    original = sphereSource.GetOutput()

    print("抽取前")
    print(f"There are {original.GetNumberOfPoints()} points.")
    print(f"There are {original.GetNumberOfPolys()} polygons.")

    subdivision = vtk.vtkLoopSubdivisionFilter()
    subdivision.SetNumberOfSubdivisions(2)
    subdivision.SetInputData(original)
    subdivision.Update()

    subdivided = subdivision.GetOutput()
    print("抽取后")
    print(f"There are {subdivided.GetNumberOfPoints()} points.")
    print(f"There are {subdivided.GetNumberOfPolys()} polygons.")

    origianlMapper = vtk.vtkPolyDataMapper()
    origianlMapper.SetInputData(original)
    origianlMapper.Update()

    origianlActor = vtk.vtkActor()
    origianlActor.SetMapper(origianlMapper)

    subdividedMapper = vtk.vtkPolyDataMapper()
    subdividedMapper.SetInputData(subdivided)

    subdividedActor = vtk.vtkActor()
    subdividedActor.SetMapper(subdividedMapper)

    originalViewport = [0.0, 0.0, 0.5, 1.0]
    linearViewport = [0.5, 0.0, 1.0, 1.0]
    loopViewport = [1.0, 0.0, 1.5, 1.0]
    butterflyViewport = [1.5, 0.0, 2.0, 1.0]

    originalRen = vtk.vtkRenderer()
    originalRen.SetViewport(originalViewport)
    originalRen.AddActor(origianlActor)
    originalRen.SetBackground(0.8, 0.8, 0.8)

    subdividedRen = vtk.vtkRenderer()
    subdividedRen.SetViewport(linearViewport)
    subdividedRen.AddActor(subdividedActor)
    subdividedRen.SetBackground(1.0, 1.0, 1.0)

    originalRen.GetActiveCamera().SetPosition(0, -1, 0)
    originalRen.GetActiveCamera().SetFocalPoint(0, 0, 0)
    originalRen.GetActiveCamera().SetViewUp(0, 0, 1)
    originalRen.GetActiveCamera().Azimuth(30)
    originalRen.GetActiveCamera().Elevation(30)
    originalRen.ResetCamera()
    subdividedRen.SetActiveCamera(originalRen.GetActiveCamera())

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(subdividedRen)
    renWin.AddRenderer(originalRen)
    renWin.SetSize(640, 320)
    renWin.Render()
    renWin.SetWindowName("Subdivision")

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    main()
