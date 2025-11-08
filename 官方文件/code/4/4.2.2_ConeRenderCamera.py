import vtk

def main():
    cone = vtk.vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)
    
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)

    ren = vtk.vtkRenderer()
    ren.AddActor(coneActor)
    ren.SetBackground(1,1,1)
    
    myCamera = vtk.vtkCamera()                           #增加相机        
    myCamera.SetClippingRange(0.1,1000)                  #设置剪切面范围
    myCamera.SetFocalPoint(0,-1,0)                       #设置焦点
    myCamera.SetPosition(5,1,1)                          #设置相加位置
    myCamera.SetViewUp(1,0.5,0.2)                        #设置相机朝上方向
    myCamera.Zoom(0.5)                                   #放大或所想模型
    ren.SetActiveCamera(myCamera)
    ren.GetActiveCamera().Azimuth(30)                    #相机视点位置沿顺时针旋转 30度角 
    ren.GetActiveCamera().Elevation(60)                  #视点位置沿向上的方向旋转 90 度角

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(600, 600)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renWin.Render()
    iren.Start()
    
if __name__ == "__main__":
    main()