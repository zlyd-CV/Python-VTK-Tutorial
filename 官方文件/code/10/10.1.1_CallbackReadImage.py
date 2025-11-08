import vtk

pressCounts = 0
def myCallback(obj, event):
    global pressCounts
    pressCounts = pressCounts + 1
    print("You have clicked:"+ str(pressCounts) + " times")

def main():
    reader = vtk.vtkPNGReader()
    reader.SetFileName('../data/vtk.PNG')

    viewer = vtk.vtkImageViewer2()
    viewer.SetInputConnection(reader.GetOutputPort())
    viewer.SetSize(500,500)
    viewer.GetRenderer().ResetCamera()

    iren = vtk.vtkRenderWindowInteractor()
    viewer.SetupInteractor(iren)
    viewer.Render()
    viewer.GetRenderWindow().SetWindowName("CallbackReadSImage")

    iren.SetRenderWindow(viewer.GetRenderWindow())
    iren.AddObserver('LeftButtonPressEvent', myCallback)

    iren.Initialize()
    iren.Start()
if __name__ == "__main__":
    main()