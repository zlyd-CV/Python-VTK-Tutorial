import vtk

def main():

    #Create a line
    lineSource =vtk.vtkLineSource()
    lineSource.SetPoint1(1.0, 0.0, 0.0)
    lineSource.SetPoint2(0.0, 1.0, 0.0);

    #Create a mapper and actor
    lineMapper =vtk.vtkPolyDataMapper()
    lineMapper.SetInputConnection(lineSource.GetOutputPort())

    lineActor =vtk.vtkActor()
    lineActor.GetProperty().SetColor(0.0,0.5,0.1)
    lineActor.SetMapper(lineMapper);

    #Create a tube (cylinder) around the line
    tubeFilter =vtk.vtkTubeFilter()
    tubeFilter.SetInputConnection(lineSource.GetOutputPort())
    tubeFilter.SetRadius(.025)
    tubeFilter.SetNumberOfSides(50)
    tubeFilter.Update()

    #Create a mapper and actor
    tubeMapper =vtk.vtkPolyDataMapper()
    tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
    tubeActor =vtk.vtkActor()
    tubeActor.GetProperty().SetOpacity(0.5)
    tubeActor.SetMapper(tubeMapper);

    #Create a renderer, render window, and interactor
    renderer =vtk.vtkRenderer()
    renderWindow =vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    #Add the actor to the scene
    renderer.AddActor(tubeActor)
    renderer.SetBackground(.3, .6, .3)   #Background color green

    #Render and interact
    renderWindow.Render();
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()