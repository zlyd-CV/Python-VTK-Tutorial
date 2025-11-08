import vtk

#创建的回调函数
def boxCallback(obj, event):
    t = vtk.vtkTransform()
    obj.GetTransform(t)
    obj.GetProp3D().SetUserTransform(t)

def main():
    
    # 创建锥形体
    cone = vtk.vtkConeSource()
    cone.SetResolution(20)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(0,0.9,0.9)

    # 创建一个渲染器和一个渲染窗口
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.9,0.9,0.9)
    renderer.AddActor(coneActor)

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(renderer)
    renwin.Render()
    renwin.SetWindowName("Box Widget")
    

    #创建交互器
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renwin)

    #生成一个盒式的Widget工具
    boxWidget = vtk.vtkBoxWidget()
    boxWidget.SetInteractor(interactor)
    boxWidget.SetProp3D(coneActor)
    boxWidget.SetPlaceFactor(1.25)  # 创建一个盒子为1.25倍大，稍大于上面的锥体
    boxWidget.PlaceWidget()
    boxWidget.On()

    # 连接回调函数
    boxWidget.AddObserver("InteractionEvent", boxCallback)

    interactor.Initialize()
    
    interactor.Start()

if __name__ == '__main__':
    main()