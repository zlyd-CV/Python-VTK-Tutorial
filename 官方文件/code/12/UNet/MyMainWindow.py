import os
import tensorflow as tf
import numpy as np
import vtk
import sys
from PyQt5.QtCore import (pyqtSlot, Qt, QItemSelectionModel, QThread,
                          QModelIndex, QFile, QIODevice, QFileInfo, QObject, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMessageBox)
from PyQt5.uic import loadUiType
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from MyTrainingDialog import MyTrainingDialog

ui_file = os.path.join(os.path.dirname(__file__), 'MainWindow.ui')
ui, QMainWindow = loadUiType(ui_file)


class MyMainWindow(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

        # 初始化默认参数
        self.init_default_values()

        # 初始化 VTK 窗口
        self.vtk_window_1 = self.init_vtk_widget(self.vtk_window_1)
        self.vtk_window_2 = self.init_vtk_widget(self.vtk_window_2)
        self.vtk_window_3 = self.init_vtk_widget(self.vtk_window_3)
        self.vtk_window_4 = self.init_vtk_widget(self.vtk_window_4)

        # 初始化全局变量
        self.dcm_viewer_ct = None
        self.dcm_viewer_roi = None
        self.dcm_viewer_pred = None

        self.img_ct_full = None
        self.img_roi_full = None
        self.img_pred_full = None

        self.npy_ct = None
        self.npy_roi = None
        self.npy_pred = None

        self.current_index = 0
        self.max_index = 0
        self.current_type = None

        self.filepath = None

    # 初始化默认参数
    def init_default_values(self):
        self.edit_batch_size.setText("10")
        self.edit_epochs.setText("3")
        self.edit_validation.setText("0.2")

    # 初始化 VTK 窗口
    def init_vtk_widget(self, ui_widget):
        # 将占位 widget 替换为 QVTKRenderWindowInteractor
        parent = ui_widget.parentWidget()
        tmp = QVTKRenderWindowInteractor(self)
        replaced_item = parent.layout().replaceWidget(ui_widget, tmp)
        if replaced_item is not None:
            ui_widget.deleteLater()
        ui_widget = tmp

        # 初始化 VTK 窗口
        ren = vtk.vtkRenderer()
        ui_widget.GetRenderWindow().AddRenderer(ren)
        iren = ui_widget.GetRenderWindow().GetInteractor()
        iren.Initialize()
        return ui_widget

    def get_vtk_image_data(self, source_npy, normal, spacing_x, spacing_y, spacing_z) -> vtk.vtkImageData:
        x_size = source_npy.shape[1]
        y_size = source_npy.shape[2]
        z_size = source_npy.shape[0]
        dim_size = source_npy.shape[3]
        img_data = vtk.vtkImageData()
        info = img_data.GetInformation()
        img_data.SetDimensions(
            x_size, y_size, z_size)
        img_data.SetSpacing(spacing_x, spacing_y, spacing_z)
        img_data.SetNumberOfScalarComponents(1, info)
        img_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        for z in range(z_size):
            for y in range(x_size):
                for x in range(y_size):
                    img_data.SetScalarComponentFromFloat(
                        y, x, z, 0, source_npy[z, x_size - 1 - x, y, 0] * normal)
        img_data.Modified()
        return img_data

    # 读取 npy 文件并将其内容写入 VTK 中
    def load_npy_files(self):
        current_roi = self.combo_roi_list.currentText()
        print(f"show_npy_files: {current_roi}")
        self.current_type = self.tab_type.tabText(self.tab_type.currentIndex())
        print(f"current_type: {self.current_type}")
        if self.current_type == "Train":
            current_name = "train"
        else:
            current_name = "test"
        ct_file_name = f"{self.filepath}/{current_roi}/X_{current_name}.npy"
        roi_file_name = f"{self.filepath}/{current_roi}/Y_{current_name}.npy"
        pred_file_name = f"{self.filepath}/{current_roi}/Y_pred.npy"
        print(f"ct_file_name: {ct_file_name}, roi_file_name: {roi_file_name}")
        if not os.path.exists(ct_file_name) or not os.path.exists(ct_file_name):
            print("File not found!")
            msg_box = QMessageBox(QMessageBox.Warning,
                                  "Warning", "File not found!")
            msg_box.exec_()
            return

        self.npy_ct = np.load(ct_file_name)
        self.npy_roi = np.load(roi_file_name)
        if self.npy_ct.shape[0] != self.npy_roi.shape[0]:
            print("Number of the slices is not the same!")
            msg_box = QMessageBox(
                QMessageBox.Warning, "Warning", "Number of the slices is not the same!")
            msg_box.exec_()
            self.npy_ct = None
            self.npy_roi = None
            return
        print(
            f"npy_ct.shape: {self.npy_ct.shape}, npy_roi.shape: {self.npy_roi.shape}")

        # 用来将 npy 数组写入 vtkImageData， 耗时较长
        # self.img_ct_full = self.get_vtk_image_data(
        #     self.npy_ct, (1 / 4000 * 255), 1, 1, 1)
        # self.img_roi_full = self.get_vtk_image_data(
        #     self.npy_roi, 255, 1, 1, 1)

        if self.current_type == "Test":
            if not os.path.exists(pred_file_name):
                print("Pred file not found!")
                msg_box = QMessageBox(QMessageBox.Warning,
                                      "Warning", "Pred file not found! Please do the predict first!")
                msg_box.exec_()
            else:
                self.npy_pred = np.load(pred_file_name)

            if self.npy_pred is not None and self.npy_ct.shape[0] != self.npy_pred.shape[0]:
                print("Pred file not correct!")
                self.npy_pred = None
                msg_box = QMessageBox(QMessageBox.Warning,
                                      "Warning", "Pred file not correct! Please do the predict first!")
                msg_box.exec_()

            if self.npy_pred is not None:
                iso_value = 1
                
                roibox = np.load(f"{self.filepath}/{current_roi}/{current_roi}BoxData.npy")
                npy_pred_512 = np.zeros((len(roibox), 512, 512, 1))
                for i in range(roibox.shape[0]):
                    image = tf.cast(self.npy_pred[i],tf.float32)
                    pred_img = tf.image.resize(image,(roibox[i][2]*2,roibox[i][2]*2))
                    npy_pred_512[i][(roibox[i][0]-roibox[i][2]):(roibox[i][0]+roibox[i][2]),(roibox[i][1]-roibox[i][2]):(roibox[i][1]+roibox[i][2])] =  pred_img[:,:]
                    
                #self.img_pred_full = self.get_vtk_image_data(
                #    self.npy_pred, 255, 1, 1, 5)
                self.img_pred_full = self.get_vtk_image_data(
                    npy_pred_512, 255, 1, 1, 5)
                surface = vtk.vtkMarchingCubes()
                surface.SetInputData(self.img_pred_full)
                surface.SetValue(0, 125)

                surface_mapper = vtk.vtkPolyDataMapper()
                surface_mapper.SetInputConnection(surface.GetOutputPort())
                surface_mapper.ScalarVisibilityOff()  # 取消颜色
                surface_actor = vtk.vtkActor()
                surface_actor.SetMapper(surface_mapper)
                ren_3d = self.vtk_window_3.GetRenderWindow().GetRenderers().GetFirstRenderer()
                ren_3d.AddActor(surface_actor)
                surface_actor.Modified()  # 通知管线，数据发生了修改
                ren_3d.ResetCamera()
                ren_3d.Render()  # 刷新窗口

        self.current_index = 0
        self.max_index = self.npy_ct.shape[0]
        self.slider_main.setMinimum(0)
        self.slider_main.setMaximum(self.max_index - 1)
        self.slider_main.setValue(0)

        self.refresh_vtk_image()

    
    def refresh_vtk_image(self):
        current_ct = self.npy_ct[self.current_index]
        current_roi = self.npy_roi[self.current_index]

        ct_x_size = current_ct.shape[0]
        ct_y_size = current_ct.shape[1]
        ct_z_size = current_ct.shape[2]

        img_ct = vtk.vtkImageData()
        info = img_ct.GetInformation()
        img_ct.SetDimensions(ct_x_size, ct_y_size, ct_z_size)
        img_ct.SetNumberOfScalarComponents(1, info)
        img_ct.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        for y in range(ct_x_size):
            for x in range(ct_y_size):
                img_ct.SetScalarComponentFromFloat(
                    y, x, 0, 0, current_ct[ct_x_size - 1 - x, y, 0] / 4000 * 255)
        img_ct.Modified()

        if self.dcm_viewer_ct is None:
            self.dcm_viewer_ct = vtk.vtkImageViewer2()
            self.dcm_viewer_ct.SetupInteractor(self.vtk_window_1)
            self.dcm_viewer_ct.SetRenderWindow(
                self.vtk_window_1.GetRenderWindow())  # 将图像显示在Qt的窗口中
        self.dcm_viewer_ct.SetInputData(img_ct)
        self.dcm_viewer_ct.SetColorLevel(125)
        self.dcm_viewer_ct.SetColorWindow(255)
        self.dcm_viewer_ct.UpdateDisplayExtent()
        self.dcm_viewer_ct.Render()

        roi_x_size = current_roi.shape[0]
        roi_y_size = current_roi.shape[1]
        roi_z_size = current_roi.shape[2]

        img_roi = vtk.vtkImageData()
        info = img_roi.GetInformation()
        img_roi.SetDimensions(roi_x_size, roi_y_size, roi_z_size)
        img_roi.SetNumberOfScalarComponents(1, info)
        img_roi.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        for y in range(roi_x_size):
            for x in range(roi_y_size):
                img_roi.SetScalarComponentFromFloat(
                    y, x, 0, 0, current_roi[roi_x_size - 1 - x, y, 0] * 255)
        img_roi.Modified()

        if self.dcm_viewer_roi is None:
            self.dcm_viewer_roi = vtk.vtkImageViewer2()
            self.dcm_viewer_roi.SetupInteractor(self.vtk_window_2)
            self.dcm_viewer_roi.SetRenderWindow(
                self.vtk_window_2.GetRenderWindow())  # 将图像显示在Qt的窗口中
        self.dcm_viewer_roi.SetInputData(img_roi)
        self.dcm_viewer_roi.SetColorLevel(125)
        self.dcm_viewer_roi.SetColorWindow(255)
        self.dcm_viewer_roi.UpdateDisplayExtent()
        self.dcm_viewer_roi.Render()

        if self.current_type == "Test" and self.npy_pred is not None:
            current_pred = self.npy_pred[self.current_index]
            pred_x_size = current_pred.shape[0]
            pred_y_size = current_pred.shape[1]
            pred_z_size = current_pred.shape[2]

            img_pred = vtk.vtkImageData()
            info = img_pred.GetInformation()
            img_pred.SetDimensions(pred_x_size, pred_y_size, pred_z_size)
            img_pred.SetNumberOfScalarComponents(1, info)
            img_pred.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
            for y in range(pred_x_size):
                for x in range(pred_y_size):
                    img_pred.SetScalarComponentFromFloat(
                        y, x, 0, 0, current_pred[pred_x_size - 1 - x, y, 0] * 255)
            img_pred.Modified()

            if self.dcm_viewer_pred is None:
                self.dcm_viewer_pred = vtk.vtkImageViewer2()
                self.dcm_viewer_pred.SetupInteractor(self.vtk_window_4)
                self.dcm_viewer_pred.SetRenderWindow(
                    self.vtk_window_4.GetRenderWindow())  # 将图像显示在Qt的窗口中
            self.dcm_viewer_pred.SetInputData(img_pred)
            self.dcm_viewer_pred.SetColorLevel(125)
            self.dcm_viewer_pred.SetColorWindow(255)
            self.dcm_viewer_pred.UpdateDisplayExtent()
            self.dcm_viewer_pred.Render()


    @pyqtSlot()
    def on_actionOpen_triggered(self):
        # 打开 dataset 目录
        self.filepath = QFileDialog.getExistingDirectory(
            self, "Open dataset folder", "../dataset")
        print(f"Selected path: {self.filepath}")

        # 读取 ROI list
        self.roi_list = os.listdir(self.filepath)
        print(f"currend roi: {self.roi_list}")
        self.combo_roi_list.clear()
        self.combo_roi_list.addItems(self.roi_list)

    @pyqtSlot('QString')
    def on_combo_roi_list_currentTextChanged(self, text):
        print(f"currentTextChanged: {text}")
        if text == "":
            return

        # 显示数据集
        self.load_npy_files()

    @pyqtSlot('int')
    def on_tab_type_currentChanged(self, i):
        print(f"on_tab_type_currentChanged: {i}")
        self.load_npy_files()

    @pyqtSlot('int')
    def on_slider_main_valueChanged(self, i):
        self.current_index = self.slider_main.value()
        self.refresh_vtk_image()

    @pyqtSlot()
    def on_bt_run_clicked(self):
        if self.current_type == "Train":
            current_roi = self.combo_roi_list.currentText()
            model_path = os.path.abspath(
                os.path.dirname(self.filepath) + "/model/" + current_roi + ".h5")
            print(f"model_path:{model_path}")

            training_dialog = MyTrainingDialog(
                model_type="UNet",
                input_shape=(256, 256, 1),
                data_path=f"{self.filepath}/{current_roi}/",
                savemodel_path=model_path,
                batch_size=int(self.edit_batch_size.text()),
                epochs=int(self.edit_epochs.text()),
                validation_split=float(self.edit_validation.text())
            )
            training_dialog.exec_()
        elif self.current_type == "Test":
            current_roi = self.combo_roi_list.currentText()
            model_path = os.path.abspath(
                os.path.dirname(self.filepath) + os.path.sep + ".")
            model_file_name = model_path + "/model/" + current_roi + ".h5"
            input_file_name = self.filepath + "/" + current_roi + "/X_test.npy"
            output_file_name = self.filepath + "/" + current_roi + "/Y_pred.npy"

            training_dialog = MyTrainingDialog(
                model_type="UNetPredict",
                model_file_name=model_file_name,
                input_file_name=input_file_name,
                output_file_name=output_file_name,
                batch_size=5,
                verbose=1
            )
            training_dialog.exec_()


    @pyqtSlot()
    def on_actionQuit_triggered(self):
        self.close()

    def closeEvent(self, event):
        self.vtk_window_1.Finalize()
        self.vtk_window_2.Finalize()
        self.vtk_window_3.Finalize()
        self.vtk_window_4.Finalize()


if __name__ == "__main__":
    app = 0
    app = QApplication(sys.argv)  # 创建GUI应用程序
    mainform = MyMainWindow()  # 创建主窗体
    mainform.show()  # 显示主窗体
    sys.exit(app.exec_())
    
