import vtk

def main(): 
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName("../data/mummy.128.vtk")

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(70, 0.00)
    opacityTransferFunction.AddPoint(90, 0.40)
    opacityTransferFunction.AddPoint(180, 0.60)    
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.52, 0.30)
    colorTransferFunction.AddRGBPoint(190.0, 1.0, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(220.0, 0.20, 0.20, 0.20)
    volumeProperty.SetColor(colorTransferFunction)

    hiresMapper =vtk.vtkGPUVolumeRayCastMapper()
    hiresMapper.SetInputConnection(reader.GetOutputPort())
    hiresMapper.SetAutoAdjustSampleDistances(0)  #关闭自动调整功能
    
    lowresMapper =vtk.vtkGPUVolumeRayCastMapper()
    lowresMapper.SetInputConnection(reader.GetOutputPort())
    lowresMapper.SetAutoAdjustSampleDistances(0)

    lowresMapper.SetSampleDistance(10 * hiresMapper.GetSampleDistance())
    lowresMapper.SetImageSampleDistance(10 * hiresMapper.GetImageSampleDistance())

    prop = vtk.vtkLODProp3D()
    prop.AddLOD(lowresMapper, volumeProperty, 0.0)
    prop.AddLOD(hiresMapper, volumeProperty, 0.0)
    
    volume = vtk.vtkVolume()
    volume.SetMapper(hiresMapper)
    volume.SetProperty(volumeProperty)
    
    volumeView = (0, 0, 0.5, 1)
    lodpropView = ( 0.5, 0, 1, 1)
    
    volumeren = vtk.vtkRenderer()
    volumeren.SetBackground(0.7, 0.7, 0.7)
    volumeren.AddVolume(volume)
    volumeren.SetViewport(volumeView)
    
    propren = vtk.vtkRenderer()
    propren.SetBackground(0.9, 0.9, 0.9)
    propren.AddVolume(prop)
    propren.SetViewport(lodpropView)
    
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(volumeren)
    renWin.AddRenderer(propren)
    renWin.SetSize(640,320)
    renWin.Render()
    renWin.SetWindowName("vtkLODProp3D")
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Start()
if __name__ == '__main__':
        main()
    
