import vtk

def main():
    sphere = vtk.vtkSphere()
    sphere.SetRadius(1)
    sphere.SetCenter(1, 0, 0)
    box = vtk.vtkBox()
    box.SetBounds(-1, 1, -1, 1, -1, 1)

    boolean = vtk.vtkImplicitBoolean()
    boolean.SetOperationTypeToDifference()
    #boolean.SetOperationTypeToUnion()
    #boolean.SetOperationTypeToIntersection()
    boolean.AddFunction(box)
    boolean.AddFunction(sphere)

    sample = vtk.vtkSampleFunction()
    sample.SetImplicitFunction(boolean)
    sample.SetModelBounds(-1, 2, -1, 1, -1, 1)
    sample.SetSampleDimensions(40, 40, 40)
    sample.ComputeNormalsOff()

    surface = vtk.vtkContourFilter()
    surface.SetInputConnection(sample.GetOutputPort())
    surface.SetValue(0, 0.0)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    mapper.ScalarVisibilityOff()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetEdgeColor(.2, .2, .5)

    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.AddActor(actor)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetWindowName("Boolean")

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    iren.Initialize()
    iren.Start()
if __name__ == '__main__':
    main()