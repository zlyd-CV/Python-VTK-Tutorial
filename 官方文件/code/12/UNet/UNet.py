from pyrsistent import v
import tensorflow as tf
import numpy as np
import time


class UNetModel:
    def __init__(self, input_shape, data_path, savemodel_path, batch_size, epochs, validation_split):
        self.input_shape = input_shape
        self.data_path = data_path
        self.savemodel_path = savemodel_path
        self.model_file = savemodel_path
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split

        self.X_train = np.load(self.data_path + 'X_train.npy')
        self.Y_train = np.load(self.data_path + 'Y_train.npy')
        self.X_test = np.load(self.data_path + 'X_test.npy')
        self.Y_test = np.load(self.data_path + 'Y_test.npy')

    # UNet输入模块
    def InputBlock(self, input, filters, kernel_size=3, strides=1, padding='same'):
        conv_1 = tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding,
                                        activation='relu')(input)  # 卷积块1
        return tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding,
                                      activation='relu')(conv_1)  # 卷积块2

    # 收缩路径模块
    def ContractingPathBlock(self, input, filters, kernel_size=3, strides=1, padding='same'):
        down_sampling = tf.keras.layers.MaxPool2D((2, 2))(input)  # 最大池化
        conv_1 = tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding,
                                        activation='relu')(down_sampling)  # 卷积块1
        return tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding,
                                      activation='relu')(conv_1)  # 卷积块2

    # 扩张（恢复）路径模块
    def ExpansivePathBlock(self, input, con_feature, filters, tran_filters, kernel_size=3, tran_kernel_size=2,
                           strides=1,
                           tran_strides=2, padding='same', tran_padding='same'):
        upsampling = tf.keras.layers.Conv2DTranspose(filters=tran_filters, kernel_size=tran_kernel_size,
                                                     strides=tran_strides, padding=tran_padding)(input)  # 上采样（转置卷积方式）

        padding_h = (con_feature.shape)[1] - (upsampling.shape)[1]
        padding_w = (con_feature.shape)[2] - (upsampling.shape)[2]
        upsampling = tf.pad(
            upsampling, ((0, 0), (0, padding_h), (0, padding_w), (0, 0)), 'constant')
        con_feature = tf.image.resize(con_feature, ((upsampling.shape)[1], (upsampling.shape)[2]),
                                      method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)  # 裁剪需要拼接的特征图
        # 拼接扩张层和收缩层的特征图（skip connection）
        concat_feature = tf.concat([con_feature, upsampling], axis=3)
        conv_1 = tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding,
                                        activation='relu')(concat_feature)  # 卷积1
        return tf.keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding=padding,
                                      activation='relu')(conv_1)  # 卷积2

    # UNet网络架构
    def UNet(self, input_shape):
        inputs = tf.keras.layers.Input(input_shape)
        s = tf.keras.layers.Lambda(lambda x: x)(inputs)

        # input block
        input_block = self.InputBlock(s, 64)

        # contracting path
        con_1 = self.ContractingPathBlock(input_block, 128)
        con_2 = self.ContractingPathBlock(con_1, 256)
        con_3 = self.ContractingPathBlock(con_2, 512)
        con_4 = self.ContractingPathBlock(con_3, 1024)

        # expansive path
        exp_4 = self.ExpansivePathBlock(con_4, con_3, 512, 512)
        exp_3 = self.ExpansivePathBlock(exp_4, con_2, 256, 256)
        exp_2 = self.ExpansivePathBlock(exp_3, con_1, 128, 128)
        exp_1 = self.ExpansivePathBlock(exp_2, input_block, 64, 64)

        outputs = tf.keras.layers.Conv2D(1, 1, activation='sigmoid')(exp_1)
        return tf.keras.Model(inputs=[inputs], outputs=[outputs])

    def train(self):
        model = self.UNet(input_shape=self.input_shape)
        model.summary()
        print(time.asctime())
        model.compile(optimizer='adam',
                      loss='binary_crossentropy', metrics=['accuracy'])

        callbacks = [tf.keras.callbacks.TensorBoard('./logs_keras')]

        print(self.X_train.shape)
        print(self.Y_train.shape)
        model.fit(self.X_train, self.Y_train, batch_size=self.batch_size,
                  epochs=self.epochs, validation_split=self.validation_split, callbacks=callbacks)
        print(time.asctime())
        model.save(self.model_file)


class UNetPredict:
    def __init__(self, model_file_name, input_file_name, output_file_name, batch_size=5, verbose=1):
        self.model_file_name = model_file_name
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.batch_size = batch_size
        self.verbose = verbose

    def predict(self):
        model = tf.keras.models.load_model(self.model_file_name)
        input_data = np.load(self.input_file_name)
        pred_data = model.predict(input_data, batch_size=self.batch_size, verbose=self.verbose)
        np.save(self.output_file_name, pred_data)


if __name__ == "__main__":
    # 样本图片大小
    IMG_WIDTH = 256
    IMG_HEIGHT = 256
    IMG_CHANNELS = 1

    ROI_NAME = 'lung_left'
    DATA_PATH = './dataset/' + ROI_NAME + '/'
    SaveModel_Path = './model/'

    u_net = UNetModel(
        input_shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS),
        data_path=DATA_PATH,
        savemodel_path=SaveModel_Path,
        roi_name=ROI_NAME,
        batch_size=10,
        epochs=50,
        validation_split=0.2
    )
    u_net.train()
