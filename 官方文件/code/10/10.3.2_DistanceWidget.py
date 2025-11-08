import vtk

def main():
    reader=vtk.vtkDICOMImageReader()
    reader.SetFileName("../data/CT_head.dcm")
    reader.Update()

    imageViewer = vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort())
    style = vtk.vtkInteractorStyleImage()
    iren =vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(style)

    imageViewer.SetupInteractor(iren)
    imageViewer.Render()
    imageViewer.GetRenderer().SetBackground(0.0, 0.0, 0.0)
    imageViewer.SetSize(600, 600)
    imageViewer.GetRenderWindow().SetWindowName("Distance Widget")

    rep = vtk.vtkDistanceRepresentation2D()
    rep.GetAxis().SetNumberOfMinorTicks(5)
    rep.GetAxis().SetTickLength(9)
    rep.GetAxis().SetTitlePosition(0.2)

    widget = vtk.vtkDistanceWidget()
    widget.SetInteractor(iren)
    widget.CreateDefaultRepresentation()
    widget.SetRepresentation(rep)
    widget.SetPriority(0.9)
    widget.ManagesCursorOn()
    widget.On()
    iren.Start()
if __name__ == '__main__':
    main()