import vtk

def main():

    reader1=vtk.vtkPNGReader()
    reader1.SetFileName("../data/PET.png")

    pad1 = vtk.vtkImageWrapPad()
    pad1.SetInputConnection(reader1.GetOutputPort())
    pad1.SetOutputWholeExtent(0,511,0,511,0,0)
    
    reader2 =vtk.vtkPNGReader()
    reader2.SetFileName ("../data/PET_Gaussian.png")
    
    pad2 = vtk.vtkImageWrapPad()
    pad2.SetInputConnection(reader2.GetOutputPort())
    pad2.SetOutputWholeExtent(0,511,0,511,0,0)
    
    checker = vtk.vtkImageCheckerboard()
    checker.SetInputConnection(0, pad1.GetOutputPort())
    checker.SetInputConnection(1, pad2.GetOutputPort())
    checker.SetNumberOfDivisions(2, 2, 1)
    
    checkerActor = vtk.vtkImageActor()
    checkerActor.GetMapper().SetInputConnection(checker.GetOutputPort())
    
    rep = vtk.vtkCheckerboardRepresentation()
    rep.SetImageActor(checkerActor)
    rep.SetCheckerboard(checker)
    
    ren = vtk.vtkRenderer()
    renWin =vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetWindowName("Checkerboard Widget")
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    checkerWidget= vtk.vtkCheckerboardWidget()
    checkerWidget.SetInteractor(iren)
    checkerWidget.SetRepresentation(rep)
    
    ren.AddActor(checkerActor)
    renWin.SetSize(500, 500)
    iren.Initialize()
    renWin.Render()
    checkerWidget.On()
    iren.Start()

if __name__ == '__main__':
    main()