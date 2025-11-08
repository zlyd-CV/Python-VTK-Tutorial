import vtk

reader = vtk.vtkPolyDataReader()
reader.SetFileName('../data/test.vtk')
curv = vtk.vtkCurvatures()
curv.SetInputConnection(reader.GetOutputPort())
curv.SetCurvatureTypeToGaussian()
curv.Update()
curvOutput = curv.GetOutput()

for i in range(curvOutput.GetPointData().GetNumberOfArrays()):
    print(curvOutput.GetPointData().GetArrayName(i))

# To set the active scalar to Gauss_Curvature
curvOutput.GetPointData().SetActiveScalars('Gauss_Curvature')

polyDataMapper = vtk.vtkPolyDataMapper()
polyDataMapper.SetInputConnection(curv.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(polyDataMapper)

ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.ResetCamera()
ren.SetBackground(1.0, 1.0, 1.0)

renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)
renwin.SetSize(640, 480)
renwin.Render()
renwin.SetWindowName("Curvatures")

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)
iren.Initialize()
iren.Start()
