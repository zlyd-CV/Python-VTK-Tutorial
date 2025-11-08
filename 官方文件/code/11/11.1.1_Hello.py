import vtk

def main():
    reader= vtk.vtkPolyDataReader()
    reader.SetFileName("../data/hello.vtk")

    lineMapper= vtk.vtkPolyDataMapper()
    lineMapper.SetInputConnection(reader.GetOutputPort())

    lineActor= vtk.vtkActor()
    lineActor.SetMapper(lineMapper)
    lineActor.GetProperty().SetColor(1.0,0.0,0.0)
    lineActor.GetProperty().SetLineWidth(3.0)

    imp= vtk.vtkImplicitModeller()
    imp.SetInputConnection(reader.GetOutputPort())
    imp.SetSampleDimensions(110, 40, 20)
    imp.SetMaximumDistance(0.25)
    imp.SetModelBounds(-1.0, 10.0, -1.0, 3.0, -1.0, 1.0)

    contour= vtk.vtkContourFilter()
    contour.SetInputConnection(imp.GetOutputPort())
    contour.SetValue(0, 0.25)

    impMapper= vtk.vtkPolyDataMapper()
    impMapper.SetInputConnection(contour.GetOutputPort())
    impMapper.ScalarVisibilityOff()

    impActor= vtk.vtkActor()
    impActor.SetMapper(impMapper)
    impActor.GetProperty().SetColor(0.3,0.3,1.0)
    impActor.GetProperty().SetOpacity(0.5)

    ren= vtk.vtkRenderer()
    ren.AddActor(lineActor)
    ren.AddActor(impActor)
    ren.SetBackground(0.8,0.8,0.8)

    renWin= vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetSize(640, 480)
    renWin.SetWindowName("Hello")

    iren= vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    camera= vtk.vtkCamera()
    camera.SetFocalPoint(4.5, 1,  0)
    camera.SetPosition(4.5, 1.0, 6.73257)
    camera.SetViewUp(0,  1,  0)

    ren.SetActiveCamera(camera)
    ren.ResetCamera()
    camera.Dolly(1.3)
    camera.SetClippingRange(1.81325, 90.6627)
    iren.Start()
if __name__ == '__main__':
    main()
