import vtk
import os
def main():


    PNGfiles = os.listdir("../data/RCT/")
    print(PNGfiles)

    reader = vtk.vtkPNGReader()
    reader.SetFilePrefix("../data/RCT/T1_")
    reader.SetFilePattern("%s%02d.png")
    reader.SetDataExtent(0,255,0,255,0,75)
    reader.SetDataSpacing(1,1,3)
    print(reader)
    reader.Update()

    style = vtk.vtkInteractorStyleImage()
    imageViewer = vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort())

    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetInteractorStyle(style)

    imageViewer.SetSlice(50)
    #imageViewer.SetSliceOrientationToXY()
    #imageViewer.SetSliceOrientationToYZ()
    imageViewer.SetSliceOrientationToXZ()

    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().SetBackground(0.0, 0.0, 0.0)
    imageViewer.SetSize(512, 512)
    imageViewer.GetRenderWindow().SetWindowName("ReadSeriesPNG")

    renderWindowInteractor.Start();

if __name__ == "__main__":
    main()