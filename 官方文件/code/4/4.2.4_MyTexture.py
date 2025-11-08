import vtk 

def main():
    reader=vtk.vtkBMPReader()                            #读取BMP格式图像
    reader.SetFileName("../data/wins.bmp")
    
    texture=vtk.vtkTexture()                             #生成纹理类对象
    texture.SetInputConnection(reader.GetOutputPort())
    texture.InterpolateOn()
    
    cylinder=vtk.vtkCylinderSource()                     #生成一个柱状体  
    cylinder.SetHeight(4.0)
    cylinder.SetRadius(1.0)
    cylinder.SetResolution(6)
    
    Mapper =vtk.vtkPolyDataMapper()                      #生成一个多边形数据映射
    Mapper.SetInputConnection(cylinder.GetOutputPort())
    
    actor=vtk.vtkActor()
    actor.SetMapper( Mapper )
    actor.SetTexture(texture)

    renderer=vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1.0,1.0,1.0)

    renWin=vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(480,480)
    renWin.Render()
    renWin.SetWindowName("MyTexture")

    iren=vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    style = vtk.vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)
    
    iren.Initialize()
    iren.Start()
    
if __name__ == "__main__":
    main()