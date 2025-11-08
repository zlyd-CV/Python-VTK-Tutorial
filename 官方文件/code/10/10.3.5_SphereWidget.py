import vtk

def sphereCallback(obj, event):
    print('Center: {}, {}, {}'.format(*obj.GetCenter()))

def main():
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.8, 0.8, 0.8)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    sphereWidget = vtk.vtkSphereWidget()
    sphereWidget.SetInteractor(iren)
    sphereWidget.SetRepresentationToSurface()
    sphereWidget.GetSphereProperty().SetColor(0.1, 0.4, 0.5)
    sphereWidget.On()
    sphereWidget.AddObserver("InteractionEvent", sphereCallback)

    iren.Initialize()
    renWin.Render()
    iren.Start()
if __name__ == '__main__':
    main()