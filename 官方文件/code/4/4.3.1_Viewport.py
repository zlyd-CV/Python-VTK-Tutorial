import vtk

def main():
    
    cone=vtk.vtkConeSource()    
    cube=vtk.vtkCubeSource()    
    cylinder=vtk.vtkCylinderSource()
    outline=vtk.vtkOutlineSource()

    
    conemapper=vtk.vtkPolyDataMapper()
    conemapper.SetInputConnection(cone.GetOutputPort())
    cubemapper=vtk.vtkPolyDataMapper()
    cubemapper.SetInputConnection(cube.GetOutputPort())
    
    cylindermapper=vtk.vtkPolyDataMapper()
    cylindermapper.SetInputConnection(cylinder.GetOutputPort())
    outlinemapper=vtk.vtkPolyDataMapper()
    outlinemapper.SetInputConnection(outline.GetOutputPort())
    
    coneactor=vtk.vtkActor()
    coneactor.SetMapper(conemapper)
    cubeactor=vtk.vtkActor()
    cubeactor.SetMapper(cubemapper)
    cylinderactor=vtk.vtkActor()
    cylinderactor.SetMapper(cylindermapper)
    outlineactor=vtk.vtkActor()
    outlineactor.SetMapper(outlinemapper)
    
    ren1=vtk.vtkRenderer()
    ren1.AddActor(coneactor)
    ren1.SetBackground(0.5,0,0)
    ren1.SetViewport(0.0,0.0,0.5,0.5)
    
    ren2=vtk.vtkRenderer()
    ren2.AddActor(cubeactor)
    ren2.SetBackground(0,1,0)
    ren2.SetViewport(0.5,0.0,1.0,0.5)
    
    ren3=vtk.vtkRenderer()
    ren3.AddActor(cylinderactor)
    ren3.SetBackground(0,0,1)
    ren3.SetViewport(0.0,0.5,0.5,1.0)
    
    ren4=vtk.vtkRenderer()
    ren4.AddActor(outlineactor)
    ren4.SetBackground(0.5,0,0)
    ren4.SetViewport(0.5,0.5,1.0,1.0)
    
    renWin=vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.AddRenderer(ren2)
    renWin.AddRenderer(ren3)
    renWin.AddRenderer(ren4)
    renWin.SetSize(640,480)
    renWin.Render() 
    renWin.SetWindowName("Viewport")
    
    
    iren=vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()
    
if __name__ == "__main__":
    main()