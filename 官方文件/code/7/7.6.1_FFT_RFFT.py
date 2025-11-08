import vtk

def main():
    reader=vtk.vtkPNGReader()
    reader.SetFileName("../data/PET.png")
    reader.Update()

    fftFilter=vtk.vtkImageFFT()
    fftFilter.SetInputConnection(reader.GetOutputPort())
    fftFilter.SetDimensionality(2)
    fftFilter.Update()

    fftExtractReal=vtk.vtkImageExtractComponents()
    fftExtractReal.SetInputConnection(fftFilter.GetOutputPort())
    fftExtractReal.SetComponents(0)
    fftExtractReal.Update()
 
    rfftFilter=vtk.vtkImageRFFT()
    rfftFilter.SetInputConnection(fftFilter.GetOutputPort())
    rfftFilter.SetDimensionality(2)
    rfftFilter.Update()
    
    ifftExtractReal=vtk.vtkImageExtractComponents()
    ifftExtractReal.SetInputConnection(rfftFilter.GetOutputPort())
    ifftExtractReal.SetComponents(0)
    ifftExtractReal.Update()

    originalActor=vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())
    
    FFTActor = vtk.vtkImageActor()
    FFTActor.SetInputData(fftExtractReal.GetOutput())
    
    erodedActor=vtk.vtkImageActor()
    erodedActor.SetInputData(ifftExtractReal.GetOutput())

    leftViewport= [0.0, 0.0, 0.33, 1.0]
    medianViewport= [0.33, 0.0, 0.66, 1.0]
    rightViewport= [0.66, 0.0, 1.0, 1.0]

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.SetSize(640,320)
    renderWindow.Render()
    renderWindow.SetWindowName("FFT_RFFT")

    interactor=vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    leftRenderer=vtk.vtkRenderer()
    renderWindow.AddRenderer(leftRenderer)
    leftRenderer.SetViewport(leftViewport)
    leftRenderer.SetBackground(1.0, 1.0, 1.0)
    
    medianRenderer=vtk.vtkRenderer()
    renderWindow.AddRenderer(medianRenderer)
    medianRenderer.SetViewport(medianViewport)
    medianRenderer.SetBackground(1.0, 1.0, 1.0)

    rightRenderer=vtk.vtkRenderer()
    renderWindow.AddRenderer(rightRenderer)
    rightRenderer.SetViewport(rightViewport)
    rightRenderer.SetBackground(1.0, 1.0, 1.0)

    leftRenderer.AddActor(originalActor)
    medianRenderer.AddActor(FFTActor)
    rightRenderer.AddActor(erodedActor)

    renderWindow.Render()
    interactor.Start()

if __name__ == "__main__":
    main()











