import vtk


def main():
    reader = vtk.vtkBMPReader()  # 读取BMP格式图像,BMP是一种位图图像文件格式
    reader.SetFileName("../data/wins.bmp")

    texture = vtk.vtkTexture()  # 生成纹理类对象,接受图像数据并将其应用于3D对象的表面
    texture.SetInputConnection(reader.GetOutputPort())  # 将数据源的输出端口连接到纹理对象的输入端口
    texture.InterpolateOn()  # 开启插值功能。当纹理被拉伸或放大时，开启此功能可以让像素之间的颜色平滑过渡，使图像看起来更自然，而不是呈现马赛克状的像素块

    cylinder = vtk.vtkCylinderSource()  # 生成一个柱状体(多边形柱状体)数据源
    cylinder.SetHeight(4.0)
    cylinder.SetRadius(1.0)
    cylinder.SetResolution(6)

    Mapper = vtk.vtkPolyDataMapper()  # 创建一个多边形数据映射器,用于将几何数据映射到图形表示
    Mapper.SetInputConnection(cylinder.GetOutputPort())  # 将柱状体数据源的输出端口连接到映射器的输入端口

    actor = vtk.vtkActor()  # 创建一个演员对象,演员代表渲染场景中的一个实体
    actor.SetMapper(Mapper)  # 为演员指定一个映射器，演员通过映射器获取其几何数据和图形表示
    actor.SetTexture(texture)  # 将纹理应用于演员，使得柱状体表面显示图像纹理,该代码行将之前创建的纹理对象应用到演员上

    renderer = vtk.vtkRenderer()  # 创建一个渲染器对象,渲染器负责管理一个三维场景中的所有演员
    renderer.AddActor(actor)  # 将演员添加到渲染器中
    renderer.SetBackground(1.0, 1.0, 1.0) # 设置渲染器的背景颜色为白色

    renWin = vtk.vtkRenderWindow()  # 创建一个渲染窗口对象,渲染窗口用于显示渲染器存储的内容
    renWin.AddRenderer(renderer)  # 将渲染器添加到渲染窗口中
    renWin.SetSize(480, 480)  # 设置渲染窗口的大小为480x480像素
    renWin.Render()  # 执行一次完整的渲染流程。VTK管线被触发，数据从源头流向末端，最终生成一幅图像并显示在渲染窗口中(其实这行代码不是必要的)
    renWin.SetWindowName("MyTexture") # 设置渲染窗口的标题为"MyTexture"

    iren = vtk.vtkRenderWindowInteractor() # 创建一个渲染窗口交互器对象,交互器用于处理用户与渲染窗口之间的交互
    iren.SetRenderWindow(renWin) # 将渲染窗口与交互器关联起来,使得用户可以通过交互器与渲染窗口进行交互

    style = vtk.vtkInteractorStyleTrackballCamera() # 创建一个交互样式对象，这里使用的是“轨迹球摄像机”样式
    iren.SetInteractorStyle(style) # 将这个交互样式设置给交互器

    iren.Initialize() # 初始化交互器,准备处理用户输入事件
    iren.Start() # 启动交互器,进入事件循环,允许用户与渲染窗口进行交互,如旋转、缩放和平移视图


if __name__ == "__main__":
    main()
"""
学习收获:
1. 学习了如何使用VTK读取图像文件并将其作为纹理应用到3D对象的表面。
2. 了解了纹理插值的作用

思考:
尝试删除纹理代码行，观察柱状体表面的变化。
"""
