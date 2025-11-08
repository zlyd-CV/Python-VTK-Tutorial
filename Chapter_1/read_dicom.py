"""
给出了如何使用pydicom库读取DICOM文件的示例代码。
"""
import pydicom

if __name__ == "__main__":
    ds = pydicom.dcmread("../data/CT.dcm") # 读取DICOM文件
    print(ds) # 打印DICOM文件的所有元数据
    print("="*50)
    print(ds.StudyDate) # 打印StudyDate字段的值
    print("="*50)
    print(ds.pixel_array) # 打印图像数据的像素数组
"""
学习收获与思考:
对于DICOM数据个人认为非常复杂,如果只是想从影像方面入手,不必太关注DICOM文件的元数据,只需了解如何使用pydicom库读取DICOM文件获取数据后转为NumPy数组即可。
"""