import cv2
import numpy


imgOne = cv2.imread("one.jpg", cv2.IMREAD_COLOR)
cv2.imshow("img", imgOne)

#Technique 1

#blur and canny edge detector
blurOne =cv2.blur(imgOne, (5,5))
edgesOne = cv2.Canny(blurOne,100,200)

cv2.imshow("edgesOne", edgesOne)




cv2.waitKey(0)
cv2.destroyAllWindows()
