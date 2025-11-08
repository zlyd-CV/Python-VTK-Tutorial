import vtk

def main():
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetWindowName("OrientationMarker Widget")
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    cube = vtk.vtkCubeSource()
    cube.SetXLength(200)
    cube.SetYLength(200)
    cube.SetZLength(200)
    cube.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cube.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.9,0.9,1.0)

    ren.AddActor(actor)
    ren.SetBackground(0.3, 0.7, 1.0)

    axesActor = vtk.vtkAnnotatedCubeActor()
    axesActor.SetXPlusFaceText('R')
    axesActor.SetXMinusFaceText('L')
    axesActor.SetYMinusFaceText('H')
    axesActor.SetYPlusFaceText('F')
    axesActor.SetZMinusFaceText('P')
    axesActor.SetZPlusFaceText('A')
    axesActor.GetTextEdgesProperty().SetColor(1.0,0.5,0.0)
    axesActor.GetTextEdgesProperty().SetLineWidth(2)
    axesActor.GetCubeProperty().SetColor(0.0,0.0,1.0)

    axes = vtk.vtkOrientationMarkerWidget()
    axes.SetOrientationMarker(axesActor)
    axes.SetInteractor(iren)
    axes.EnabledOn()
    axes.InteractiveOn()

    ren.ResetCamera()
    iren.Initialize()
    ren.GetActiveCamera().SetPosition(-151.5, 540.1, 364.0)
    ren.GetActiveCamera().SetViewUp(0.2, 0.6, -0.8)
    renWin.Render()
    iren.Start()
if __name__ == '__main__':
    main()