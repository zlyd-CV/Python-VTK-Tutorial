import vtk

def main():
    #Create a sphere
    sphereSource = vtk.vtkSphereSource()
    sphereSource.Update()

    dijkstra =vtk.vtkDijkstraGraphGeodesicPath()
    dijkstra.SetInputConnection(sphereSource.GetOutputPort())
    dijkstra.SetStartVertex(0)
    dijkstra.SetEndVertex(10)
    dijkstra.Update()

    #Create a mapper and actor
    pathMapper =vtk.vtkPolyDataMapper()
    pathMapper.SetInputConnection(dijkstra.GetOutputPort())

    pathActor =vtk.vtkActor()
    pathActor.SetMapper(pathMapper)
    pathActor.GetProperty().SetColor(1,0,0)
    pathActor.GetProperty().SetLineWidth(4)

    #Create a mapper and actor
    mapper =vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())

    actor =vtk.vtkActor()
    actor.SetMapper(mapper)

    #Create a renderer, render window, and interactor
    renderer =vtk.vtkRenderer()
    renderWindow =vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    #Add the actor to the scene
    renderer.AddActor(actor)
    renderer.AddActor(pathActor)
    renderer.SetBackground(.3, .6, .3)   #Background color green

    #Render and interact
    renderWindow.Render();
    renderWindow.SetWindowName("DijkstraGraphGeodesicPath")
    renderWindowInteractor.Start();


if __name__ == "__main__":
    main()