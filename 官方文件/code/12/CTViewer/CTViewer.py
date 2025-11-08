import vtk
import sys

from PyQt5.QtWidgets import  (QApplication, QMainWindow, QFileDialog, QDialog, QInputDialog, QLineEdit,
                         QAbstractItemView, QMessageBox, QDataWidgetMapper, QFileDialog, QTreeWidgetItem)
from PyQt5.QtCore import  (pyqtSlot, Qt,QItemSelectionModel,
                         QModelIndex,QFile,QIODevice,QFileInfo)

from vtkmodules import vtkInteractionStyle
from MainWindow import Ui_MainWindow

class MyCTViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui=Ui_MainWindow()    #创建UI对象
        self.ui.setupUi(self)      #构造UI界面

        self.cur_window = 1
        self.init_SagittalVTKWin()       #初始化矢状面显示窗口
        self.init_CoronalVTKWin()        #初始化冠状面显示窗口
        self.init_AxialVTKWin()          #初始化横断面显示窗口
        self.init_SurfaceVTKWin()        #初始化等值面显示窗口

        # CT序列读取
        self.filepath = QFileDialog.getExistingDirectory(self,"打开文件夹","./")             #打开CT文件夹
        print(self.filepath)
        self.dcmReader = vtk.vtkDICOMImageReader()
        self.dcmReader.SetDataByteOrderToLittleEndian()
        self.dcmReader.SetDirectoryName(self.filepath)
        #self.dcmRescaleSlope = self.dcmReader.GetRescaleSlope()
        #self.dcmRescaleOffset = self.dcmReader.GetRescaleOffset()
        self.dcmReader.Update()

        # 横断面窗口显示的参数设置
        self.dcmViewer1 = vtk.vtkImageViewer2()
        self.dcmViewer1.SetInputConnection(self.dcmReader.GetOutputPort())
        self.dcmViewer1.SetupInteractor(self.ui.vtk_window_1)
        self.dcmViewer1.SetRenderWindow(self.ui.vtk_window_1.GetRenderWindow())  # 将图像显示在Qt的窗口中
        self.dcmViewer1.SetColorLevel(0)
        self.dcmViewer1.SetColorWindow(1500)
        self.dcmViewer1.SetSliceOrientationToXY()                                # 横断面 (Transverse)
        self.dcmViewer1.UpdateDisplayExtent()
        self.dcmViewer1.Render()

        # 冠狀面窗口显示的参数设置
        self.dcmViewer2 = vtk.vtkImageViewer2()
        self.dcmViewer2.SetInputConnection(self.dcmReader.GetOutputPort())
        self.dcmViewer2.SetupInteractor(self.ui.vtk_window_2)
        self.dcmViewer2.SetRenderWindow(self.ui.vtk_window_2.GetRenderWindow())
        self.dcmViewer2.SetColorLevel(0)
        self.dcmViewer2.SetColorWindow(1500)
        self.dcmViewer2.SetSliceOrientationToYZ()                                # 冠狀面 (Coronal plane)
        self.dcmViewer2.UpdateDisplayExtent()
        self.renderer2 = self.dcmViewer2.GetRenderer()
        self.cam2 = self.renderer2.GetActiveCamera()
        self.cam2.SetViewUp(0, 0, -1)                                            #翻转CT显示方向
        self.renderer2.ResetCamera()
        self.dcmViewer2.Render()

        # 矢状面窗口显示的参数设置
        self.dcmViewer3 = vtk.vtkImageViewer2()
        self.dcmViewer3.SetInputConnection(self.dcmReader.GetOutputPort())
        self.dcmViewer3.SetupInteractor(self.ui.vtk_window_3)
        self.dcmViewer3.SetRenderWindow(self.ui.vtk_window_3.GetRenderWindow())
        self.dcmViewer3.SetColorLevel(0)
        self.dcmViewer3.SetColorWindow(1500)
        self.dcmViewer3.SetSliceOrientationToXZ()   # 矢状面 (Sagittal plane)
        self.dcmViewer3.UpdateDisplayExtent()
        self.renderer3 = self.dcmViewer3.GetRenderer()
        self.cam3 = self.renderer3.GetActiveCamera()
        self.cam3.SetViewUp(0, 0, -1)                                           #翻转CT显示方向
        self.renderer3.ResetCamera()
        self.dcmViewer3.Render()

        #生成等值面
        mc=vtk.vtkMarchingCubes()
        mc.SetInputConnection(self.dcmReader.GetOutputPort())
        mc.SetValue(-500,-300)
        mcmapper=vtk.vtkPolyDataMapper()
        mcmapper.SetInputConnection(mc.GetOutputPort())
        mcmapper.ScalarVisibilityOff()  #取消颜色
        mcactor=vtk.vtkActor()
        mcactor.SetMapper(mcmapper)
        self.renSurfaceVTKWin.AddActor(mcactor)
        self.renSurfaceVTKWin.ResetCamera()


        #设置键盘监听
        self.ui.vtk_window_1.AddObserver(vtk.vtkCommand.KeyPressEvent, self.keyboard_callback_func)
        self.ui.vtk_window_2.AddObserver(vtk.vtkCommand.KeyPressEvent, self.keyboard_callback_func)
        self.ui.vtk_window_3.AddObserver(vtk.vtkCommand.KeyPressEvent, self.keyboard_callback_func)

        #设置鼠标右键监听
        self.ui.vtk_window_1.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.VTKWindow1Callback)
        self.ui.vtk_window_2.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.VTKWindow2Callback)
        self.ui.vtk_window_3.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.VTKWindow3Callback)

    def init_AxialVTKWin(self):
        self.renAxialVTKWin = vtk.vtkRenderer()
        self.ui.vtk_window_1.GetRenderWindow().AddRenderer(self.renAxialVTKWin)
        self.irenAxialVTKWin = self.ui.vtk_window_1.GetRenderWindow().GetInteractor()
        self.irenAxialVTKWin.Initialize()

    def init_CoronalVTKWin(self):
        self.renCoronalVTKWin = vtk.vtkRenderer()
        self.ui.vtk_window_2.GetRenderWindow().AddRenderer(self.renCoronalVTKWin)
        self.irenCoronalVTKWin = self.ui.vtk_window_2.GetRenderWindow().GetInteractor()
        self.irenCoronalVTKWin.Initialize()

    def init_SagittalVTKWin(self):
        self.renSagittalVTKWin = vtk.vtkRenderer()
        self.ui.vtk_window_3.GetRenderWindow().AddRenderer(self.renSagittalVTKWin)
        self.irenSagittalVTKWin = self.ui.vtk_window_3.GetRenderWindow().GetInteractor()
        self.irenSagittalVTKWin.Initialize()

    def init_SurfaceVTKWin(self):
        self.renSurfaceVTKWin = vtk.vtkRenderer()
        self.ui.vtk_window_4.GetRenderWindow().AddRenderer(self.renSurfaceVTKWin)
        self.irenSurfaceVTKWin = self.ui.vtk_window_4.GetRenderWindow().GetInteractor()
        self.irenSurfaceVTKWin.Initialize()

    def keyboard_callback_func(self, obj, event_id):
        if self.cur_window == 1:
            cur_dcm_viewer = self.dcmViewer1
        elif self.cur_window == 2:
            cur_dcm_viewer = self.dcmViewer2
        elif self.cur_window == 3:
            cur_dcm_viewer = self.dcmViewer3

        cur_slice = cur_dcm_viewer.GetSlice()
        if obj.GetKeySym() == 'Right' or obj.GetKeySym() == 'Down':
            cur_slice = (cur_slice + 1) % (cur_dcm_viewer.GetSliceMax() + 1)
            cur_dcm_viewer.SetSlice(cur_slice)
        if obj.GetKeySym() == 'Left' or obj.GetKeySym() == 'Up':
            cur_slice = (cur_slice + cur_dcm_viewer.GetSliceMax()) % (cur_dcm_viewer.GetSliceMax() + 1)
            cur_dcm_viewer.SetSlice(cur_slice)
        #print(' %d / %d ' % (cur_slice + 1, self.dcmViewer.GetSliceMax() + 1))

    def VTKWindow1Callback(self, obj, event):
        if event == "RightButtonPressEvent":
            self.cur_window = 1

    def VTKWindow2Callback(self, obj, event):
        if event == "RightButtonPressEvent":
            self.cur_window = 2

    def VTKWindow3Callback(self, obj, event):
        if event == "RightButtonPressEvent":
            self.cur_window = 3

    def RightButtonCallback(self, obj, event):
        print(obj.name())
        print('RightButtonPressEvent')
        if event == "RightButtonPressEvent":
            self.is_right_button_down = True
        else:
            self.is_right_button_down = False


if  __name__ == "__main__":
    app = 0
    app = QApplication(sys.argv)    #创建GUI应用程序
    mainform = MyCTViewer()        #创建主窗体
    mainform.show()                 #显示主窗体
    sys.exit(app.exec_())
