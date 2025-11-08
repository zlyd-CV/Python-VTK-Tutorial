import vtk

def main():
    cone = vtk.vtkConeSource()                          #生成一个锥形体
    cone.SetHeight(2.0)
    cone.SetRadius(1.0)
    cone.SetResolution(8)

    coneMapper = vtk.vtkPolyDataMapper()                #锥形体数据的映射转换 
    coneMapper.SetInputConnection(cone.GetOutputPort())

    coneActor = vtk.vtkActor()                          #生成一个演员
    coneActor.SetMapper(coneMapper)

    ren = vtk.vtkRenderer()                             #生成一个渲染器
    ren.AddActor(coneActor)
    ren.SetBackground(0,0,0)
    
    renWin = vtk.vtkRenderWindow()                      #生成渲染显示的窗口
    renWin.AddRenderer(ren)
    renWin.SetSize(500, 500)
 
    iren = vtk.vtkRenderWindowInteractor()              #生成一个交互器
    iren.SetRenderWindow(renWin)

    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)

    renWin.Render()
    renWin.SetWindowName("Cone")
    ren.GetActiveCamera().Azimuth(1)
    iren.Start()                                        #程序运行
if __name__ == "__main__":
    main()