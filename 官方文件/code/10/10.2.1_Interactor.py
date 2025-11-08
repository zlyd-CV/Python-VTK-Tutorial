import vtk

def main():
    reader=vtk.vtkPNGReader()
    reader.SetFileName('../data/vtk.PNG')
    reader.Update()

    imageActor=vtk.vtkImageActor()
    imageActor.SetInputData( reader.GetOutput() )
    imageActor.Update()

    renderer=vtk.vtkRenderer()
    renderer.AddActor( imageActor )
    renderer.SetBackground(1.0, 1.0, 1.0)


    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer( renderer )
    renWin.SetSize( 640, 480 )
    renWin.Render()
    renWin.SetWindowName("Interactor")

    iren =vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    style=vtk.vtkInteractorStyleImage()
    iren.SetInteractorStyle(style)
    iren.Initialize()
    iren.Start()

if __name__ == "__main__":
    main()












