import vtk

def main():
    reader=vtk.vtkDICOMImageReader()
    reader.SetFileName("../data/CT_head.dcm")

    imageviewer = vtk.vtkImageViewer2()
    imageviewer.SetInputConnection(reader.GetOutputPort())
    iren = vtk.vtkRenderWindowInteractor()
    imageviewer.SetupInteractor(iren)
    imageviewer.SetSize(500,500)
    imageviewer.GetRenderer().ResetCamera()
    imageviewer.Render()
    imageviewer.GetRenderWindow().SetWindowName("vtkAngleWidget")

    rep = vtk.vtkDistanceRepresentation2D()
    rep.GetAxis().SetNumberOfMinorTicks(4)
    rep.GetAxis().SetTickLength(9)
    rep.GetAxis().SetTitlePosition(0.2)

    widget = vtk.vtkAngleWidget()
    widget.SetInteractor(iren)
    widget.CreateDefaultRepresentation()
    widget.ManagesCursorOn()
    widget.On()

    iren.Start()
if __name__ == "__main__":
    main()