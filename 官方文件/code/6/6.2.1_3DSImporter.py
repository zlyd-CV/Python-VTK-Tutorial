import vtk

def main():
    fileName = "../data/iflamigm.3ds"
    importer = vtk.vtk3DSImporter()
    importer.SetFileName(fileName)
    importer.ComputeNormalsOn()

    colors = vtk.vtkNamedColors()

    renderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()

    renWin.AddRenderer(renderer)
    renderer.SetBackground2(colors.GetColor3d("Gold"))
    renderer.SetBackground(colors.GetColor3d("Wheat"))
    renderer.GradientBackgroundOn()

    iren.SetRenderWindow(renWin)
    importer.SetRenderWindow(renWin)
    importer.Update()

    actors = renderer.GetActors()
    print("There are", actors.GetNumberOfItems(), "actors")

    renWin.Render()
    camera = vtk.vtkCamera()
    camera.SetPosition(0, -1, 0)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    camera.Azimuth(150)
    camera.Elevation(30)

    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    renderer.ResetCameraClippingRange()

    renWin.Render()
    renWin.SetWindowName("3DS Importer")
    iren.Start()
if __name__ == '__main__':
    main()
