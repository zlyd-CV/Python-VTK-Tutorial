import vtk


def main():
    cone = vtk.vtkConeSource()  # 创建数据源圆锥体,其参数配置与之前一样
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(8)
    coneMapper = vtk.vtkPolyDataMapper()  # 创建圆锥体数据的映射转换器
    coneMapper.SetInputConnection(cone.GetOutputPort())  # 将映射器的输入与圆锥体数据源的输出连接起来,建立VTK管线(pipeline)

    coneActor = vtk.vtkActor()  # 生成一个演员
    coneActor.SetMapper(coneMapper)  # 将映射器(圆锥体)与演员关联起来
    sphere = vtk.vtkSphereSource()  # 创建数据源球体,其参数配置与之前一样
    sphere.SetRadius(3.0)  # 设置球体半径
    sphere.SetPhiResolution(30)  # 设置球体纬线分辨率
    sphere.SetThetaResolution(30)  # 设置球体经线分辨率
    sphere.SetCenter(5, 2, 0)  # 设置球体中心位置

    sphereMapper = vtk.vtkPolyDataMapper()  # 创建球体数据的映射转换器
    sphereMapper.SetInputConnection(sphere.GetOutputPort())  # 设置映射器的数据输入端口为球体数据源的输出端口

    sphereActor = vtk.vtkActor()  # 生成一个演员
    sphereActor.SetMapper(sphereMapper)  # 将映射器(球体)与演员关联起来
    sphereActor.GetProperty().SetRepresentationToWireframe()  # 设置球体演员的显示属性为线框模式

    lightR = vtk.vtkLight()  # 新建一个vtkLight对象,该对象表示一个光源
    lightR.SetColor(1, 0, 0)  # 设置红色光
    lightR.SetPosition(0, 0, 10)  # 设置光源位置

    lightG = vtk.vtkLight()  # 新建一个vtkLight对象,该对象表示一个光源
    lightG.SetColor(0, 1, 0)  # 设置绿色光
    lightG.SetPosition(0, 10, 0)  # 设置光源位置

    ren = vtk.vtkRenderer()  # 生成一个渲染器
    ren.SetBackground(1, 1, 1)  # 设置背景为白色
    ren.AddActor(coneActor)  # 将圆锥体演员添加到渲染器中
    ren.AddActor(sphereActor)  # 将球体演员添加到渲染器中
    lightR.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())  # 将红色灯光的焦点设置在渲染器当前活动相机的焦点上，这使得灯光总是朝向场景中心
    lightG.SetFocalPoint(ren.GetActiveCamera().GetFocalPoint())  # 将绿色灯光的焦点设置在渲染器当前活动相机的焦点上，这使得灯光总是朝向场景中心
    """
    代码拆解:
    ren.GetActiveCamera()：获取当前场景的相机，也就是你的“眼睛”
    .GetFocalPoint()：获取相机的焦点位置，通常是场景的中心点
    lightR.SetFocalPoint(...)：将光源的焦点设置为相机,光源从点光源变为聚光灯,光线朝向焦点位置
    这样设置的目的是确保无论相机如何移动,光源始终朝向场景的中心,从而实现一致的照明效果
    """
    ren.AddLight(lightR)  # 将红色光源添加到渲染器中,一旦添加光源,默认的头顶光照明将被禁用
    ren.AddLight(lightG)  # 将绿色光源添加到渲染器中

    # 为了更直观的观察演员的位置,我在源代码的基础上添加了坐标轴显示,你可以观察光源的位置与演员的位置关系
    axes = vtk.vtkAxesActor()  # 创建坐标轴演员,该演员包含X、Y、Z三个坐标轴
    axes.SetTotalLength(3.0, 3.0, 3.0)  # 设置坐标轴显示轴线的总长度
    axes.SetShaftTypeToCylinder()  # 设置坐标轴的轴杆类型为圆柱
    axes.SetCylinderRadius(0.01)  # 设置坐标轴的圆柱半径为0.01
    axes.GetXAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()  # 设置坐标轴标签的文本缩放模式为无缩放
    axes.GetYAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()  # 设置坐标轴标签的文本缩放模式为无缩放
    axes.GetZAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()  # 设置坐标轴标签的文本缩放模式为无缩放
    axes.GetXAxisCaptionActor2D().SetCaptionTextProperty(vtk.vtkTextProperty())  # 设置X轴标签的文本属性,vtkTextProperty()是一个文本属性对象
    axes.GetYAxisCaptionActor2D().SetCaptionTextProperty(vtk.vtkTextProperty())  # 设置Y轴标签的文本属性
    axes.GetZAxisCaptionActor2D().SetCaptionTextProperty(vtk.vtkTextProperty())  # 设置Z轴标签的文本属性
    ren.AddActor(axes)  # 将坐标轴添加到渲染器中

    renWin = vtk.vtkRenderWindow()  # 创建一个渲染窗口(RenderWindow)。这是在屏幕上实际显示的窗口
    renWin.AddRenderer(ren)  # 将渲染器添加到渲染窗口中
    renWin.SetSize(300, 300)  # 设置渲染窗口的大小为300x300像素
    renWin.Render()  # 执行渲染操作,将场景绘制到渲染窗口中
    renWin.SetWindowName("Light")  # 设置渲染窗口的标题为"Light"

    iren = vtk.vtkRenderWindowInteractor()  # 生成一个交互器(iren),处理键盘和鼠标事件
    iren.SetRenderWindow(renWin)  # 将渲染窗口(renWin)与交互器(iren)关联起来

    style = vtk.vtkInteractorStyleTrackballCamera()  # 创建一个交互样式对象，这里使用的是“轨迹球相机”样式,即移动的是相机而不是演员

    iren.SetInteractorStyle(style)  # 将这个交互样式设置给交互器
    ren.ResetCamera()  # 重置相机以适应场景中的所有演员
    ren.GetActiveCamera().Azimuth(30)  # 将相机绕垂直轴顺时针旋转30度(可以看看默最初视角的偏移以理解偏移方向)

    iren.Start()  # 启动交互器,开始事件循环,允许用户与渲染窗口进行交互


if __name__ == "__main__":
    main()
"""
学习收获与思考:
1.与前2个代码都构成一样,VTK管线包括数据源->映射器->演员(包括图形与光源)->渲染器->渲染窗口->交互器
在本代码中,数据源是圆锥体和球体,映射器分别是圆锥体映射器和球体映射器,演员分别是圆锥体演员和球体演员,渲染器是ren,渲染窗口是renWin,交互器是iren(轨迹球相机交互器)
在渲染器里添加的不仅有演员,还有光源,光源与演员共同决定了最终的渲染效果

思考:
1.尝试在不同位置添加更多图形,借由坐标显示轴,观察指定图像的坐标是如何影响图形位置的
2.同样,将style = vtk.vtkInteractorStyleTrackballCamera()改为style = vtk.vtkInteractorStyleTrackballActor(),你将更清楚的理解为什么后者是移动演员
3.尝试添加更多光源(通过不同的RGB值的组合),并调整它们的位置和颜色,观察渲染效果的变化
"""
