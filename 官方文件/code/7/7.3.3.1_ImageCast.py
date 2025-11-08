import vtk

def main():     
    reader =vtk.vtkBMPReader()
    reader.SetFileName ("../data/CT.bmp")
    reader.Update()
    
    imageCast = vtk.vtkImageCast()
    imageCast.SetInputConnection(reader.GetOutputPort())
    imageCast.SetOutputScalarTypeToFloat()
    imageCast.ClampOverflowOn()
    imageCast.Update()

    imageViewer =vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(imageCast.GetOutputPort())
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()

    imageViewer.GetRenderer().SetBackground(1.0, 1.0, 1.0)
    imageViewer.SetSize(480, 360)
    imageViewer.GetRenderWindow().SetWindowName("ImageCast")

    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()