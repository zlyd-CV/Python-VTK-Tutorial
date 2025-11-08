import vtk
import random


def main():
    img_size = 500
    x_size = img_size
    y_size = img_size
    z_size = 1

    img = vtk.vtkImageData()
    info = img.GetInformation()
    img.SetDimensions(x_size, y_size, z_size)
    img.SetNumberOfScalarComponents(1, info)
    img.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 3)

    for x in range(x_size):
        for y in range(y_size):
                img.SetScalarComponentFromFloat(x, y, 0,0, (x/x_size)*255)  # red
                img.SetScalarComponentFromFloat(x, y, 0, 1, (y/y_size)*255)  # green
                img.SetScalarComponentFromFloat(x, y, 0, 2, 125)  # blue

    img.Modified()

    img_mapper = vtk.vtkImageMapper()
    img_mapper.SetInputData(img)
    img_mapper.SetColorWindow(256)
    img_mapper.SetColorLevel(125)

    redActor = vtk.vtkActor2D()
    redActor.SetMapper(img_mapper)
    redViewport = [0.0, 0.0, 1.0, 1.0]

    redRenderer = vtk.vtkRenderer()
    redRenderer.SetViewport(redViewport)
    redRenderer.AddActor(redActor)
    redRenderer.ResetCamera()
    redRenderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(redRenderer)
    renderWindow.SetSize(x_size, y_size)
    renderWindow.Render()
    renderWindow.SetWindowName("CreateVTKImageData")

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()
    renderWindowInteractor.SetInteractorStyle(style)

    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
