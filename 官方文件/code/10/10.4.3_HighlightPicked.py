import vtk

NUMBER_OF_SPHERES = 10

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        self.NewPickedActor = picker.GetActor()
        if self.NewPickedActor:
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            self.NewPickedActor.GetProperty().SetColor(1.0,0,0)
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            self.LastPickedActor = self.NewPickedActor

        self.OnLeftButtonDown()
        return

def main():
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.5,0.5,0.5)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(500,500)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    style = MouseInteractorHighLightActor()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(style)

    for i in range(NUMBER_OF_SPHERES):
        source = vtk.vtkSphereSource()
        x = vtk.vtkMath.Random(-10, 10)
        y = vtk.vtkMath.Random(-10, 10)
        z = vtk.vtkMath.Random(-10, 10)
        radius = vtk.vtkMath.Random(.5, 1.0)

        source.SetRadius(radius)
        source.SetCenter(x, y, z)
        source.SetPhiResolution(11)
        source.SetThetaResolution(21)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        r = vtk.vtkMath.Random(.4, 1.0)
        g = vtk.vtkMath.Random(.4, 1.0)
        b = vtk.vtkMath.Random(.4, 1.0)
        actor.GetProperty().SetDiffuseColor(r, g, b)
        actor.GetProperty().SetDiffuse(.8)
        actor.GetProperty().SetSpecular(.5)
        actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        actor.GetProperty().SetSpecularPower(30.0)
        ren.AddActor(actor)

    iren.Initialize()
    renWin.Render()
    renWin.SetWindowName("Highlight Picked")
    iren.Start()
if __name__ == '__main__':
    main()