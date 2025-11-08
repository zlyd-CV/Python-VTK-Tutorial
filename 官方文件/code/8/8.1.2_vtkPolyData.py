import vtk

points=vtk.vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(2.0, 0.0, 0.0)

polygon=vtk.vtkPolygon()
polygon.GetPointIds().SetNumberOfIds(4)
polygon.GetPointIds().SetId(0, 0)
polygon.GetPointIds().SetId(1, 1)
polygon.GetPointIds().SetId(2,2)
polygon.GetPointIds().SetId(3,3)

trianle=vtk.vtkTriangle()
trianle.GetPointIds().SetId(0, 1)
trianle.GetPointIds().SetId(1, 2)
trianle.GetPointIds().SetId(2, 4)

cells=vtk.vtkCellArray()
cells.InsertNextCell(polygon)
cells.InsertNextCell(trianle)

polygonPolyData = vtk.vtkPolyData()
polygonPolyData.SetPoints(points)
polygonPolyData.SetPolys(cells)

mapper=vtk.vtkPolyDataMapper()
mapper.SetInputData(polygonPolyData)

actor=vtk.vtkActor()
actor.SetMapper(mapper)

renderer=vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5,0.5,0.5)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize( 640, 480 )
renderWindow.Render()
renderWindow.SetWindowName("PolyDataNew")

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)

iren.Initialize()
iren.Start()
