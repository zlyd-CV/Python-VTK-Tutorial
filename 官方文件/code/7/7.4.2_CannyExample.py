import vtk

def main():
    reader = vtk.vtkPNGReader()
    reader.SetFileName("../data/CT_head.png")
    reader.Update()

    il = vtk.vtkImageLuminance()
    il.SetInputConnection(reader.GetOutputPort())
    il.Update()

    ic =vtk.vtkImageCast()
    ic.SetOutputScalarTypeToFloat()
    ic.SetInputConnection(il.GetOutputPort())
    ic.Update()

    gs =vtk.vtkImageGaussianSmooth()
    gs.SetInputConnection(ic.GetOutputPort())
    gs.SetDimensionality(2)
    gs.SetRadiusFactors(1, 1, 0)
    gs.Update()

    imgGradient =vtk.vtkImageGradient()
    imgGradient.SetInputConnection(gs.GetOutputPort())
    imgGradient.SetDimensionality(2)
    imgGradient.Update()

    imgMagnitude =vtk.vtkImageMagnitude()
    imgMagnitude.SetInputConnection(imgGradient.GetOutputPort())
    imgMagnitude.Update()

    nonMax =vtk.vtkImageNonMaximumSuppression()
    nonMax.SetMagnitudeInputData(imgMagnitude.GetOutput())
    nonMax.SetVectorInputData(imgGradient.GetOutput())
    nonMax.SetDimensionality(2)
    nonMax.Update()

    pad =vtk.vtkImageConstantPad()
    pad.SetInputConnection(imgGradient.GetOutputPort())
    pad.SetOutputNumberOfScalarComponents(3)
    pad.SetConstant(0)
    pad.Update()

    i2sp1 =vtk.vtkImageToStructuredPoints()
    i2sp1.SetInputConnection(nonMax.GetOutputPort())
    i2sp1.SetVectorInputData(pad.GetOutput())
    i2sp1.Update()

    imgLink =vtk.vtkLinkEdgels()
    imgLink.SetInputData(i2sp1.GetOutput())
    imgLink.SetGradientThreshold(2)

    thresholdEdgels =vtk.vtkThreshold()
    thresholdEdgels.SetInputConnection(imgLink.GetOutputPort())
    thresholdEdgels.ThresholdByUpper(10)
    thresholdEdgels.AllScalarsOff()

    gf =vtk.vtkGeometryFilter()
    gf.SetInputConnection(thresholdEdgels.GetOutputPort())
    gf.Update()

    i2sp = vtk.vtkImageToStructuredPoints()
    i2sp.SetInputConnection(imgMagnitude.GetOutputPort())
    i2sp.SetVectorInputData(pad.GetOutput())
    i2sp.Update()

    spe = vtk.vtkSubPixelPositionEdgels()
    spe.SetInputConnection(gf.GetOutputPort())
    spe.SetGradMapsData(i2sp.GetStructuredPointsOutput())

    strip =vtk.vtkStripper()
    strip.SetInputConnection(spe.GetOutputPort())

    dsm =vtk.vtkPolyDataMapper()
    dsm.SetInputConnection(strip.GetOutputPort())
    dsm.ScalarVisibilityOff()

    planeActor =vtk.vtkActor()
    planeActor.SetMapper(dsm)
    planeActor.GetProperty().SetAmbient(1.0)
    planeActor.GetProperty().SetDiffuse(0.0)
    #planeActor.GetProperty().SetColor(1.0, 0.0, 0.0)

    originalActor =vtk.vtkImageActor()
    originalActor.SetInputData(reader.GetOutput())

    originalViewport = (0.0, 0.0, 0.5, 1.0)
    gradviewport = (0.5, 0.0, 1.0, 1.0)

    originalRenderer =vtk.vtkRenderer()
    originalRenderer.SetViewport(originalViewport)
    originalRenderer.AddActor(originalActor)
    originalRenderer.ResetCamera()
    originalRenderer.SetBackground(1.0, 1.0, 1.0)

    gradRenderer =vtk.vtkRenderer()
    gradRenderer.SetViewport(gradviewport)
    gradRenderer.AddActor(planeActor)
    gradRenderer.ResetCamera()
    gradRenderer.SetBackground(0.0, 0.0, 0.0)

    renderWindow =vtk.vtkRenderWindow()
    renderWindow.SetSize(900, 300)
    renderWindow.AddRenderer(originalRenderer)
    renderWindow.AddRenderer(gradRenderer)
    renderWindow.Render()
    renderWindow.SetWindowName("CannyExample")

    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    style =vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()
