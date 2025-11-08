import vtk
import random

def main():
    # Generate a 10 x 10 grid of points
    points =vtk.vtkPoints()
    for x in range(10):

        for y in range(10):
            points.InsertNextPoint(x + random.uniform(-.25, .25),y + random.uniform(-.25,.25),0)

    aPolyData = vtk.vtkPolyData()
    aPolyData.SetPoints(points);

    # Create a cell array to store the polygon in
    aCellArray =vtk.vtkCellArray()

    # Define a polygonal hole with a clockwise polygon
    aPolygon =vtk.vtkPolygon()

    aPolygon.GetPointIds().InsertNextId(22)
    aPolygon.GetPointIds().InsertNextId(23)
    aPolygon.GetPointIds().InsertNextId(24)
    aPolygon.GetPointIds().InsertNextId(25)
    aPolygon.GetPointIds().InsertNextId(35)
    aPolygon.GetPointIds().InsertNextId(45)
    aPolygon.GetPointIds().InsertNextId(44)
    aPolygon.GetPointIds().InsertNextId(43)
    aPolygon.GetPointIds().InsertNextId(42)
    aPolygon.GetPointIds().InsertNextId(32)
    aCellArray.InsertNextCell(aPolygon)

    # Create a polydata to store the boundary. The points must be the
    # same as the points we will triangulate.
    boundary =vtk.vtkPolyData()
    boundary.SetPoints(aPolyData.GetPoints())
    boundary.SetPolys(aCellArray)

    # Triangulate the grid points
    delaunay =vtk.vtkDelaunay2D()
    delaunay.SetInputData(aPolyData)
    delaunay.SetSourceData(boundary)

    # Visualize
    meshMapper =vtk.vtkPolyDataMapper()
    meshMapper.SetInputConnection(delaunay.GetOutputPort())

    meshActor =vtk.vtkActor()
    meshActor.SetMapper(meshMapper)
    meshActor.GetProperty().EdgeVisibilityOn()
    #meshActor.GetProperty().SetEdgeColor(colors.GetColor3d("Peacock").GetData())
    meshActor.GetProperty().SetEdgeColor(0.8,0.2,0.6)
    meshActor.GetProperty().SetInterpolationToFlat()

    boundaryMapper =vtk.vtkPolyDataMapper()
    boundaryMapper.SetInputData(boundary)

    boundaryActor =vtk.vtkActor()
    boundaryActor.SetMapper(boundaryMapper)
    boundaryActor.GetProperty().SetColor(0.2,0.2,0.2)
    boundaryActor.GetProperty().SetLineWidth(3)
    boundaryActor.GetProperty().EdgeVisibilityOn()
    boundaryActor.GetProperty().SetEdgeColor(1,0,0)
    boundaryActor.GetProperty().SetRepresentationToWireframe()

    # Create a renderer, render window, and interactor
    renderer =vtk.vtkRenderer()
    renderWindow =vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(meshActor)
    renderer.AddActor(boundaryActor)
    renderer.SetBackground((0.2,0.2,0.0))

    # Render and interact
    renderWindow.SetSize(500, 500)
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
