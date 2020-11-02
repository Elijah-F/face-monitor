'''test.py'''
import cv2


def test_img(arg: str):
    '''test_img'''
    img = cv2.imread(arg)
    cv2.imshow("Output", img)
    cv2.waitKey(1000)  # 等待1s按键输入


def test_video(arg: str):
    '''test_video'''
    cap = cv2.VideoCapture(arg)
    while True:
        success, img = cap.read()
        if success:
            cv2.imshow("video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def test_net_video():
    '''test_net_video'''
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)    # 3:宽
    cap.set(4, 480)    # 4:高

    while True:
        success, img = cap.read()
        if success:
            cv2.imshow("video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def test_gray(arg: str):
    '''test_gray'''
    old_img = cv2.imread(arg)
    #  img = cv2.resize(old_img, (old_img.shape[1]/2, old_img.shape[0]/2))
    img = cv2.resize(
        old_img, (int(old_img.shape[1]/2), int(old_img.shape[0]/2)))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)
    img_canny = cv2.Canny(img, 100, 100)
    cv2.imshow("gray_image", img_gray)
    cv2.waitKey(0)
    cv2.imshow("blur_image", img_blur)
    cv2.waitKey(0)
    cv2.imshow("canny_image", img_canny)
    cv2.waitKey(0)


if __name__ == "__main__":
    #  test_img("resources/img/ml.jpg")
    #  test_video("resources/video/sese.mp4")
    #  test_net_video()
    test_gray("resources/img/cb.jpg")
