import cv2

foo = cv2.imread("./image1.png")
bar = cv2.imread("./image2.png")

key = cv2.bitwise_xor(foo, bar)
cv2.imshow("xored data", key)
cv2.waitKey(0)