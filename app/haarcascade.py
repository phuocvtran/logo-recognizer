import cv2
import numpy as np
import os


class HaarCascade:
    def __init__(self):
        self.logo_cascade = {}
        self.detected_logo_coords = None

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
        self.detected_logo_coords = np.zeros(4)
        img_list = []
        image = cv2.imread(image)
        detect_img = image.copy()
        gray = cv2.cvtColor(detect_img, cv2.COLOR_BGR2GRAY)
        G = 0
        R = 0
        B = 255
        i = 0
        for key in self.logo_cascade:
            curr_coord = self.logo_cascade[key].detectMultiScale(gray, 1.1, 1)
            if np.array(curr_coord).size > 3:
                self.detected_logo_coords = np.vstack((self.detected_logo_coords, curr_coord))
                for (x, y, w, h) in curr_coord:
                    cv2.rectangle(detect_img, (x, y),(x + w, y + h), (B, G, R), 2)
                    cv2.putText(img=detect_img, text=str(i + 1), org=(x, y - 3), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(B, G, R), fontScale=0.8, thickness=2)
                    i += 1
                G += 11
                R += abs(G / B)
                B -= round(abs(B / G / R / 3))

        self.detected_logo_coords = np.delete(self.detected_logo_coords, 0, axis=0)

        cv2.imwrite(dst, detect_img)
        if self.detected_logo_coords.size > 3:
            for (x, y, w, h) in self.detected_logo_coords:
                x = int(x)
                y = int(y)
                w = int(w)
                h = int(h)
                crop_img = image[y : y + h, x : x + w]
                img_list.append(crop_img)

        return img_list
