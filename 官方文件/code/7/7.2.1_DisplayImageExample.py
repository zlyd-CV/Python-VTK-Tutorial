import vtk

def main():

    imagefilename = "../data/head.mhd"
    mhd_reader  = vtk.vtkMetaImageReader()
    mhd_reader.SetFileName(imagefilename)
    mhd_reader.Update()

    imageviewer = vtk.vtkImageViewer2()
    imageviewer.SetInputConnection(mhd_reader.GetOutputPort())
    iren = vtk.vtkRenderWindowInteractor()
    imageviewer.SetupInteractor(iren)
    imageviewer.SetSize(500,500)

    imageviewer.SetColorLevel(500)
    imageviewer.SetColorWindow(2000)
    imageviewer.SetSlice(30)
    #imageviewer.SetSliceOrientationToXY()
    imageviewer.SetSliceOrientationToYZ()
    #imageviewer.SetSliceOrientationToXZ()
    imageviewer.Render()
    iren.Start()

if __name__ == '__main__':
    main()