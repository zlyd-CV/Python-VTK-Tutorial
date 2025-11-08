import vtk

def main():

    reader =vtk.vtkPolyDataReader()
    reader.SetFileName("../data/fran_cut.vtk")
    reader.Update()

    points =vtk.vtkPolyData()
    points.SetPoints(reader.GetOutput().GetPoints())
    print(points)

    surf =vtk.vtkSurfaceReconstructionFilter()
    surf.SetInputData(points)
    surf.SetNeighborhoodSize(20)
    surf.SetSampleSpacing(0.005)
    surf.Update()

    contour =vtk.vtkContourFilter()
    contour.SetInputConnection(surf.GetOutputPort())
    contour.SetValue(0, 0.0)
    contour.Update()

    leftViewport = [0.0, 0.0, 0.5, 1.0]
    rightViewport = [0.5, 0.0, 1.0, 1.0]

    vertexGlyphFilter =vtk.vtkVertexGlyphFilter()
    vertexGlyphFilter.AddInputData(points)
    vertexGlyphFilter.Update()

    vertexMapper =vtk.vtkPolyDataMapper()
    vertexMapper.SetInputData(vertexGlyphFilter.GetOutput())
    vertexMapper.ScalarVisibilityOff()

    vertexActor =vtk.vtkActor()
    vertexActor.SetMapper(vertexMapper)
    vertexActor.GetProperty().SetColor(0.0, 0.0, 1.0)

    vertexRenderer =vtk.vtkRenderer()
    vertexRenderer.AddActor(vertexActor)
    vertexRenderer.SetViewport(leftViewport)
    vertexRenderer.SetBackground(1, 1, 1)

    surfMapper =vtk.vtkPolyDataMapper()
    surfMapper.SetInputData(contour.GetOutput())
    surfMapper.ScalarVisibilityOff()

    surfActor =vtk.vtkActor()
    surfActor.SetMapper(surfMapper)
    surfActor.GetProperty().SetColor(1.0, 0.2, 0.0)

    surfRenderer =vtk.vtkRenderer ()
    surfRenderer.AddActor(surfActor)
    surfRenderer.SetViewport(rightViewport)
    surfRenderer.SetBackground(0.0, 0.0, 0.0)

    renWin =vtk.vtkRenderWindow()
    renWin.AddRenderer(surfRenderer)
    renWin.AddRenderer(vertexRenderer)
    renWin.SetSize(640, 320)
    renWin.Render()
    renWin.SetWindowName("PolyDataSurfaceReconstruction")

    iren =vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renWin.Render()
    iren.Start()

if __name__ == "__main__":
    main()