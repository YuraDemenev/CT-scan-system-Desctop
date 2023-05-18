# Для Dicom
from datetime import datetime
import pydicom as dicom
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt


def get_pixels_hu(scans: dicom.Dataset):
    image = np.stack(scans.pixel_array)
    image = image.astype(np.int16)
    image[image == -2000] = 0

    intercept = scans.RescaleIntercept if "RescaleIntercept" in scans else -1024
    slope = scans.RescaleSlope if "RescaleSlope" in scans else 1

    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)

    return np.array(image, dtype=np.int16)


class DicomOpenClass:
    def OpenDicom():
        dc = dicom.dcmread(os.getcwd() + "\\WorkFiles\\dicom.dcm")
        arr_hu = get_pixels_hu(dc)

        np.save("./WorkFiles/npy1", arr_hu)

        img_shape = list(dc.pixel_array[0].shape)
        img_shape.append(int(512))
        volume3d = np.zeros(img_shape)

        for i in range(512):
            array2d = dc.pixel_array[i]
            volume3d[:, :, i] = array2d

        print("start image")
        for i in range(0, img_shape[2]):
            plt.imsave(
                f"./Images/Axial/axial{i+1}.jpg",
                volume3d[:, :, i],
                cmap="gray",
            )
            plt.imsave(
                f"./Images/Sagital/sagital{i+1}.jpg",
                volume3d[:, i, :],
                cmap="gray",
            )
            plt.imsave(
                f"./Images/Coronal/coronal{i+1}.jpg",
                volume3d[511 - i, :, :],
                cmap="gray",
            )
        print("End image")

    def create_a_table_array():
        dc = dicom.dcmread(os.getcwd() + "\\WorkFiles\\dicom.dcm")
        arr_string = str(np.array(dc.convert_pixel_data))
        arr_string = arr_string.split()

        # Получение даты
        index = arr_string.index("Study")
        study_data = arr_string[index + 3]
        study_data = study_data.replace("'", "")

        arr_string.pop(index)

        date = datetime(
            year=int(study_data[0:4]),
            month=int(study_data[4:6]),
            day=int(study_data[6:8]),
        )

        study_data = str(date)

        scores = (
            ["Study date", study_data[0:10]],
            ["Modality", dc.Modality],
            ["Patient ID", dc.PatientID],
            ["Patient position", dc.PatientPosition],
            ["Patient sex", dc.PatientSex],
        )
        return scores
