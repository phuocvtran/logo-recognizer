import cv2
import numpy as np
import os


class HaarCascade:
    def __init__(self):
        self.logo_cascade = {}
        self.detected_logos_coord = np.zeros(4)

    def fit(self, haar_xml_paths, keys):
        """
        Đọc các file xml chứa haar-feature
        :param harr_xml_paths: Đường dẫn đến folder chứa các file xml
        :param keys: danh sách tên các class
        """
        for key in keys:
            self.logo_cascade[key] = cv2.CascadeClassifier(os.path.join(haar_xml_paths, key + ".xml"))

    def detectAndCrop(self, image, dst):
        """
        Vẽ các vùng detect được và crop
        :param image: Đường dẫn đến ảnh
        :param dst: Đường dẫn đến nơi lưu trữ ảnh được vẽ
        """
        img_list = []
        image = cv2.imread(image)
        detect_img = image.copy()
        gray = cv2.cvtColor(detect_img, cv2.COLOR_BGR2GRAY)
        G = 0
        R = 0
        B = 255
        for key in self.logo_cascade:
            curr_coord = self.logo_cascade[key].detectMultiScale(gray, 1.1, 1)
            self.detected_logos_coord = np.vstack((self.detected_logos_coord, curr_coord))
            for (x, y, w, h) in curr_coord:
                cv2.rectangle(detect_img, (x, y),(x + w, y + h), (B, G, R), 1)
            G += 11
            R += abs(G - B)
            B -= round(abs(B - G / R / 3))

        self.detected_logos_coord = np.delete(self.detected_logos_coord, 0, axis=0)

        cv2.imwrite(dst, detect_img)

        for (x, y, w, h) in self.detected_logos_coord:
            x = int(x)
            y = int(y)
            w = int(w)
            h = int(h)
            crop_img = image[y : y + h, x : x + w]
            img_list.append(crop_img)
        return img_list
