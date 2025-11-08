import vtk

def main():

    imagefilename = "../data/PET.png"
    png_reader  = vtk.vtkPNGReader()
    png_reader.SetFileName(imagefilename)
    png_reader.Update()

    actor = vtk.vtkImageActor()
    actor.SetInputData(png_reader.GetOutput())

    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(500,500)
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetWindowName("vtkImageActor")
         
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    style = vtk.vtkInteractorStyleImage()
    iren.SetInteractorStyle(style)
    iren.Initialize()
    iren.Start()

if __name__ == '__main__':
    main()