import vtk

def main():
    lut = vtk.vtkLookupTable()
    lut.Build()

    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName("../data/uGridEx.vtk")
    reader.Update()

    scalarRange = reader.GetOutput().GetScalarRange()
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    mapper.SetScalarRange(scalarRange)
    mapper.SetLookupTable(lut)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground( 0.2, 0.4, 1.0)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(300, 300)
    renWin.Render()
    renWin.SetWindowName("ScalarBar Widget")
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()

    scalarbar = vtk.vtkScalarBarActor()
    scalarbar.SetOrientationToHorizontal()
    scalarbar.SetLookupTable(lut)

    scalarbarwidget = vtk.vtkScalarBarWidget()
    scalarbarwidget.SetInteractor(iren)
    scalarbarwidget.SetScalarBarActor(scalarbar)
    scalarbarwidget.On()

    ren.GetActiveCamera().SetPosition(-6.4, 10.3, 1.4)
    ren.GetActiveCamera().SetFocalPoint(1.0, 0.5, 3.0)
    ren.GetActiveCamera().SetViewUp(0.6, 0.4, -0.7)

    iren.Start()
if __name__ == '__main__':
    main()