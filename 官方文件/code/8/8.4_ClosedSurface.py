import vtk

sphereSource = vtk.vtkSphereSource()
sphereSource.Update()

ids = vtk.vtkIdTypeArray()
ids.SetNumberOfComponents(1)
ids.InsertNextValue(2)
ids.InsertNextValue(10)

selectionNode = vtk.vtkSelectionNode()
selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
selectionNode.SetSelectionList(ids)
selectionNode.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)

selection = vtk.vtkSelection()
selection.AddNode(selectionNode)

extractSelection = vtk.vtkExtractSelection()
extractSelection.SetInputConnection(0, sphereSource.GetOutputPort())
extractSelection.SetInputData(1, selection)
extractSelection.Update()

surface = vtk.vtkDataSetSurfaceFilter()
surface.SetInputConnection(extractSelection.GetOutputPort())
surface.Update()

featureEdges = vtk.vtkFeatureEdges()
featureEdges.SetInputData(surface.GetOutput())
featureEdges.BoundaryEdgesOn()
featureEdges.FeatureEdgesOff()
featureEdges.NonManifoldEdgesOff()
featureEdges.ManifoldEdgesOff()
featureEdges.Update()

numberOfOpenEdges = featureEdges.GetOutput().GetNumberOfCells()
if numberOfOpenEdges == 0:
    print("No open edges.")
else:
    print("%d open edges." % numberOfOpenEdges)

fillHoles = vtk.vtkFillHolesFilter()
fillHoles.SetInputData(surface.GetOutput())
fillHoles.Update()

normals = vtk.vtkPolyDataNormals()
normals.SetInputData(fillHoles.GetOutput())
normals.ConsistencyOn()
normals.SplittingOff()
normals.Update()

leftViewPort = [0.0, 0.0, 0.5, 1.0]
rightViewPort = [0.5, 0.0, 1.0, 1.0]

originalMapper = vtk.vtkPolyDataMapper()
originalMapper.SetInputData(surface.GetOutput())
backFaceProperty = vtk.vtkProperty()
backFaceProperty.SetDiffuseColor(0.89, 0.81, 0.34)
originalActor = vtk.vtkActor()
originalActor.SetMapper(originalMapper)
originalActor.SetBackfaceProperty(backFaceProperty)
originalActor.GetProperty().SetDiffuseColor(1.0, 0.3882, 0.2784)

edgeMapper = vtk.vtkPolyDataMapper()
edgeMapper.SetInputData(featureEdges.GetOutput())
edgeActor = vtk.vtkActor()
edgeActor.SetMapper(edgeMapper)
edgeActor.GetProperty().SetEdgeColor(0., 0., 1.0)
edgeActor.GetProperty().SetEdgeVisibility(1)
edgeActor.GetProperty().SetLineWidth(5)

filledMapper = vtk.vtkPolyDataMapper()
filledMapper.SetInputData(normals.GetOutput())
filledActor = vtk.vtkActor()
filledActor.SetMapper(filledMapper)
filledActor.GetProperty().SetDiffuseColor(1.0, 0.3882, 0.2784)

leftRenderer = vtk.vtkRenderer()
leftRenderer.SetViewport(leftViewPort)
leftRenderer.AddActor(originalActor)
leftRenderer.AddActor(edgeActor)
leftRenderer.SetBackground(1.0, 1.0, 1.0)

rightRenderer = vtk.vtkRenderer()
rightRenderer.SetViewport(rightViewPort)
rightRenderer.AddActor(filledActor)
rightRenderer.SetBackground(0, 0, 0)

renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(600, 300)
renderWindow.AddRenderer(leftRenderer)
renderWindow.AddRenderer(rightRenderer)
renderWindow.Render()
renderWindow.SetWindowName("ClosedSurface")

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)
rightRenderer.SetActiveCamera(leftRenderer.GetActiveCamera())
iren.Initialize()
iren.Start()
