import cv2
img_rgb = cv2.imread('frame_29.jpg')
img_gray =img_rgb[:,:,2]
w,h = img_gray.shape[::-1]
img_gray = img_gray[int(h*.75):h,0:w]
cv2.imwrite('frame_29.jpg',img_gray)