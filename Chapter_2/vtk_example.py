"""
欢迎踏上VTK的学习之旅!VTK(Visualization Toolkit)是一个强大的开源软件系统,用于3D计算机图形学、图像处理和可视化。
它广泛应用于科学计算、医学成像和工程模拟等领域。
让我们先从使用VTK创建一个简单的3D锥体开始
"""

import vtk


def main():
    """
    在正式阅读代码之前,您需要了解VTK的可视化管线：
    1. 数据源（Source）：生成或读取数据，例如几何体、图像等。
    2. 过滤器（Filter）：对数据进行处理和转换。
    3. 映射器（Mapper）：将数据映射到图形表示。
    4. 演员（Actor）：表示图形对象，可以设置属性如颜色、位置等。
    5. 渲染器（Renderer）：负责将演员渲染到屏幕上。
    6. 渲染窗口（Render Window）：显示渲染结果的窗口。
    7. 交互器（Interactor）：处理用户交互，如鼠标和键盘事件。
    """
    # ----- 创建数据源(Source) -----
    cone = vtk.vtkConeSource()  # 创建一个vtkConeSource 对象,这是一个算法对象,用于生成圆锥体的几何数据（点、线、多边形等）
    cone.SetHeight(2.0)  # 设置圆锥的高度为2.0
    cone.SetRadius(1.0)  # 设置圆锥的底部半径为1.0
    cone.SetResolution(8)  # 设置圆锥底部的多边形分辨率为8,这意味着底部将是一个八边形,值越大,底部越接近圆形,

    # ----- 创建映射器(Mapper) -----
    coneMapper = vtk.vtkPolyDataMapper()  # 创建一个vtkPolyDataMapper对象,用于将圆锥体的几何数据映射到图形表示
    # 若下行代码编辑器报错，只是因为C++底层库在Python解释器中的"误判"，不需要修正
    coneMapper.SetInputConnection(cone.GetOutputPort())  # 将圆锥体数据源的输出端口连接到映射器的输入端口，表示了数据流的方向

    # ----- 创建演员(Actor) -----
    coneActor = vtk.vtkActor() # 创建一个vtkActor对象,演员(Actor)代表了渲染场景中的一个实体,可以设置其属性如位置、颜色等
    coneActor.SetMapper(coneMapper) # 为演员指定一个映射器，演员通过映射器获取其几何数据和图形表示,演员还负责定义物体的外观和行为

    # ----- 创建渲染器(Renderer) -----
    ren = vtk.vtkRenderer() # 创建一个vtkRenderer对象,该对象为vtk管线中渲染器,渲染器负责管理一个三维场景中的所有演员
    ren.AddActor(coneActor) # 将圆锥体演员(coneActor)添加到渲染器中,一个渲染器可以包含多个演员
    ren.SetBackground(0.8, 0.8, 0.8) # 设置渲染器的背景颜色为浅灰色,参数表示RGB3通道的颜色值，范围从0到1

    # ----- 创建渲染窗口(Render Window) -----
    renWin = vtk.vtkRenderWindow() # 创建一个vtkRenderWindow对象,渲染窗口用于显示渲染器(ren)存储的内容
    renWin.AddRenderer(ren) # 将渲染器(ren)添加到渲染窗口中,一个渲染窗口可以包含多个渲染器
    renWin.SetSize(500, 500) # 设置渲染窗口的大小为500x500像素

    # ----- 创建交互器(Interactor) -----
    iren = vtk.vtkRenderWindowInteractor() # 创建一个vtkRenderWindowInteractor对象,交互器用于处理用户与渲染窗口之间的交互
    iren.SetRenderWindow(renWin) # 将渲染窗口(renWin)与交互器(iren)关联起来,使得用户可以通过交互器与渲染窗口进行交互

    # ----- 场景设置和渲染 -----
    ren.ResetCamera() # 重置摄像机位置,以确保场景中的所有演员都在视野范围内
    ren.GetActiveCamera().Azimuth(30) # 调整摄像机的方位角,使得视角绕Y轴旋转30度,这会从一个稍微侧方的角度来观察物体

    renWin.Render()  # 执行一次完整的渲染流程。VTK管线被触发，数据从源头流向末端，最终生成一幅图像并显示在渲染窗口中
    renWin.SetWindowName('Cone') # 设置渲染窗口的标题为'Cone'
    ren.GetActiveCamera().Azimuth(1) # 进一步调整摄像机的方位角,使得视角绕Y轴再旋转1度,这有助于微调视角以获得更好的观察效果(怎么感觉这行代码用处不大)
    iren.Start() # 启动交互器,进入事件循环,允许用户与渲染窗口进行交互,如旋转、缩放和平移视图


if __name__ == '__main__':
    main()
"""
学习收获:
1.综上,我们可以推断VTK可视化管线的数据流是从数据源开始,构建演员再使用渲染器将创建的演员显示在渲染窗口中,用户可以通过交互器与渲染窗口进行交互。

2.你可以自己试着改进代码超参数,以尝试获得不同的图像,这将对于你理解代码有很大帮助。
例如:
①cone.SetHeight(2.0),将2.0变为5.0或5;
②cone.SetResolution(8),将8变为100,你会得到一个底部平滑(但并不是真正完全平滑)的圆锥体;
③ren.SetBackground(0.8, 0.8, 0.8),尝试更改通道值(假设你熟悉RGB通道的基本原理)将背景颜色改为其他颜色,例如(1,0,0)表示红色;
④renWin.SetSize(500, 500),尝试更改生成的窗口大小,例如(800,600)等。

3.如果你对VTK感兴趣,可以参考官方文档(https://examples.vtk.org/site/Python/Tutorial/Tutorial_Step1/)和教程,最后祝您学习之旅愉快!
"""