import vtk

def main():

    reader = vtk.vtkPNGReader()
    reader.SetFileName ("../data/PET.png") 
    
    Filter = vtk.vtkImageLuminance()
    Filter.SetInputConnection(reader.GetOutputPort())
    Filter.Update()
    
    Viewer = vtk.vtkImageViewer2()
    Viewer.SetInputConnection(Filter.GetOutputPort())
    iren = vtk.vtkRenderWindowInteractor()
    Viewer.SetupInteractor(iren)

    Viewer.SetSize(500,500)
    Viewer.GetRenderWindow().SetWindowName("ImageLuminance")
    #Viewer.SetColorLevel(0)
    #Viewer.SetColorWindow(1000)
    Viewer.Render()
    iren.Start()

if __name__ == '__main__':
    main()