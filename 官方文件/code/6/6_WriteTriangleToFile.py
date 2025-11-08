import vtk


def main():
    
    Points = vtk.vtkPoints()
    Triangles = vtk.vtkCellArray()
    Triangle = vtk.vtkTriangle()
    
    id = Points.InsertNextPoint(1.0, 0.0, 0.0)
    id = Points.InsertNextPoint(0.0, 0.0, 0.0)
    id = Points.InsertNextPoint(0.0, 1.0, 0.0)
    
    Triangle.GetPointIds().SetId(0, 0)
    Triangle.GetPointIds().SetId(1, 1)
    Triangle.GetPointIds().SetId(2, 2)
    Triangles.InsertNextCell(Triangle)
    
    
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(Points)
    polydata.SetPolys(Triangles)
    polydata.Modified()
    if vtk.VTK_MAJOR_VERSION <= 5:
        polydata.Update()
    
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("../data/Triangle.vtp")
    writer.SetInputData(polydata)
    writer.Write()
    
if __name__ == '__main__':
    main()
