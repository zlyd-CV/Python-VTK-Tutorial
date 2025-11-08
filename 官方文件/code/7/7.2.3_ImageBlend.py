import vtk

def main():
    img = vtk.vtkPNGReader()
    img.SetFileName("../data/PET.png")

    canvas = vtk.vtkImageCanvasSource2D()
    canvas.SetScalarTypeToUnsignedChar()
    canvas.SetExtent(0,300,0,300,0,0)
    canvas.SetDrawColor(0.0)
    canvas.FillBox(0,300,0,300)
    canvas.SetDrawColor(255.0)
    canvas.FillBox(50,150,50,150)

    img_blender = vtk.vtkImageBlend()
    img_blender.AddInputConnection(img.GetOutputPort())
    img_blender.AddInputConnection(canvas.GetOutputPort())
    img_blender.SetOpacity(0, 0.5)
    img_blender.SetOpacity(1, 0.5)
    img_blender.Update()

    img_actor = vtk.vtkImageActor()
    img_actor.SetInputData(img_blender.GetOutput())

    renderer = vtk.vtkRenderer()
    renderer.AddActor(img_actor)
    renderer.ResetCamera()
    renderer.SetBackground(0.7,0.7,0.7)

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(renderer)  
    renwin.SetSize(400,400)
    renwin.Render()
    renwin.SetWindowName("vtkImageBlend")

    style = vtk.vtkInteractorStyleImage()
    rwi = vtk.vtkRenderWindowInteractor()
    rwi.SetInteractorStyle(style)
    rwi.SetRenderWindow(renwin)

    rwi.Initialize()
    rwi.Start()

if __name__ == '__main__':
    main()