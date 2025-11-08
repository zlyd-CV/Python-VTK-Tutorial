import vtk

def main():
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName("../data/CT/")
    reader.SetDataExtent(0,511,0,511,0,116)
    reader.Update()


    imageViewer = vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort())

    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()
    renderWindowInteractor.SetInteractorStyle(style)

    imageViewer.SetSlice(30)
    imageViewer.SetSliceOrientationToXY()
    #imageViewer.SetSliceOrientationToYZ()
    #imageViewer.SetSliceOrientationToXZ()

    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().SetBackground(0.0, 0.0, 0.0)
    imageViewer.SetSize(600, 600)
    imageViewer.GetRenderWindow().SetWindowName("ReadSeriesCT")
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()