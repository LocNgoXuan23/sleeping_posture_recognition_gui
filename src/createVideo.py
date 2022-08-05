import cv2
import os

if __name__ == '__main__':
    path = 'imgs'

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter('video.avi', fourcc, 1, (160, 120))

    imgNames = os.listdir(path)
    for imgName in imgNames:
        print(imgName)
        img = cv2.imread(os.path.join(path, imgName))
        video.write(img)


    cv2.destroyAllWindows()
    video.release()