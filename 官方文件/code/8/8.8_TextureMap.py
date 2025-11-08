import vtk


def main():

    translate = [10.0,0.0,0.0]
    texReader =vtk.vtkBMPReader()
    texReader.SetFileName("../data/CT.bmp")

    texture =vtk.vtkTexture()
    texture.SetInputConnection(texReader.GetOutputPort())

    modelReader =vtk.vtkXMLPolyDataReader()
    modelReader.SetFileName("../data/cow.vtp")

    texturemap =vtk.vtkTextureMapToCylinder()
    texturemap.SetInputConnection(modelReader.GetOutputPort())

    mapper =vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(texturemap.GetOutputPort())

    actor =vtk.vtkActor()
    actor.SetMapper( mapper )
    actor.SetTexture( texture )

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1.0, 1.0, 1.0)

    renderWindow =vtk.vtkRenderWindow()
    renderWindow.AddRenderer( renderer )

    renWinInteractor =vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow( renderWindow )

    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName("TextureMap")
    renderWindow.Render()
    renderWindow.Render()
    renWinInteractor.Start()

if __name__ == '__main__':
    main()