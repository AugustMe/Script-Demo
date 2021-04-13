import glob
import random
import xml.etree.ElementTree as ET
import numpy as np
import math


# load_data() 加载数据，获取宽高
def load_data(path):
    data = []
    # 对于每一个xml都寻找box
    for xml_file in glob.glob('{}/*xml'.format(path)):
        tree = ET.parse(xml_file)
        height = int(tree.findtext('./size/height'))
        width = int(tree.findtext('./size/width'))
        if height <= 0 or width <= 0:
            continue

        # 对于每一个目标都获得它的宽高
        for obj in tree.iter('object'):
            xmin = int(float(obj.findtext('bndbox/xmin'))) / width
            ymin = int(float(obj.findtext('bndbox/ymin'))) / height
            xmax = int(float(obj.findtext('bndbox/xmax'))) / width
            ymax = int(float(obj.findtext('bndbox/ymax'))) / height

            xmin = np.float64(xmin)
            ymin = np.float64(ymin)
            xmax = np.float64(xmax)
            ymax = np.float64(ymax)
            # 得到宽高
            data.append([xmax - xmin, ymax - ymin])
    return np.array(data) # 此时np.array(data)中存放的是数据所有框的宽高


def kmeans(boxes, k, dist=np.median):
    rows = boxes.shape[0]
    print("total box:", rows)

    distances = np.empty((rows, k))
    last_clusters = np.zeros((rows,))

    np.random.seed()

    # the Forgy method will fail if the whole array contains the same rows
    clusters = kpp_centers(boxes, k)
    # print("clusters:", clusters)
    clusters = np.array(clusters)
    #clusters = boxes[np.random.choice(rows, k, replace=False)] 这是K-means的，两个切换注释下就行了

    while True:
        for row in range(rows):
            distances[row] = 1 - iou(boxes[row], clusters)  # iou很大则距离很小
        # 对每个标注框选择与其距离最接近的集群中心的标号作为所属类别的编号。
        nearest_clusters = np.argmin(distances, axis=1)     # axis=1表示沿着列的方向水平延伸

        if (last_clusters == nearest_clusters).all():
            break

        for cluster in range(k):
            clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)    # 给每类算均值新中心点
            '''
            利用与第几个点距离最小的框求均值得到聚类结果，如现在求第一个anchor box，
            那么就取出nearest_clusters == 0的box，因为这些box是与第一个中心点距离最近的(nearest_clusters)=0
            然后利用均值，求出新的中心点
            '''

        last_clusters = nearest_clusters
        # print("clusters:",clusters)
    # print("clusters:", clusters)
    return clusters


def get_closest_dist(point, centroids):
    min_dist = math.inf  # 初始设为无穷大
    # print(centroids)
    for i, centroid in enumerate(centroids):
        # print(centroids)
        dist = 1 - iou_kpp(point, centroid)		# 点和当前每个中心点进行计算距离
        if dist < min_dist:
            min_dist = dist		# 注意我K-means++博客中的这句“指该点离中心点这一数组中所有中心点距离中的最短距离”
    return min_dist


def kpp_centers(data_set: list, k: int) -> list:
    """
    从数据集中返回 k 个对象可作为质心
    """
    cluster_centers = []
    cluster_centers.append(random.choice(data_set))
    # print("cluster_centers:", cluster_centers)
    d = [0 for _ in range(len(data_set))]
    #print(d)
    for _ in range(1, k):
        total = 0.0
        for i, point in enumerate(data_set):
            d[i] = get_closest_dist(point, cluster_centers) # 与最近一个聚类中心的距离
            total += d[i]
        total *= random.random()
        for i, di in enumerate(d): # 轮盘法选出下一个聚类中心；
            total -= di
            if total > 0:
                continue
            cluster_centers.append(data_set[i])
            # print("cluster_centers:", cluster_centers)
            break
    return cluster_centers


def iou(box, clusters):
    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])

    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]

    # iou_ = np.true_divide(intersection, box_area + cluster_area - intersection + 1e-10)
    iou_ = intersection / (box_area + cluster_area - intersection + 1e-10)

    return iou_


def avg_iou(boxes, clusters):
    return np.mean([np.max(iou(boxes[i], clusters)) for i in range(boxes.shape[0])])


def iou_kpp(box, clusters):
    x = np.minimum(clusters[0], box[0])
    y = np.minimum(clusters[1], box[1])

    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")

    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[0] * clusters[1]

    # iou_ = np.true_divide(intersection, box_area + cluster_area - intersection + 1e-10)
    iou_ = intersection / (box_area + cluster_area - intersection + 1e-10)

    return iou_


####### load_data() 加载数据，获取宽高 ######
def load_data(path):
    data = []
    # 对于每一个xml都寻找box
    for xml_file in glob.glob('{}/*xml'.format(path)):
        tree = ET.parse(xml_file)
        height = int(tree.findtext('./size/height'))
        width = int(tree.findtext('./size/width'))
        if height <= 0 or width <= 0:
            continue

        # 对于每一个目标都获得它的宽高
        for obj in tree.iter('object'):
            xmin = int(float(obj.findtext('bndbox/xmin'))) / width
            ymin = int(float(obj.findtext('bndbox/ymin'))) / height
            xmax = int(float(obj.findtext('bndbox/xmax'))) / width
            ymax = int(float(obj.findtext('bndbox/ymax'))) / height

            xmin = np.float64(xmin)
            ymin = np.float64(ymin)
            xmax = np.float64(xmax)
            ymax = np.float64(ymax)
            # 得到宽高
            data.append([xmax - xmin, ymax - ymin])
    return np.array(data)   # 此时np.array(data)中存放的是数据所有框的宽高


if __name__ == '__main__':
    # 运行该程序会计算'./VOCdevkit/VOC2007/Annotations'的xml
    # 会生成yolo_anchors.txt
    SIZE = 416
    anchors_num = 9
    # 载入数据集，可以使用VOC的xml
    path = r'./VOCdevkit/VOC2007/Annotations'

    # 载入所有的xml
    # 存储格式为转化为比例后的width,height
    data = load_data(path)
    # print("=====data=====")
    # print(data)

    # 使用kmeans++聚类算法
    out = kmeans(data, anchors_num)

    out = out[np.argsort(out[:, 0])]

    print('acc:{:.2f}%'.format(avg_iou(data, out) * 100))
    out = out*SIZE
    print(out)
    f = open("yolo_kmeanspp_anchors.txt", 'w')
    row = np.shape(out)[0]
    for i in range(row):
        if i == 0:
            x_y = "%d,%d" % (out[i][0], out[i][1])
        else:
            x_y = ", %d,%d" % (out[i][0], out[i][1])
        f.write(x_y)
    f.close()