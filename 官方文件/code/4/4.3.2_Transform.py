import vtk

def main():
    #创建一个球
    sourceSphere = vtk.vtkSphereSource()
    sourceSphere.SetRadius(1)
    sourceSphere.SetPhiResolution(50)
    sourceSphere.SetThetaResolution(50)
    sourceSphere.Update()

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sourceSphere.GetOutputPort())

    sphereActor = vtk.vtkActor()
    sphereActor.SetPosition(0,0,0)
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(1,0,0)

    #创建一个锥体
    sourceCone = vtk.vtkConeSource()
    sourceCone.SetRadius(1)
    sourceCone.SetHeight(3)
    sourceCone.SetCenter(0,0,0)
    sourceCone.Update()

    ConeMapper = vtk.vtkPolyDataMapper()
    ConeMapper.SetInputConnection(sourceCone.GetOutputPort())

    ConeActor = vtk.vtkActor()
    ConeActor.SetPosition(0,0,0)
    ConeActor.SetMapper(ConeMapper)
    ConeActor.GetProperty().SetColor(0,1,0)

    oriConeActor = vtk.vtkActor()
    oriConeActor.SetMapper(ConeMapper)

    #创建一个坐标轴演员
    oriAxesActor = vtk.vtkAxesActor()
    oriAxesActor.SetPosition(0,0,0)
    oriAxesActor.SetTotalLength(3,3,3)
    oriAxesActor.SetShaftType(0)
    oriAxesActor.SetAxisLabels(0)
    oriAxesActor.SetCylinderRadius(0.005)

    #创建另一个坐标轴
    axesActor = vtk.vtkAxesActor()
    axesActor.SetPosition(0,0,0)
    axesActor.SetTotalLength(3,3,3)
    axesActor.SetShaftType(0)
    axesActor.SetAxisLabels(0)
    axesActor.SetCylinderRadius(0.005)

    #创建一个文字标签
    textActor = vtk.vtkTextActor()
    textActor.SetPosition2(100,40)
    textActor.GetTextProperty().SetFontSize(24)
    textActor.GetTextProperty().SetColor(1,0,0)

    #创建空间变换
    trans = vtk.vtkTransform()
    trans.PostMultiply()
    ConeActor.SetPosition(1,0,0)
    trans.Translate(5,0,0)
    trans.RotateZ(45)

    ConeActor.SetUserTransform(trans)
    textActor.SetInput(" PostMultiply()\n RotateZ(45)\n Translate(1,0,0)")

    print(ConeActor.GetMatrix())
    print(ConeActor.GetUserMatrix())

    ren1 = vtk.vtkRenderer()
    ren2 = vtk.vtkRenderer() 
    ren1.AddActor(oriAxesActor)
    ren1.AddActor(sphereActor)
    ren1.AddActor(oriConeActor)
    ren2.AddActor(axesActor)
    ren2.AddActor(ConeActor)
    ren2.AddActor(sphereActor)

    #标签信息的二维显示
    ren2.AddActor2D(textActor)
    
    leftview = [0,0,0.5,1.0]
    rightview = [0.5,0,1.0,1.0]
    ren1.SetBackground(0.3,0.3,0.5)
    ren2.SetBackground(0.2,0.4,0.5)
    ren1.SetViewport(leftview)
    ren2.SetViewport(rightview)
    
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(800,400)
    renWin.AddRenderer(ren1)
    renWin.AddRenderer(ren2)
    renWin.Render()
    renWin.SetWindowName("Transform")
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)  
    iren.Start()

if __name__ == '__main__':
    main()