import vtk

cone=vtk.vtkConeSource()
cone.Update()

print(cone)
npoints=[]
ncells=[]
cone.GetOutput().GetNumberOfPoints()
cone.GetOutput().GetNumberOfCells()

print("Points number:",str(npoints))
print("Cells  number:",str(ncells))

mapper=vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

actor=vtk.vtkActor()
actor.SetMapper(mapper)

renderer=vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)

renwin=vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)
renwin.SetSize(640,480)
renwin.Render()
renwin.SetWindowName("PolyDataSource")

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#style=vtk.vtkInteractorStyleTrackballCamera()
#iren.SetInteractorStyle(style)

renwin.Render()

iren.Initialize()
iren.Start()










