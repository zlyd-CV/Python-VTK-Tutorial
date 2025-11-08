import vtk

def main():

    reader =vtk.vtkBMPReader()
    reader.SetFileName ("../data/CT.bmp")
    reader.Update()

    dims = []
    origin = []
    spaceing = []

    dims.append(reader.GetOutput().GetDimensions())
    print("图像维数："+str(dims[0]))
    origin.append(reader.GetOutput().GetOrigin())
    print("图像原点："+str(origin[0]))
    spaceing.append(reader.GetOutput().GetSpacing())
    print("像素间隔："+str(spaceing[0]))
    print("\t")

    changer =vtk.vtkImageChangeInformation()
    changer.SetInputConnection(reader.GetOutputPort())
    changer.SetOutputOrigin(100, 100, 0)
    changer.SetOutputSpacing(5,5,1)
    changer.SetCenterImage(1)
    changer.Update();
    
    dims.append(changer.GetOutput().GetDimensions())
    print("图像维数："+str(dims[1]))
    origin.append(changer.GetOutput().GetOrigin())
    print("图像原点："+str(origin[1]))
    spaceing.append(changer.GetOutput().GetSpacing())
    print("像素间隔："+str(spaceing[1]))

    imageViewer =vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(changer.GetOutputPort())
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()
    imageViewer.Render()

    imageViewer.GetRenderer().SetBackground(1.0, 1.0, 1.0)
    imageViewer.SetSize(480, 360)
    imageViewer.GetRenderWindow().SetWindowName("ImageChangeInformation")

    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()