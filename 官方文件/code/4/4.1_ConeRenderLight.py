import vtk
 
def main():
    cone = vtk.vtkConeSource()                        #生成一个锥形体
    cone.SetHeight(2.0)
    cone.SetRadius(1.0)
    cone.SetResolution(8)
 
    coneMapper = vtk.vtkPolyDataMapper()            #锥形体数据的映射转换 
    coneMapper.SetInputConnection(cone.GetOutputPort())
 
    coneActor = vtk.vtkActor()                         #生成一个演员
    coneActor.SetMapper(coneMapper)
    
    light=vtk.vtkLight()                               #设置灯光
    light.SetColor(1,0,0)
    light.SetPosition(0,0,10)
    
    ren = vtk.vtkRenderer()                            #生成一个渲染器
    ren.SetBackground(0,0,0)
    ren.AddActor(coneActor)
    light.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())
    ren.AddLight(light)
    
    renWin = vtk.vtkRenderWindow()                    #生成渲染显示的窗口
    renWin.AddRenderer(ren)
    renWin.SetSize(500, 500)
    renWin.Render()
    renWin.SetWindowName("ConeRenderLight")
 
    iren = vtk.vtkRenderWindowInteractor()               #生成一个交互器
    iren.SetRenderWindow(renWin)    
    style = vtk.vtkInteractorStyleTrackballActor()           #设置交互模式
    iren.SetInteractorStyle(style)
 
    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)
    iren.Start()                                       #程序交互运行
if __name__ == "__main__":
    main()