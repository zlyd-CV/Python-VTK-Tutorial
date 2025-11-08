import vtk

cube=vtk.vtkCubeSource()
cube.Update()

triFilter =  vtk.vtkTriangleFilter()
triFilter.SetInputConnection(cube.GetOutputPort())
triFilter.Update()

massProp =  vtk.vtkMassProperties()
massProp.SetInputConnection(triFilter.GetOutputPort())

print(cube)
print("Volume:",massProp.GetVolume())
print("Surface Area:",massProp.GetSurfaceArea())
print("Max Area:",massProp.GetMaxCellArea())
print("Min Area:",massProp.GetMinCellArea())

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(triFilter.GetOutputPort())

actor =  vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0,1,0)
actor.GetProperty().SetEdgeColor(0,0,0)
actor.GetProperty().SetEdgeVisibility(1)

renderer =  vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0,1.0,1.0)

renwin=vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)
renwin.SetSize( 640, 480 )
renwin.Render()
renwin.SetWindowName("PolyDataMassProperty")

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

renwin.Render()
iren.Initialize()
iren.Start()




