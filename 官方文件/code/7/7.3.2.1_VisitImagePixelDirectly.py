import vtk

def main():

    reader = vtk.vtkPNGReader()
    reader.SetFileName("../data/PET.png")
    reader.Update()

    dims = ()
    dims = reader.GetOutput().GetDimensions()
    nbOfComp = []
    nbOfComp.append(reader.GetOutput().GetNumberOfScalarComponents())

    for k in range(dims[2]):
        for j in range(dims[1]):
            for i in range(dims[0]):
                if(i<100) and (j<100):
                     reader.GetOutput().SetScalarComponentFromFloat(i, j, k, 0, 255)
                     reader.GetOutput().SetScalarComponentFromFloat(i, j, k, 1, 0)
                     reader.GetOutput().SetScalarComponentFromFloat(i, j, k, 2, 0)

    imageViewer = vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort())

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    imageViewer.SetupInteractor(renderWindowInteractor)
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()
    imageViewer.Render()

    imageViewer.GetRenderer().SetBackground(1.0, 1.0, 1.0)
    imageViewer.SetSize(640, 480)
    imageViewer.GetRenderWindow().SetWindowName("VisitImagePixelDirectly")


    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
