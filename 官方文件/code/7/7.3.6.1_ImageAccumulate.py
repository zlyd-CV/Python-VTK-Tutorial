import vtk


def main():
    reader = vtk.vtkBMPReader()
    reader.SetFileName ("../data/lena.bmp")
    reader.Update()

    il = vtk.vtkImageLuminance()
    il.SetInputConnection(reader.GetOutputPort())
    il.Update()

    ic =vtk.vtkImageCast()
    ic.SetOutputScalarTypeToFloat()
    ic.SetInputConnection(il.GetOutputPort())
    ic.Update()

    bins   = 16
    comps  = 1

    histogram = vtk.vtkImageAccumulate()
    histogram.SetInputData(ic.GetOutput())
    histogram.SetComponentExtent(0, bins-1, 0, 0, 0, 0)
    histogram.SetComponentOrigin(0, 0, 0)
    histogram.SetComponentSpacing(256.0/bins, 0, 0)
    histogram.Update()


    output =histogram.GetOutput().GetScalarPointer()


    frequencies = vtk.vtkIntArray()
    frequencies.SetNumberOfComponents(1)

    for i in range(bins):
        for j in range(comps):
            output1 =histogram.GetOutput().GetScalarComponentAsDouble(i, j, 0, 0)
            frequencies.InsertNextTuple1(output1)

    #print(frequencies)

    dataObject = vtk.vtkDataObject()
    dataObject.GetFieldData().AddArray( frequencies )

    barChart = vtk.vtkBarChartActor()
    barChart.SetInput(dataObject)
    barChart.SetTitle("Histogram")
    barChart.GetPositionCoordinate().SetValue(0.1,0.1,0.0)
    barChart.GetPosition2Coordinate().SetValue(0.90,0.90,0.0)
    barChart.GetProperty().SetColor(0,0,0)
    barChart.GetTitleTextProperty().SetColor(0,0,0)
    barChart.GetLabelTextProperty().SetColor(0,0,0)
    barChart.GetLegendActor().SetNumberOfEntries(dataObject.GetFieldData().GetArray(0).GetNumberOfTuples())
    barChart.LegendVisibilityOff()
    barChart.LabelVisibilityOff()

    renderer =vtk.vtkRenderer()
    renderer.AddActor(barChart)
    renderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageAccumulate")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()