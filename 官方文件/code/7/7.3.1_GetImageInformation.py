import vtk

def main():

    reader =vtk.vtkBMPReader()
    reader.SetFileName ("../data/CT.bmp")
    reader.Update()

    dims = []
    dims.append(reader.GetOutput().GetDimensions())
    print("图像维数："+str(dims))

    origin = []
    origin.append(reader.GetOutput().GetOrigin())
    print("图像原点："+str(origin))

    spaceing = []
    spaceing.append(reader.GetOutput().GetSpacing())
    print("像素间隔："+str(spaceing))

    imageViewer =vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort());

    renderWindowInteractor =vtk.vtkRenderWindowInteractor()
    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()
    imageViewer.Render()

    imageViewer.GetRenderer().SetBackground(1.0, 1.0, 1.0)
    imageViewer.SetSize(480, 360)
    imageViewer.GetRenderWindow().SetWindowName("GetImageInformation")

    renderWindowInteractor.Start();

if __name__ == "__main__":
    main()

