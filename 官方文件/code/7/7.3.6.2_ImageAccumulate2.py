import vtk

def main():
    reader = vtk.vtkJPEGReader()
    reader.SetFileName ("../data/lena.jpg")
    reader.Update()

    numComponents = reader.GetOutput().GetNumberOfScalarComponents()
    print(numComponents)

    plot =vtk.vtkXYPlotActor()
    plot.ExchangeAxesOff()
    plot.SetLabelFormat( "%g" )
    plot.SetXTitle( "Intensity" )
    plot.SetYTitle( "Frequency" )
    plot.SetXValuesToValue()
    plot.GetProperty().SetColor(0.0, 0.0, 0.0)
    plot.GetAxisLabelTextProperty().SetColor(0.0, 0.0, 0.0)
    plot.GetAxisTitleTextProperty().SetColor(0.0, 0.0, 0.0)


    colors = [[ 1, 0, 0 ],[ 0, 1, 0 ],[ 0, 0, 1 ]]

    labels = ["Red", "Green", "Blue"]

    xmax = 0
    ymax = 0

    for i in range(numComponents):
        extract = vtk.vtkImageExtractComponents()
        extract.SetInputConnection( reader.GetOutputPort() )
        extract.SetComponents( i )
        extract.Update()

        Myrange =extract.GetOutput().GetScalarRange()

        extent = int(Myrange[1])-int(Myrange[0])-1

        histogram =vtk.vtkImageAccumulate()
        histogram.SetInputConnection( extract.GetOutputPort() )
        histogram.SetComponentExtent( 0,extent, 0,0, 0,0)
        histogram.SetComponentOrigin( Myrange[0],0,0 )
        histogram.SetComponentSpacing( 1,0,0 )
        histogram.SetIgnoreZero( 1 )
        histogram.Update()

        if(Myrange[1] > xmax ):
            xmax = Myrange[1]

        if( histogram.GetOutput().GetScalarRange()[1] > ymax ):
            ymax = histogram.GetOutput().GetScalarRange()[1]

        plot.AddDataSetInput(histogram.GetOutput())
        plot.SetPlotColor(i,colors[i])
        plot.SetPlotLabel(i,labels[i])
        plot.LegendOn()

    plot.SetXRange( 0, xmax)
    plot.SetYRange( 0, ymax)

    renderer =vtk.vtkRenderer()
    renderer.AddActor(plot)
    renderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer( renderer )
    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName("ImageAccumulate2")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow( renderWindow )
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()