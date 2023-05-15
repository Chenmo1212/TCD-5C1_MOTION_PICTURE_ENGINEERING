import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt


def eval_single(img1, img2, obj):
    # convert to grayscale image
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculation accuracy
    diff_pixels = np.sum(gray1 != gray2)
    total_pixels = gray1.shape[0] * gray1.shape[1]
    accuracy = (1 - diff_pixels / total_pixels) * 100
    # print('Accuracy:', accuracy)
    obj["accuracy"] += accuracy

    # Calculate the mean squared error (MSE)
    mse = np.mean((gray1 - gray2) ** 2)
    # print('MSE:', mse)
    obj["mse"] += mse

    # Compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")

    # Print the score
    # print("SSIM: {}".format(score))
    obj["ssim"] += score


def evaluate(type_, iter=5, pixel_size=8):
    frame = [47, 48, 49]

    tmp = {"accuracy": 0, "mse": 0, "ssim": 0}
    str_iter = "" if type_ == "ML" else str(iter)
    pixel_path = "" if pixel_size == 8 else ("/" + str(pixel_size) + "/")

    for i in frame:
        # read pictures
        img1 = cv2.imread('Hula.Fore.ACKGT.000' + str(i) + '.png')
        img2 = cv2.imread("../" + type_ + "/" + pixel_path + type_ + "_res" + str_iter + ".00" + str(i) + ".png")

        eval_single(img1, img2, tmp)

    print(type_, "iter: ", iter, ": ")
    for key in tmp:
        tmp[key] = tmp[key] / len(tmp)
        print(key, ":", tmp[key])
    print()
    return tmp


def show_3_5():
    ML = evaluate("ML")
    MRF_3D_3 = evaluate("3D", 3)
    MRF_3D_5 = evaluate("3D", 5)
    MRF_motion_3 = evaluate("motion", 3)
    MRF_motion_5 = evaluate("motion", 5)
    MRF_2D_3 = evaluate("2D", 3)
    MRF_2D_5 = evaluate("2D", 5)

    obj_list = [ML, MRF_3D_3, MRF_3D_5, MRF_motion_3, MRF_motion_5, MRF_2D_3, MRF_2D_5]
    str_obj_list = ['ML', 'MRF_2D_3', 'MRF_2D_5', 'MRF_3D_3', 'MRF_3D_5', 'MRF_motion_3', 'MRF_motion_5']

    # Create a list to store the accuracy, mse, ssim of each object
    accuracy_list = []
    mse_list = []
    ssim_list = []

    # Traverse the dictionary and add the accuracy, mse, ssim of each object to the list
    for obj in obj_list:
        accuracy_list.append(obj['accuracy'])
        mse_list.append(obj['mse'])
        ssim_list.append(obj['ssim'])

    # 设置图表的x轴和y轴
    x_label = str_obj_list
    y_label = [accuracy_list, mse_list, ssim_list]

    # 创建一个图表
    fig = plt.figure(figsize=(10, 10))
    plt.title('Performance comparison of different algorithms')

    # 将图表转换为3个子图
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    # 绘制3条折线图
    ax1.plot(x_label, accuracy_list, 'r-', label='accuracy')
    ax2.plot(x_label, mse_list, 'g-', label='mse')
    ax3.plot(x_label, ssim_list, 'b-', label='ssim')

    # 添加图表的x轴和y轴标签
    ax1.set_xlabel('Objects')
    ax1.set_ylabel('Accuracy')
    ax2.set_xlabel('Objects')
    ax2.set_ylabel('MSE')
    ax3.set_xlabel('Objects')
    ax3.set_ylabel('SSIM')

    # 添加图表的图例
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    ax3.legend(loc='upper right')

    # 显示图表
    plt.show()


def show_iters():
    MRF_2D_1 = evaluate("2D", 1)
    MRF_2D_2 = evaluate("2D", 2)
    MRF_2D_3 = evaluate("2D", 3)
    MRF_2D_4 = evaluate("2D", 4)
    MRF_2D_5 = evaluate("2D", 5)

    MRF_3D_1 = evaluate("3D", 1)
    MRF_3D_2 = evaluate("3D", 2)
    MRF_3D_3 = evaluate("3D", 3)
    MRF_3D_4 = evaluate("3D", 4)
    MRF_3D_5 = evaluate("3D", 5)

    MRF_3D_MC_1 = evaluate("motion", 1)
    MRF_3D_MC_2 = evaluate("motion", 2)
    MRF_3D_MC_3 = evaluate("motion", 3)
    MRF_3D_MC_4 = evaluate("motion", 4)
    MRF_3D_MC_5 = evaluate("motion", 5)

    MRF_2D_list = [MRF_2D_1, MRF_2D_2, MRF_2D_3, MRF_2D_4, MRF_2D_5]
    MRF_3D_list = [MRF_3D_1, MRF_3D_2, MRF_3D_3, MRF_3D_4, MRF_3D_5]
    MRF_3D_MC_list = [MRF_3D_MC_1, MRF_3D_MC_2, MRF_3D_MC_3, MRF_3D_MC_4, MRF_3D_MC_5]
    str_obj_list = ['MRF_2D_1', 'MRF_2D_2', 'MRF_2D_3', 'MRF_2D_4', 'MRF_2D_5']

    # Create a list to store the accuracy, mse, ssim of each object
    MRF_2D_accuracy_list = []
    MRF_3D_accuracy_list = []
    MRF_3D_MC_accuracy_list = []

    # Traverse the dictionary and add the accuracy, mse, ssim of each object to the list
    for i in range(5):
        MRF_2D_accuracy_list.append(MRF_2D_list[i]['accuracy'])
        MRF_3D_accuracy_list.append(MRF_3D_list[i]['accuracy'])
        MRF_3D_MC_accuracy_list.append(MRF_3D_MC_list[i]['accuracy'])

    # 设置图表的x轴和y轴
    x_label = [1,2,3,4,5]
    y_label = [MRF_2D_accuracy_list]

    # 创建一个图表
    fig = plt.figure(figsize=(10, 3))
    plt.title('Performance comparison of different algorithms')

    # 绘制3条折线图
    fig.plot(x_label, MRF_2D_accuracy_list, 'r-', label='MRF_2D')
    fig.plot(x_label, MRF_3D_accuracy_list, 'g-', label='MRF_3D')
    fig.plot(x_label, MRF_3D_MC_accuracy_list, 'b-', label='MRF_3D_MC')

    # 添加图表的x轴和y轴标签
    fig.set_xlabel('Objects')
    fig.set_ylabel('Accuracy')
    # ax2.set_xlabel('Objects')
    # ax2.set_ylabel('MSE')
    # ax3.set_xlabel('Objects')
    # ax3.set_ylabel('SSIM')

    # 添加图表的图例
    fig.legend(loc='upper right')
    # ax2.legend(loc='upper right')
    # ax3.legend(loc='upper right')

    # 显示图表
    plt.show()


def show_pixels():
    MRF_3D_p8 = evaluate("3D", 5)
    MRF_3D_p4 = evaluate("3D", 5, 4)
    MRF_3D_p15 = evaluate("3D", 5, 15)

    accuracy = []

    # Traverse the dictionary and add the accuracy, mse, ssim of each object to the list
    accuracy.append(MRF_3D_p4['accuracy'])
    accuracy.append(MRF_3D_p8['accuracy'])
    accuracy.append(MRF_3D_p15['accuracy'])

    # 设置图表的x轴和y轴
    x_label = [4,8,15]
    y_label = [accuracy]

    # 创建一个图表
    fig = plt.figure(figsize=(10, 4))
    plt.title('In addition, the relationship between the number of pixels used and the accuracy based on the MRF_3D algorithm is also explored. It can be clearly found from Figure 3 that as the number of pixels used increases, the accuracy of the algorithm will be higher.')

    plt.plot(x_label, accuracy, 'r-', label='MRF_3D')

    # 添加图表的x轴和y轴标签
    plt.xlabel('Pixel Size')
    plt.ylabel('Accuracy')
    # ax2.set_xlabel('Objects')
    # ax2.set_ylabel('MSE')
    # ax3.set_xlabel('Objects')
    # ax3.set_ylabel('SSIM')

    # 添加图表的图例
    plt.legend(loc='upper right')
    # ax2.legend(loc='upper right')
    # ax3.legend(loc='upper right')

    # 显示图表
    plt.show()


if __name__ == '__main__':
    # # read pictures
    # img1 = cv2.imread('Hula.Fore.ACKGT.00047.png')
    # # img2 = cv2.imread('ML_res.0047.png')
    # img2 = cv2.imread('Motion_res5.0047.png')

    # show_3_5()

    # show_iters()

    show_pixels()




