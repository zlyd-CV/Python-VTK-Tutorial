import vtk

def main():
    colors = vtk.vtkNamedColors()
    cone = vtk.vtkCone()
    cone.SetAngle(20)
    vertPlane = vtk.vtkPlane()
    vertPlane.SetOrigin(.1, 0, 0)
    vertPlane.SetNormal(-1, 0, 0)
    basePlane = vtk.vtkPlane()
    basePlane.SetOrigin(1.2, 0, 0)
    basePlane.SetNormal(1, 0, 0)
    iceCream = vtk.vtkSphere()
    iceCream.SetCenter(1.333, 0, 0)
    iceCream.SetRadius(0.5)
    bite = vtk.vtkSphere()
    bite.SetCenter(1.5, 0, 0.5)
    bite.SetRadius(0.25)

    theCone = vtk.vtkImplicitBoolean()
    theCone.SetOperationTypeToIntersection()
    theCone.AddFunction(cone)
    theCone.AddFunction(vertPlane)
    theCone.AddFunction(basePlane)

    theCream = vtk.vtkImplicitBoolean()
    theCream.SetOperationTypeToDifference()
    theCream.AddFunction(iceCream)
    theCream.AddFunction(bite)

    theConeSample = vtk.vtkSampleFunction()
    theConeSample.SetImplicitFunction(theCone)
    theConeSample.SetModelBounds(-1, 1.5, -1.25, 1.25, -1.25, 1.25)
    theConeSample.SetSampleDimensions(128, 128, 128)
    theConeSample.ComputeNormalsOff()

    theConeSurface = vtk.vtkContourFilter()
    theConeSurface.SetInputConnection(theConeSample.GetOutputPort())
    theConeSurface.SetValue(0, 0.0)

    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(theConeSurface.GetOutputPort())
    coneMapper.ScalarVisibilityOff()

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d("chocolate"))

    theCreamSample = vtk.vtkSampleFunction()
    theCreamSample.SetImplicitFunction(theCream)
    theCreamSample.SetModelBounds(0, 2.5, -1.25, 1.25, -1.25, 1.25)
    theCreamSample.SetSampleDimensions(128, 128, 128)
    theCreamSample.ComputeNormalsOff()

    theCreamSurface = vtk.vtkContourFilter()
    theCreamSurface.SetInputConnection(theCreamSample.GetOutputPort())
    theCreamSurface.SetValue(0, 0.0)

    creamMapper = vtk.vtkPolyDataMapper()
    creamMapper.SetInputConnection(theCreamSurface.GetOutputPort())
    creamMapper.ScalarVisibilityOff()

    creamActor = vtk.vtkActor()
    creamActor.SetMapper(creamMapper)
    creamActor.GetProperty().SetDiffuseColor(colors.GetColor3d("mint"))
    creamActor.GetProperty().SetSpecular(.6)
    creamActor.GetProperty().SetSpecularPower(50)

    ren = vtk.vtkRenderer()
    ren.AddActor(coneActor)
    ren.AddActor(creamActor)
    ren.SetBackground(colors.GetColor3d("SlateGray"))
    ren.ResetCamera()
    ren.GetActiveCamera().Roll(90)
    ren.GetActiveCamera().Dolly(1.25)
    ren.ResetCameraClippingRange()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(640, 480)
    renWin.Render()
    renWin.SetWindowName("Ice Cream")
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    iren.Initialize()
    iren.Start()
if __name__ == '__main__':
    main()
