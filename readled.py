import cv2
import matplotlib.pyplot as plt
import numpy as np

class LED_Detect():
    def __init__(self) -> None:
        self.img_diff = []

        self.img_led_on = cv2.imread("./save.jpg")
        self.img_led_off = cv2.imread("./save2.jpg")
        self.run()

    def diff(self):
        m1 = np.max(self.img_led_on,2)
        m2 = np.max(self.img_led_off,2)
        diff = self.img_led_on-self.img_led_off
        var_d = np.var(diff[:])
        mask = m1>3*var_d

        gimg = img*0.5
        for i in range(0, 3):
            tmp = gimg[:,:,i]
            tmp2 = img[:,:,i]
            tmp[mask] = tmp2[mask]
            gimg[:,:,i ]= tmp    

        self.img_diff = gimg

    def run(self):
        pass

if __name__ == '__main__':
    img = cv2.imread("./save.jpg")
    img2 = cv2.imread("./save2.jpg")

    m1 = np.max(img,2)
#    print(m1.dtype)
    m2 = np.max(img2,2)
    diff = img2-img
    var_d = np.var(diff[:])
#    print(diff)
    mask = m1>3*var_d
#    print(mask.shape)

    gimg = img*0.5
    for i in range(0, 3):
#        print(i)
        tmp = gimg[:,:,i]
        tmp2 = img[:,:,i]
        tmp[mask] = tmp2[mask]
        gimg[:,:,i ]= tmp
    # a = np.random.rand(2,3,2)
    # print(a)
    # a = np.max(a, 0)
    # print(a)
#    img3 = cv2.cvtColor(gimg,cv2.COLOR_BGR2GRAY)
#    cv2.imshow("image", gimg)
    gimg = gimg.astype(np.float32)
    gimg1 = cv2.cvtColor(gimg, cv2.COLOR_BGR2GRAY)
    ret,gimg2=cv2.threshold(gimg1,76,255,3) 
#    cv2.imshow("gimg", gimg1)
    
    kernel = np.ones((3, 3), np.uint8)  
    opening = cv2.morphologyEx(gimg2, cv2.MORPH_OPEN, kernel)
#    opening1 = cv2.fastNlMeansDenoising(opening, None, 10, 10, 7, 21)
    print(opening.shape)
    cv2.imshow("image3", opening)
    ss = np.hstack((gimg1, opening))
#    print(diff.shape)
    ret,diff1=cv2.threshold(diff,127,255,cv2.THRESH_BINARY) 
#    cv_show(ss)

    cv2.imshow("image3", ss)
    opening = opening.astype(np.uint8)

    # print(type()))
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):
        # 是否为凸包
        ret = cv2.isContourConvex(contours[c])
        # 凸包检测
        points = cv2.convexHull(contours[c])
        total = len(points)
        for i in range(len(points)):
            x1, y1 = points[i % total][0]
            x2, y2 = points[(i+1) % total][0]
            cv2.circle(img, (x1, y1), 4, (255, 0, 0), 2, 8, 0)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2, 8, 0)
        print(points)
        print("convex : ", ret)

#    cv2.imshow("image3", mask)
#    plt.hist(img.ravel(), 256)
#    plt.show()
    cv2.imshow("image1", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
