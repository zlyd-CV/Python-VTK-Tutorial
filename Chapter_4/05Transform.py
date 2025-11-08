import vtk


def main():
    # 创建一个球,半径为1,分辨率为50
    sourceSphere = vtk.vtkSphereSource()
    sourceSphere.SetRadius(1)
    sourceSphere.SetPhiResolution(50)  # 设置纬线方向的分辨率,越大越平滑
    sourceSphere.SetThetaResolution(50)  # 设置经线方向的分辨率,可以试试改成1,2,3...可以更好地理解多边体这一概念
    sourceSphere.Update()  # 更新球体数据,尽管不是必须的,但可以作为数据准备完成的一个标识

    sphereMapper = vtk.vtkPolyDataMapper()  # 创建一个多边形数据映射器
    sphereMapper.SetInputConnection(sourceSphere.GetOutputPort())  # 将球体数据连接到映射器

    sphereActor = vtk.vtkActor()  # 创建一个演员来表示球体
    sphereActor.SetPosition(0, 0, 0)  # 设置球体位置在原点
    sphereActor.SetMapper(sphereMapper)  # 将映射器赋给演员
    sphereActor.GetProperty().SetColor(1, 0, 0)  # 设置球体颜色为红色

    # 创建一个锥体
    sourceCone = vtk.vtkConeSource()  # 创建一个锥体数据源
    sourceCone.SetRadius(1)  # 设置锥体底部半径为1
    sourceCone.SetHeight(3)  # 设置锥体高度为3
    sourceCone.SetCenter(0, 0, 0)  # 设置锥体中心在原点(你可以试试改成(1.5,0,0)看看效果)
    sourceCone.Update()  # 更新锥体数据

    ConeMapper = vtk.vtkPolyDataMapper()  # 创建一个多边形数据映射器
    ConeMapper.SetInputConnection(sourceCone.GetOutputPort())  # 将锥体数据连接到映射器

    ConeActor = vtk.vtkActor()  # 创建一个演员来表示锥体
    ConeActor.SetPosition(0, 0, 0)  # 设置锥体位置在原点
    ConeActor.SetMapper(ConeMapper)  # 将映射器赋给演员
    ConeActor.GetProperty().SetColor(0, 1, 0)  # 设置锥体颜色为绿色
    """
    上述代码创建了一个红色的球体和一个绿色的锥体,并将它们的位置都设置在了坐标原点(0,0,0),完成了数据源->演员的创建。
    """

    oriConeActor = vtk.vtkActor()  # 创建一个原始锥体演员(记录未变换前的锥体)
    oriConeActor.SetMapper(ConeMapper)  # 将映射器赋给原始锥体演员

    # 创建一个坐标轴演员
    oriAxesActor = vtk.vtkAxesActor()
    oriAxesActor.SetPosition(0, 0, 0)  # 设置坐标轴位置在原点
    oriAxesActor.SetTotalLength(3, 3, 3)  # 设置坐标轴的总长度
    oriAxesActor.SetShaftType(0)  # 设置轴杆类型为线条,1为圆柱
    """
    为了让代码更具可读性，避免记住 0 和 1 这种“魔术数字 (Magic Numbers)”，VTK 提供了两个等效的、名字更清晰的方法：
    oriAxesActor.SetShaftTypeToLine() 等同于 oriAxesActor.SetShaftType(0)
    oriAxesActor.SetShaftTypeToCylinder() 等同于 oriAxesActor.SetShaftType(1)
    """
    oriAxesActor.SetAxisLabels(0)  # 不显示轴标签(如果想显示xyz标签,可以改成非0值)
    oriAxesActor.SetCylinderRadius(0.005)  # 设置轴的圆柱半径

    # 创建另一个坐标轴,配置同上
    axesActor = vtk.vtkAxesActor()
    axesActor.SetPosition(0, 0, 0)
    axesActor.SetTotalLength(3, 3, 3)
    axesActor.SetShaftType(0)
    axesActor.SetAxisLabels(0)
    axesActor.SetCylinderRadius(0.005)

    # 创建一个文字标签,显示变换信息
    textActor = vtk.vtkTextActor()  # 创建一个文本演员
    textActor.SetPosition2(100, 40)  # 设置文本演员在渲染窗口中的位置(像素单位), (左下角为(0,0))
    textActor.GetTextProperty().SetFontSize(24)  # 设置文本字体大小
    textActor.GetTextProperty().SetColor(1, 0, 0)  # 设置文本颜色为红色

    # 创建空间变换
    trans = vtk.vtkTransform() # 创建一个变换对象
    trans.PostMultiply() # 设置变换顺序为后乘(PostMultiply),即先执行后添加的变换操作
    ConeActor.SetPosition(1, 0, 0) # 先将锥体沿X轴平移1个单位
    trans.Translate(5, 0, 0) # 再将锥体沿X轴平移5个单位
    trans.RotateZ(45) # 最后将锥体绕Z轴旋转45度

    ConeActor.SetUserTransform(trans)  # 将变换应用到锥体演员
    textActor.SetInput(" PostMultiply()\n RotateZ(45)\n Translate(1,0,0)")  # 设置文本内容显示变换顺序

    print(ConeActor.GetMatrix())  # 通过 actor.GetMatrix() 获取这个最终组合好的内部变换矩阵。这个矩阵代表了你所有 SetPosition、Rotate、Scale 等方法调用的综合结果。
    print(ConeActor.GetUserMatrix()) # 打印锥体的用户变换矩阵,用户变换指使用独立的 vtkTransform 对象,对演员实现空间变换
    # 最终变换矩阵 = 用户变换矩阵 * 内部变换矩阵

    ren1 = vtk.vtkRenderer() # 创建第一个渲染器
    ren2 = vtk.vtkRenderer() # 创建第二个渲染器
    ren1.AddActor(oriAxesActor) # 在第一个渲染器中添加原始坐标轴演员
    ren1.AddActor(sphereActor) # 在第一个渲染器中添加球体演员
    ren1.AddActor(oriConeActor) # 在第一个渲染器中添加原始锥体演员
    ren2.AddActor(axesActor) # 在第二个渲染器中添加变换后的坐标轴演员
    ren2.AddActor(ConeActor) # 在第二个渲染器中添加变换后的锥体演员
    ren2.AddActor(sphereActor) # 在第二个渲染器中添加球体演员

    # 标签信息的二维显示
    # ren2.AddActor2D(textActor) 该方法已经过时了,尽管可以使用但会触发警告,开发者打算在vtk9.50之后的某个版本中移除它
    # 因为在旧的vtk版本中,向渲染器添加不同的物体需要添加不同的方法,例如:
    # 添加三维物体(Actor): renderer.AddActor(my3DActor)
    # 添加二维物体(Actor2D): renderer.AddActor2D(my2DActor)
    # 添加体数据(Volume): renderer.AddVolume(myVolume)
    # 为了让 API 更具一致性，他们引入了一个更通用的基类 vtkProp，所有可以被渲染的东西（演员、体、2D演员等）都继承自它。
    # 因此，他们也提供了一个通用的添加方法：AddViewProp()
    ren2.AddViewProp(textActor)

    leftview = [0, 0, 0.5, 1.0]  # 设置第一个渲染器的视口为左半边(与上节不同的是,这里使用列表表示[xmin,ymin,xmax,ymax])
    rightview = [0.5, 0, 1.0, 1.0] # 设置第二个渲染器的视口为右半边
    ren1.SetBackground(0.3, 0.3, 0.5) # 设置第一个渲染器的背景颜色
    ren2.SetBackground(0.2, 0.4, 0.5) # 设置第二个渲染器的背景颜色
    ren1.SetViewport(leftview) # 应用第一个渲染器的视口设置,用于确认渲染器(包含原始坐标轴,球体,原始锥体演员)位置
    ren2.SetViewport(rightview) # 应用第二个渲染器的视口设置,用于确认渲染器(包含变换后的坐标轴,球体,变化后的锥体演员)位置

    renWin = vtk.vtkRenderWindow() # 创建渲染窗口
    renWin.SetSize(800, 400) # 设置渲染窗口大小为800x400像素
    renWin.AddRenderer(ren1) # 将第一个渲染器添加到渲染窗口
    renWin.AddRenderer(ren2) # 将第二个渲染器添加到渲染窗口
    renWin.Render()  # 执行渲染操作(其实这里可以省略,因为后面交互器启动时会自动调用渲染)
    renWin.SetWindowName("Transform")

    iren = vtk.vtkRenderWindowInteractor() # 创建渲染窗口交互器
    iren.SetRenderWindow(renWin) # 将渲染窗口交互器与渲染窗口关联
    iren.Start() # 启动交互器,循环等待用户交互


if __name__ == '__main__':
    main()
"""
学习收获:
1.本代码通过配置2个渲染器的视口(Viewport),实现了在同一个渲染窗口中同时显示两个不同的渲染器构建的场景。
2.通过对演员应用空间变换(Transform),实现了对演员位置和朝向的控制。
3.通过打印演员的变换矩阵,理解了变换矩阵和用户变换矩阵的区别。
4.总结了交互器(RenderWindowInteractor)、渲染窗口(RenderWindow)、渲染器(Renderer)和演员(Actor)之间的关系。
[ vtkRenderWindowInteractor ]  <-- (交互器处理用户输入)
                         |
                         | .SetRenderWindow()
                         V
            [ vtkRenderWindow ]  <-- (管理所有渲染器，是屏幕上的窗口)
                /          \
               / .AddRenderer() \
              V                  V
[ vtkRenderer 1 ]     [ vtkRenderer 2 ]  <-- (管理各自的场景: Actor, Camera, Light)
      |                        |
      V                        V
[ vtkActor A ]         [ vtkActor B ]
"""
