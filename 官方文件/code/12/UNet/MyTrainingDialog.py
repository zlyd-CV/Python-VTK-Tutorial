import os
import sys
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QApplication, QDialog)
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import loadUiType
from UNet import UNetModel, UNetPredict

ui_file = os.path.join(os.path.dirname(__file__), 'TrainingDialog.ui')
ui, QMainWindow = loadUiType(ui_file)


# 当程序打印内容更新时，发出 text_changed 信号，传递当前打印内容
class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))

    def flush(self):
        pass


# 定义一个工作类，用于运行训练程序
class UNetTrainingWork(QObject):
    # 定义一个信号，用于传递训练结果
    training_finish = pyqtSignal()

    def __init__(self, model_type, input_shape, data_path, savemodel_path, batch_size, epochs,
                 validation_split):
        super().__init__()
        self.model_type = model_type
        self.input_shape = input_shape
        self.data_path = data_path
        self.savemodel_path = savemodel_path
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split

    def run_training(self):
        # run u net
        u_net = UNetModel(
            input_shape=self.input_shape,
            data_path=self.data_path,
            savemodel_path=self.savemodel_path,
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_split=self.validation_split
        )
        u_net.train()

        self.training_finish.emit()


class UNetPredictionWork(QObject):
    # 定义一个信号，用于传递训练结果
    prediction_finish = pyqtSignal()

    def __init__(self, model_file_name, input_file_name, output_file_name, batch_size=5, verbose=1):
        super().__init__()
        self.model_file_name = model_file_name
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.batch_size = batch_size
        self.verbose = verbose

    def run_prediction(self):
        # run u net
        prediction = UNetPredict(
            self.model_file_name,
            self.input_file_name,
            self.output_file_name,
            self.batch_size,
            self.verbose
        )
        prediction.predict()
        self.prediction_finish.emit()


class MyTrainingDialog(QMainWindow, ui):
    def __init__(self, **params):
        super(MyTrainingDialog, self).__init__()
        self.setupUi(self)

        # 创建方法，接管系统 print 输出，并将输出写入文本框
        sys.stdout = EmittingStream(text_written=self.output_written)

        self.training_work = None
        self.training_thread = None
        
        self.group_box_info.setTitle(params.get('model_type'))
        info = ""
        for key, value in params.items():
            info = info + f"{key}: {value}\n"
        
        self.label_msg.setText(info)

        # 创建线程，并创建工作类的实例，并将工作类的实例传递给线程
        # 将线程的启动信号与工作类的 run_training 方法关联，在线程启动时，调用工作类的 run_training 方法，开始训练
        # 将工作类的完成信号与 on_training_finish 方法关联，用于在线程完成后关闭线程
        # 使用按钮启动线程
        if params.get('model_type') == 'UNet':
            self.training_thread = QThread()
            self.training_work = UNetTrainingWork(
                model_type=params.get("model_type"),
                input_shape=params.get("input_shape"),
                data_path=params.get("data_path"),
                savemodel_path=params.get("savemodel_path"),
                batch_size=params.get("batch_size"),
                epochs=params.get("epochs"),
                validation_split=params.get("validation_split")
            )
            self.training_work.moveToThread(self.training_thread)
            self.training_thread.started.connect(self.training_work.run_training)
            self.training_work.training_finish.connect(self.on_training_finish)
        elif params.get('model_type') == 'UNetPredict':
            self.training_thread = QThread()
            self.prediction_work = UNetPredictionWork(
                model_file_name=params.get("model_file_name"),
                input_file_name=params.get("input_file_name"),
                output_file_name=params.get("output_file_name"),
                batch_size=params.get("batch_size"),
                verbose=params.get("verbose")
            )
            self.prediction_work.moveToThread(self.training_thread)
            self.training_thread.started.connect(self.prediction_work.run_prediction)
            self.prediction_work.prediction_finish.connect(self.on_training_finish)

        self.bt_start.clicked.connect(lambda: self.start())

    # start 方法用于与按钮事件连接，启动线程
    def start(self):
        #print("Start")

        if self.training_thread is not None:
            self.training_thread.start()

    # on_training_finish 方法用于与工作类的完成信号连接，关闭线程
    def on_training_finish(self):
        print("Finished")
        self.training_thread.quit()

    # output_written 方法用于与 EmittingStream 的输出信号连接，将输出写入文本框
    def output_written(self, text):
        cursor = self.text_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_log.setTextCursor(cursor)
        self.text_log.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建GUI应用程序
    main_window = MyTrainingDialog(
        model_type="U-Net",
        input_shape="input_shape",
        data_path="data_path",
        savemodel_path="savemodel_path",
        roi_name="ROIName",
        batch_size="batch_size",
        epochs="epochs",
        validation_split="validation_split"
    )  # 创建主窗体
    main_window.show()  # 显示主窗体
    sys.exit(app.exec_())
