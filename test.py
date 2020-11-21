'''test.py'''
import cv2
import numpy


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
    kernel = numpy.ones((5, 5), numpy.int8)

    old_img = cv2.imread(arg)
    #  img = cv2.resize(old_img, (old_img.shape[1]/2, old_img.shape[0]/2))
    img = cv2.resize(
        old_img, (int(old_img.shape[1]/2), int(old_img.shape[0]/2)))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)              # 灰色
    img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)              # 模糊
    img_canny = cv2.Canny(img, 100, 100)                          # 描边
    img_dialation = cv2.dilate(img_canny, kernel, iterations=1)   # 扩张
    img_eroded = cv2.erode(img_dialation, kernel, iterations=1)   # 侵蚀

    cv2.imshow("gray_image", img_gray)
    cv2.waitKey(0)
    cv2.imshow("blur_image", img_blur)
    cv2.waitKey(0)
    cv2.imshow("canny_image", img_canny)
    cv2.waitKey(0)
    cv2.imshow("dialation_image", img_dialation)
    cv2.waitKey(0)
    cv2.imshow("eroded_image", img_eroded)
    cv2.waitKey(0)


def test_size(arg: str):
    '''test_size'''
    img = cv2.imread(arg)
    img_resized = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))
    print(img_resized.shape)
    img_cropped = img_resized[100:200, 200:300]

    cv2.imshow("image resized", img_resized)
    cv2.waitKey(0)
    cv2.imshow("image cropped", img_cropped)
    cv2.waitKey(0)


def test_draw(arg: str):
    '''test_draw'''
    img = numpy.zeros((512, 512, 3), numpy.uint8)
    #  print(img.shape)
    #  img[:] = 255, 0, 0

    cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
    cv2.rectangle(img, (0, 0), (250, 350), (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (450, 50), 30, (255, 255, 0), 5)
    cv2.putText(img, "ONLY SHIT!", (300, 100),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 2)

    cv2.imshow("image", img)
    cv2.waitKey(0)


def test_repeat(arg: str):
    '''test_repeat'''
    img = cv2.imread(arg)
    img_hor = numpy.hstack((img, img))
    img_ver = numpy.vstack((img, img))

    cv2.imshow("Horizontal img", img_hor)
    cv2.waitKey(0)
    cv2.imshow("Vertical img", img_ver)
    cv2.waitKey(0)


def empty(_):
    '''pass'''


def test_color(arg: str):
    '''test_color'''
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)

    img = cv2.imread(arg)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow("image", img_hsv)
    cv2.waitKey(0)


def test_face(arg: str):
    '''test_face'''
    face_cascade = cv2.CascadeClassifier(
        "resources/xml/haarcascade_frontalface_default.xml")
    img = cv2.imread(arg)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 2, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    img_resized = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))
    cv2.imshow("face img", img_resized)
    cv2.waitKey(0)


if __name__ == "__main__":
    #  test_img("resources/img/ml.jpg")
    test_video("resources/video/sese.mp4")
    #  test_net_video()
    #  test_gray("resources/img/cb.jpg")
    #  test_size("resources/img/cb.jpg")
    #  test_draw("resources/img/cb.jpg")
    #  test_repeat("resources/img/ml.jpg")
    #  test_color("resources/img/ml.jpg")
    #  test_face("resources/img/ml.jpg")
