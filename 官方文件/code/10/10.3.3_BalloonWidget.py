import vtk

def main():
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(-4.0, 0.0, 0.0)
    sphereSource.SetRadius(4.0)

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())
    sphereActor = vtk.vtkActor()

    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(0.3,0.3,1.0)

    regularPolygonSource = vtk.vtkRegularPolygonSource()
    regularPolygonSource.SetCenter(4.0, 0.0, 0.0)
    regularPolygonSource.SetRadius(4.0)

    regularPolygonMapper = vtk.vtkPolyDataMapper()
    regularPolygonMapper.SetInputConnection(regularPolygonSource.GetOutputPort())

    regularPolygonActor = vtk.vtkActor()
    regularPolygonActor.SetMapper(regularPolygonMapper)
    regularPolygonActor.GetProperty().SetColor(0.9,0.5,0.5)

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    rep = vtk.vtkBalloonRepresentation()
    rep.SetBalloonLayoutToImageRight()

    balloonWidget = vtk.vtkBalloonWidget()
    balloonWidget.SetInteractor(iren)
    balloonWidget.SetRepresentation(rep)
    balloonWidget.AddBalloon(sphereActor, "This is a sphere")
    balloonWidget.AddBalloon(regularPolygonActor, "This is a regular polygon")
    balloonWidget.EnabledOn()

    ren.AddActor(sphereActor)
    ren.AddActor(regularPolygonActor)
    ren.SetBackground(0.8,0.8,0.8)

    renWin.Render()
    renWin.SetWindowName("Balloon Widget")
    iren.Start()
    iren.Initialize()
if __name__ == '__main__':
    main()