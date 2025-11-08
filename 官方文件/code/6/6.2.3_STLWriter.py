import vtk

def main():
    filename = "Arrow.stl"
    arrowSource = vtk.vtkArrowSource()
    arrowSource.Update()

    stlWriter = vtk.vtkSTLWriter()
    stlWriter.SetFileName(filename)
    stlWriter.SetInputConnection(arrowSource.GetOutputPort())
    stlWriter.Write()

    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()
    ren.SetBackground(0.6,0.6,0.8)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.AddActor(actor)
    iren.Initialize()
    renWin.Render()
    renWin.SetWindowName("STL Writer")
    iren.Start()
if __name__ == '__main__':
    main()