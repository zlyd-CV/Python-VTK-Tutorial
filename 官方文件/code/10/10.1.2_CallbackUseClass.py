import vtk

class UseClassCallback(object):
    def __init__(self, source,cam):
        self.ClickTimes = 0
        self.source = source
        self.cam = cam

    def __call__(self, caller, ev):
        self.ClickTimes += 1
        print("Clicked", self.ClickTimes, "Times")
        print("Hight: ", self.source.GetHeight())
        print("Radius:",self.source.GetRadius())

        print("Position:", self.cam.GetPosition())
        print("Focal point:", self.cam.GetFocalPoint())
        print("Clipping range:", self.cam.GetClippingRange())
        print("View up:",self.cam.GetViewUp())

def main():
    source = vtk.vtkConeSource()
    source.SetCenter(0, 0, 0)
    source.SetRadius(1)

    source.SetHeight(2)
    source.SetResolution(100)
    source.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.5,0.5,0.8)

    actor.GetProperty().SetAmbient(0.3)
    actor.GetProperty().SetDiffuse(0.0)
    actor.GetProperty().SetSpecular(1.0)
    actor.GetProperty().SetSpecularPower(20.0)

    ren = vtk.vtkRenderer()

    camera = vtk.vtkCamera()
    camera.SetPosition(4.6, -2.0, 3.8)
    camera.SetFocalPoint(0.0, 0.0, 0.0)
    camera.SetClippingRange(3.2, 10.2)
    camera.SetViewUp(0.3, 1.0, 0.13)
    ren.SetActiveCamera(camera)

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.AddActor(actor)
    ren.SetBackground(0.8,0.8,0.8)
    renWin.SetSize(512, 512)

    renWin.Render()
    renWin.SetWindowName("CallBacUseClass")
    iren.AddObserver('LeftButtonPressEvent', UseClassCallback(source, ren.GetActiveCamera()))

    iren.Initialize()
    iren.Start()
if __name__ == "__main__":
    main()
