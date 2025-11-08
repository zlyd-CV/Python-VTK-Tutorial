import vtk

def main():
     
    reader =vtk.vtkPNGReader()
    reader.SetFileName ("../data/CT_head.png")
    reader.Update()
    
    shiftScaleFilter = vtk.vtkImageShiftScale()
    shiftScaleFilter.SetInputConnection(reader.GetOutputPort())
    shiftScaleFilter.SetOutputScalarTypeToUnsignedChar()
    shiftScaleFilter.SetShift(1)
    shiftScaleFilter.SetScale(255)
    shiftScaleFilter.Update()

    imageViewer =vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(shiftScaleFilter.GetOutputPort())
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()

    imageViewer.GetRenderer().SetBackground(1.0, 1.0, 1.0)
    imageViewer.SetSize(480, 360)
    imageViewer.GetRenderWindow().SetWindowName("ImageShiftScale")

    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()