import cv2

rect1 = ((0, 0), (1, 1), 45)
rect2 = ((1.5, 0), (4, 3), 0)
r1 = cv2.rotatedRectangleIntersection(rect1, rect2)
print(r1)
