import vtk

def main():
    source = vtk.vtkSphereSource()
    source.SetRadius(100)
    source.SetPhiResolution(100)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(0.1, 0.2, 0.4)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(500, 500)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    rep = vtk.vtkSliderRepresentation3D()
    rep.SetValue(30)
    rep.SetMinimumValue(1)
    rep.SetMaximumValue(100)
    rep.SetTitleText("Resolution")
    rep.GetPoint1Coordinate().SetCoordinateSystemToWorld()
    rep.GetPoint1Coordinate().SetValue(1, -150, 0)
    rep.GetPoint2Coordinate().SetCoordinateSystemToWorld()
    rep.GetPoint2Coordinate().SetValue(200, -150, 0)
    rep.SetSliderLength(0.05)
    rep.SetSliderWidth(0.05)
    rep.SetEndCapLength(0.05)

    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetInteractor(iren)
    sliderWidget.SetRepresentation(rep)
    sliderWidget.SetAnimationModeToAnimate()
    sliderWidget.EnabledOn()

    def SelectResolution(object, event):
        slidervalue = int(round(object.GetRepresentation().GetValue()))
        source.SetPhiResolution(slidervalue)
        source.SetThetaResolution(slidervalue)

    sliderWidget.AddObserver("InteractionEvent", SelectResolution)

    iren.Initialize()
    renWin.Render()
    renWin.SetWindowName("Slider Widget")
    iren.Start()
if __name__ == '__main__':
    main()

























