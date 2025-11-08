import vtk

class CellPickerInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.polyData = vtk.vtkPolyData()
        self.selectedMapper = vtk.vtkDataSetMapper()
        self.selectedActor = vtk.vtkActor()

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.0005)
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        picked = picker.GetPickPosition()
        print(picked)

        if(picker.GetCellId() != -1):
            ids = vtk.vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(picker.GetCellId())

            selectionNode = vtk.vtkSelectionNode()
            selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
            selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
            selectionNode.SetSelectionList(ids)

            selection = vtk.vtkSelection()
            selection.AddNode(selectionNode)

            extractSelection = vtk.vtkExtractSelection()
            extractSelection.SetInputData(0, self.polyData)
            extractSelection.SetInputData(1, selection)
            extractSelection.Update();

            self.selectedMapper.SetInputConnection(extractSelection.GetOutputPort())
            self.selectedActor.SetMapper(self.selectedMapper);
            self.selectedActor.GetProperty().EdgeVisibilityOn();
            self.selectedActor.GetProperty().SetEdgeColor(1,0,0);
            self.selectedActor.GetProperty().SetLineWidth(3);
            self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(self.selectedActor)

        self.OnLeftButtonDown()
        return
def main():
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetPhiResolution(10)
    sphereSource.SetThetaResolution(10)
    sphereSource.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.0,0.5,1.0)

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.Render()
    renWin.SetWindowName("Cell Picker")
    renWin.AddRenderer(ren)
    renWin.SetSize(500,500)

    pointPicker = vtk.vtkPointPicker()

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetPicker(pointPicker)
    iren.SetRenderWindow(renWin)

    style = CellPickerInteractorStyle()
    style.SetDefaultRenderer(ren)
    style.polyData = sphereSource.GetOutput()
    iren.SetInteractorStyle( style )

    ren.AddActor(actor)
    ren.SetBackground(1.0,1.0,1.0)
    iren.Start()
if __name__ == '__main__':
    main()