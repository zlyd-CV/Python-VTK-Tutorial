import vtk

def main():
    ConeSource = vtk.vtkConeSource()
    ConeSource.SetResolution(50)
    ConeSource.SetHeight(5)
    ConeSource.SetRadius(2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(ConeSource.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.1,0.8,0)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    compassRepresentation = vtk.vtkCompassRepresentation()
    compassWidget = vtk.vtkCompassWidget()
    compassWidget.SetInteractor(renderWindowInteractor)
    compassWidget.SetRepresentation(compassRepresentation)

    #eventTranslator = compassWidget.GetEventTranslator()
    #eventTranslator.SetTranslation(vtk.vtkCommand.RightButtonPressEvent, vtk.vtkWidgetEvent.Select)
    #eventTranslator.SetTranslation(vtk.vtkCommand.RightButtonReleaseEvent, vtk.vtkWidgetEvent.EndSelect)

    renderer.AddActor(actor)
    renderer.SetBackground(0.4,0.4,0.5)
    renderWindow.Render()
    compassWidget.EnabledOn()

    style = vtk.vtkInteractorStyleTrackballCamera()
    renderWindowInteractor.SetInteractorStyle(style)

    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindow.SetWindowName("vtkWidgetEventTranslator")
    renderWindowInteractor.Start()
if __name__ == '__main__':
    main()
