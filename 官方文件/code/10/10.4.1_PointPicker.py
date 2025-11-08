import vtk

class PointPickerInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()
        print("Picking pixel: ",clickPos)
        xyz = [clickPos[0], clickPos[1], 0]
        picker = vtk.vtkPointPicker()
        picker.Pick(xyz, self.GetDefaultRenderer())

        picked = picker.GetPickPosition()
        print(picked)
        sphere = vtk.vtkSphereSource()
        sphere.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        actor.SetPosition(picked)
        actor.SetScale(0.05)
        actor.GetProperty().SetColor(1.0, 0.0, 0.0)
        self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
        self.OnLeftButtonDown()
        return

def main():
    sphereSource = vtk.vtkSphereSource()
    sphereSource.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.0,0.0,1.0)

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.Render()
    renWin.SetWindowName("Point Picker")
    renWin.AddRenderer(ren)
    renWin.SetSize(500,500)

    pointPicker = vtk.vtkPointPicker()
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetPicker(pointPicker)
    iren.SetRenderWindow(renWin)

    style = PointPickerInteractorStyle()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle( style )

    ren.AddActor(actor)
    ren.SetBackground(1.0,1.0,1.0)
    iren.Start()
if __name__ == '__main__':
    main()