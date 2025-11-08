import vtk

def main():

    imagefilename = "../data/CT.dcm"
    dcm_reader  = vtk.vtkDICOMImageReader()
    dcm_reader.SetFileName(imagefilename)

    imgViewer = vtk.vtkImageViewer2()
    imgViewer.SetInputConnection(dcm_reader.GetOutputPort())
    iren = vtk.vtkRenderWindowInteractor()
    imgViewer.SetupInteractor(iren)

    imgViewer.SetSize(500,500)
    imgViewer.SetColorLevel(500)
    imgViewer.SetColorWindow(2000)
    imgViewer.Render()
    iren.Start()

if __name__ == '__main__':
    main()