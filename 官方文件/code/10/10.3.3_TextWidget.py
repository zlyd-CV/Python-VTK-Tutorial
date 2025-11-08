import vtk

def main():
    source = vtk.vtkSphereSource()
    source.SetRadius(15)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(0.8,0.8,0.8)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(300, 300)
    renWin.Render()
    renWin.SetWindowName("Text Widget")
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    textActor = vtk.vtkTextActor()
    textActor.SetInput("This is a Text Widget")
    textActor.GetTextProperty().SetColor(1.0,0.0,0.0)

    rep = vtk.vtkTextRepresentation()
    rep.GetPositionCoordinate().SetValue(0.15, 0.15)
    rep.GetPosition2Coordinate().SetValue(0.7, 0.2)

    textWidget = vtk.vtkTextWidget()
    textWidget.SetRepresentation(rep)
    textWidget.SetInteractor(iren)
    textWidget.SetTextActor(textActor)
    textWidget.SelectableOff()
    textWidget.On()

    iren.Initialize()
    iren.Start()
if __name__ == '__main__':
    main()