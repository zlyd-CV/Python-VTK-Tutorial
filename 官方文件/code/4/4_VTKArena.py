import vtk

def main():
    cone = vtk.vtkConeSource()                        #生成一个锥形体
    cone.SetHeight(2.0)
    cone.SetRadius(1.0)
    cone.SetResolution(8)
    

    coneMapper = vtk.vtkPolyDataMapper()              #锥形体数据的映射转换 
    coneMapper.SetInputConnection(cone.GetOutputPort())

    coneActor = vtk.vtkActor()                         #生成一个演员
    coneActor.SetMapper(coneMapper)
    
    sphere =vtk.vtkSphereSource()
    sphere.SetRadius(2.0)
    sphere.SetPhiResolution(30)
    sphere.SetThetaResolution(30)
    sphere.SetCenter(5,2,0)
    
    sphereMapper = vtk.vtkPolyDataMapper()              #球体数据的映射转换 
    sphereMapper.SetInputConnection(sphere.GetOutputPort())

    sphereActor = vtk.vtkActor()                         #生成一个演员
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetRepresentationToWireframe()
    #sphereActor.GetProperty().SetRepresentationToPoints()
    
    cylinder1 = vtk.vtkCylinderSource()
    cylinder1.SetResolution(50)
    cylinder1.SetCenter(3,5,0)
    cylinder1.SetRadius(0.3)
    cylinder1.SetHeight(0.5)
    
    cylinder1Mapper = vtk.vtkPolyDataMapper()              #球体数据的映射转换 
    cylinder1Mapper.SetInputConnection(cylinder1.GetOutputPort())

    cylinder1Actor = vtk.vtkActor()                         #生成一个演员
    cylinder1Actor.SetMapper(cylinder1Mapper)
    
    cylinder2 = vtk.vtkCylinderSource()
    cylinder2.SetResolution(50)
    cylinder2.SetCenter(0,5,0)
    cylinder2.SetRadius(0.3)
    cylinder2.SetHeight(0.5)
    
    cylinder2Mapper = vtk.vtkPolyDataMapper()              #球体数据的映射转换 
    cylinder2Mapper.SetInputConnection(cylinder2.GetOutputPort())

    cylinder2Actor = vtk.vtkActor()                         #生成一个演员
    cylinder2Actor.SetMapper(cylinder2Mapper)
    
    cylinder3 = vtk.vtkCylinderSource()
    cylinder3.SetResolution(50)
    cylinder3.SetCenter(6,5,0)
    cylinder3.SetRadius(0.3)
    cylinder3.SetHeight(0.5)
    
    cylinder3Mapper = vtk.vtkPolyDataMapper()              #球体数据的映射转换 
    cylinder3Mapper.SetInputConnection(cylinder3.GetOutputPort())

    cylinder3Actor = vtk.vtkActor()                         #生成一个演员
    cylinder3Actor.SetMapper(cylinder3Mapper)
    
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
    ren.AddActor(cylinder1Actor)
    ren.AddActor(cylinder2Actor)
    ren.AddActor(cylinder3Actor)
    lightR.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())
    lightG.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())
    ren.AddLight(lightR)
    ren.AddLight(lightG)
    
    renWin = vtk.vtkRenderWindow()                    #生成渲染显示的窗口
    renWin.AddRenderer(ren)
    renWin.SetSize(500, 300)
    renWin.Render()
    renWin.SetWindowName("Arena")

    iren = vtk.vtkRenderWindowInteractor()               #生成一个交互器
    iren.SetRenderWindow(renWin)
    
    style = vtk.vtkInteractorStyleTrackballCamera()       #设置交互模式
    iren.SetInteractorStyle(style)

    ren.ResetCamera()
    ren.GetActiveCamera().Azimuth(30)

    iren.Start()                                       #程序交互运行
if __name__ == "__main__":
    main()     
   
    
    
