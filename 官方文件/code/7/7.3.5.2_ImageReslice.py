import vtk

def main():

    reader = vtk.vtkMetaImageReader()
    reader.SetFileName("../data/brain.mhd")
    reader.Update()

    extent = (0,0,0,0,0,0)
    spacing =(0,0,0)
    origin = (0,0,0)

    extent =reader.GetOutput().GetExtent()
    spacing = reader.GetOutput().GetSpacing()
    origin = reader.GetOutput().GetOrigin()
    print(extent,spacing,origin)

    center = [0,0,0]
    center[0] = origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1]);
    center[1] = origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3]);
    center[2] = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5]);

    #print(center)

    axialElements = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)

    resliceAxes = vtk.vtkMatrix4x4()
    resliceAxes.DeepCopy(axialElements);
    resliceAxes.SetElement(0, 3, center[0])
    resliceAxes.SetElement(1, 3, center[1])
    resliceAxes.SetElement(2, 3, center[2])


    reslice = vtk.vtkImageReslice()
    reslice.SetInputConnection(reader.GetOutputPort())
    reslice.SetOutputDimensionality(2)
    reslice.SetResliceAxes(resliceAxes)
    reslice.SetInterpolationModeToLinear()

    colorTable = vtk.vtkLookupTable()
    colorTable.SetRange(0, 1000)
    colorTable.SetValueRange(0.0, 1.0)
    colorTable.SetSaturationRange(0.0, 0.0)
    colorTable.SetRampToLinear()
    colorTable.Build()


    colorMap =vtk.vtkImageMapToColors()
    colorMap.SetLookupTable(colorTable)
    colorMap.SetInputConnection(reslice.GetOutputPort())
    colorMap.Update()

    imgActor =vtk.vtkImageActor()
    imgActor.SetInputData(colorMap.GetOutput())

    renderer = vtk.vtkRenderer()
    renderer.AddActor(imgActor)
    renderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.Render()
    renderWindow.SetSize(640, 480)
    renderWindow.SetWindowName("ImageReslice")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()

    renderWindowInteractor.SetInteractorStyle(style)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()