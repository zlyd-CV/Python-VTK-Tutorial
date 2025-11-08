import math
import sys
import vtk

def main():
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.SetBackground(0.0,0.0,1.0)
    renWin.SetSize(600, 600)

    contourRep = vtk.vtkOrientedGlyphContourRepresentation()
    contourRep.GetLinesProperty().SetColor(1.0, 0.3, 0.3)

    contourWidget = vtk.vtkContourWidget()
    contourWidget.SetInteractor(iren)
    contourWidget.SetRepresentation(contourRep)
    contourWidget.On()

    for arg in sys.argv:
        if "-Shift" == arg:
            contourWidget.GetEventTranslator().RemoveTranslation(
                vtk.vtkCommand.LeftButtonPressEvent)
            contourWidget.GetEventTranslator().SetTranslation(
                vtk.vtkCommand.LeftButtonPressEvent,
                vtk.vtkWidgetEvent.Translate)
        elif "-Scale" == arg:
            contourWidget.GetEventTranslator().RemoveTranslation(
                vtk.vtkCommand.LeftButtonPressEvent)
            contourWidget.GetEventTranslator().SetTranslation(
                vtk.vtkCommand.LeftButtonPressEvent,
                vtk.vtkWidgetEvent.Scale)

    pd = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    num_pts = 21
    for i in range(0, num_pts):
        angle = 2.0 * math.pi * i / 20.0
        points.InsertPoint(i, 0.1 * math.cos(angle),
                           0.1 * math.sin(angle), 0.0)

    vertex_indices = list(range(0, num_pts))
    vertex_indices.append(0)
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(num_pts + 1, vertex_indices)
    pd.SetPoints(points)
    pd.SetLines(lines)

    contourWidget.Initialize(pd, 1)
    contourWidget.Render()
    ren.ResetCamera()
    renWin.Render()
    iren.Initialize()
    iren.Start()
if __name__ == '__main__':
    main()