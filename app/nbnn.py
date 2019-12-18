from sklearn.neighbors import KDTree
import cv2
import numpy as np
import h5py


class NaiveBayesNN:
    def __init__(self):
        self.dsift_file = None
        self.trees = None
        self.keys = None

    def fit(self, dsift_path):
        """
        Từ các key trong file hdf5 tạo nên các cây tương ứng
        :param dsift_file: path đến file hdf5 lưu trữ dsift của các lớp
        :param return: Trả về các key của file
        """
        self.dsift_file = h5py.File(dsift_path, "r")
        self.keys = [key for key in self.dsift_file.keys()]
        self.trees = self.construct_kd_tree(self.keys)
        self.dsift_file.close()

        return self.keys

    def getDSift(self, image, step_size):
        """
        Lấy dsift của ảnh bằng cách chia ảnh ra thành nhiều vùng có kích thước step_size * step_size
        và thực hiện tìm key point trên từng vùng, sau đó trích descriptor từ các key point đó.
        :param image: Ảnh cần lấy dsift.
        :param step_size: Số bước / kích thước từng vùng được chia ra.
        :return: các key point và sift descriptor.
        """
        processed_image = self.process_img(image)
        sift = cv2.xfeatures2d.SIFT_create()
        key_points = [cv2.KeyPoint(x, y, step_size) for y in range(0, processed_image.shape[0], step_size)
                      for x in range(0, processed_image.shape[1], step_size)]
        descriptor = sift.compute(processed_image, key_points)
        return key_points, np.array(descriptor[:][1])

    @staticmethod
    def process_img(img):
        """
        Chuyển ảnh sang ảnh xám, cân bằng histogram và resize ảnh
        :param img: Ảnh đầu vào
        :return: Ảnh đã xử lý
        """
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
        img = cv2.resize(img, (80, 80))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = clahe.apply(img)

        return img

    def predict(self, images, step=5):
        """
        Nhận dạng cho ảnh đầu vào
        :param images: Ảnh đầu vào là một list
        :param step: Số bước để chia vùng ảnh lấy dsift
        :return: Nhãn y dự đoán lớp ảnh thuộc về
        """
        if not images:
            return None

        y = []
        for image in images:
            key_points, des = self.getDSift(image, step)
            all_dist = {}
            for label in self.keys:
                dist, ind = self.trees[label].query(X=des, k=1, dualtree=True)
                sum_dist = np.sum(dist)
                all_dist[label] = sum_dist
            y.append(min(all_dist, key=all_dist.get))

        return y

    def construct_kd_tree(self, keys):
        """
        Tạo các cây kd của từng class
        :param keys: Tên các class
        :return: Dict chứa các kd tree của từng class
        """
        kd_trees = {}
        for label in keys:
            class_dsift = self.dsift_file.get(label)
            class_dsift = np.array(class_dsift)
            tree = KDTree(class_dsift, metric="manhattan", leaf_size=2560)
            kd_trees[label] = tree

        return kd_trees
