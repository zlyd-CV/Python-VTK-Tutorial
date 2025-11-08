import vtk

def main():
    cone = vtk.vtkConeSource()                        #生成一个锥形体
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(8)
    
    coneMapper = vtk.vtkPolyDataMapper()              #锥形体数据的映射转换 
    coneMapper.SetInputConnection(cone.GetOutputPort())

    coneActor = vtk.vtkActor()                         #生成一个演员
    coneActor.SetMapper(coneMapper)
    
    sphere =vtk.vtkSphereSource()
    sphere.SetRadius(3.0)
    sphere.SetPhiResolution(30)
    sphere.SetThetaResolution(30)
    sphere.SetCenter(5,2,0)
    
    sphereMapper = vtk.vtkPolyDataMapper()              #球体数据的映射转换 
    sphereMapper.SetInputConnection(sphere.GetOutputPort())

    sphereActor = vtk.vtkActor()                         #生成一个演员
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetRepresentationToWireframe()
    
    lightR=vtk.vtkLight()                               #设置红光灯光
    lightR.SetColor(1,0,0)
    lightR.SetPosition(0,0,10)
    
    lightG=vtk.vtkLight()                               #设置绿灯光
    lightG.SetColor(0,1,0)
    lightG.SetPosition(0,10,0)
    
    ren = vtk.vtkRenderer()                            #生成一个渲染器
    ren.SetBackground(1,1,1)
    ren.AddActor(coneActor)
    ren.AddActor(sphereActor)
    lightR.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())
    lightG.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())
    ren.AddLight(lightR)
    ren.AddLight(lightG)
    
    renWin = vtk.vtkRenderWindow()                    #生成渲染显示的窗口
    renWin.AddRenderer(ren)
    renWin.SetSize(300, 300)
    renWin.Render()
    renWin.SetWindowName("Light")

    iren = vtk.vtkRenderWindowInteractor()               #生成一个交互器
    iren.SetRenderWindow(renWin)
    
    style = vtk.vtkInteractorStyleTrackballCamera()       #设置交互模式
    iren.SetInteractorStyle(style)

    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)

    iren.Start()                                       #程序交互运行
if __name__ == "__main__":
    main()     
   
    
    
