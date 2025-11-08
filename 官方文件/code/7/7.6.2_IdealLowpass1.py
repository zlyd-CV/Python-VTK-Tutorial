import vtk

def main():
    reader=vtk.vtkPNGReader()
    reader.SetFileName("../data/PET.png")
    reader.Update()

    fftFilter=vtk.vtkImageFFT()
    fftFilter.SetInputConnection(reader.GetOutputPort())
    fftFilter.Update()

    lowPassFilter=vtk.vtkImageIdealLowPass()
    lowPassFilter.SetInputConnection(fftFilter.GetOutputPort())
    lowPassFilter.SetXCutOff(0.05)
    lowPassFilter.SetYCutOff(0.05)
    lowPassFilter.Update()

    rfftFilter=vtk.vtkImageRFFT()
    rfftFilter.SetInputConnection(lowPassFilter.GetOutputPort())
    rfftFilter.Update()

    ifftExtractReal=vtk.vtkImageExtractComponents()
    ifftExtractReal.SetInputConnection(rfftFilter.GetOutputPort())
    ifftExtractReal.SetComponents(0)

    CastFilter=vtk.vtkImageCast()
    CastFilter.SetInputConnection(ifftExtractReal.GetOutputPort())
    CastFilter.SetOutputScalarTypeToUnsignedChar()
    CastFilter.Update()

    originalActor=vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    erodedActor=vtk.vtkImageActor()
    erodedActor.SetInputData(CastFilter.GetOutput())

    leftViewport= [0.0, 0.0, 0.5, 1.0]
    rightViewport= [0.5, 0.0, 1.0, 1.0]

    renderWindow=vtk.vtkRenderWindow()
    renderWindow.SetSize(640,320)
    renderWindow.Render()
    renderWindow.SetWindowName("IdealLowPass")

    interactor=vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    leftRenderer=vtk.vtkRenderer()
    renderWindow.AddRenderer(leftRenderer)
    leftRenderer.SetViewport(leftViewport)
    leftRenderer.SetBackground(1.0, 1.0, 1.0)

    rightRenderer=vtk.vtkRenderer()
    renderWindow.AddRenderer(rightRenderer)
    rightRenderer.SetViewport(rightViewport)
    rightRenderer.SetBackground(1.0, 1.0, 1.0)

    leftRenderer.AddActor(originalActor)
    rightRenderer.AddActor(erodedActor)

    leftRenderer.ResetCamera()
    rightRenderer.ResetCamera()

    renderWindow.Render()
    interactor.Start()

if __name__ == "__main__":
    main()











