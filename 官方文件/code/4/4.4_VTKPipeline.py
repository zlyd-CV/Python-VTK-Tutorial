import vtk

def main():
    fileName = "../data/head.vtk"
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(fileName)

    mc=vtk.vtkMarchingCubes()
    mc.SetInputConnection(reader.GetOutputPort())
    mc.SetValue(0,500)
    
    mcmapper=vtk.vtkPolyDataMapper()
    mcmapper.SetInputConnection(mc.GetOutputPort())
    mcmapper.ScalarVisibilityOff()  
    
    mcactor=vtk.vtkActor()
    mcactor.SetMapper(mcmapper)
    
    ren1 = vtk.vtkRenderer()
    ren1.AddActor(mcactor)
    ren1.SetBackground(1,1,1)
    ren1.ResetCamera()
    
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(500, 500)  
    renWin.Render()
    renWin.SetWindowName("VTK Pipeline") 
   
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Start()    

if __name__ == '__main__':
    main() 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    