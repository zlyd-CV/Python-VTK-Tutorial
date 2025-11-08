import vtk

def main():
    colors = vtk.vtkNamedColors()

    points = vtk.vtkPoints()
    points.InsertPoint(0, 1.0, 0.0, 0.0)
    points.InsertPoint(1, 1.0732, 0.0, -0.1768)
    points.InsertPoint(2, 1.25, 0.0, -0.25)
    points.InsertPoint(3, 1.4268, 0.0, -0.1768)
    points.InsertPoint(4, 1.5, 0.0, 0.00)
    points.InsertPoint(5, 1.4268, 0.0, 0.1768)
    points.InsertPoint(6, 1.25, 0.0, 0.25)
    points.InsertPoint(7, 1.0732, 0.0, 0.1768)

    poly = vtk.vtkCellArray()
    poly.InsertNextCell(8)  # The number of points.
    poly.InsertCellPoint(0)
    poly.InsertCellPoint(1)
    poly.InsertCellPoint(2)
    poly.InsertCellPoint(3)
    poly.InsertCellPoint(4)
    poly.InsertCellPoint(5)
    poly.InsertCellPoint(6)
    poly.InsertCellPoint(7)

    profile = vtk.vtkPolyData()
    profile.SetPoints(points)
    profile.SetPolys(poly)


    extrude = vtk.vtkRotationalExtrusionFilter()
    extrude.SetInputData(profile)
    extrude.SetResolution(360)
    extrude.SetTranslation(6)
    extrude.SetDeltaRadius(1.0)
    extrude.SetAngle(2160.0)  # six revolutions

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(extrude.GetOutputPort())
    normals.SetFeatureAngle(60)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())

    spring = vtk.vtkActor()
    spring.SetMapper(mapper)
    spring.GetProperty().SetColor(colors.GetColor3d("PowderBlue"))
    spring.GetProperty().SetDiffuse(0.7)
    spring.GetProperty().SetSpecular(0.4)
    spring.GetProperty().SetSpecularPower(20)
    spring.GetProperty().BackfaceCullingOn()

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(640, 512)
    renWin.Render()
    renWin.SetWindowName("Spring")
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.AddActor(spring)
    ren.SetBackground(colors.GetColor3d("Burlywood"))
    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(90)
    iren.Start()
if __name__ == '__main__':
    main()
