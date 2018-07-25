import cv2
import numpy as np
from random import randint

#CONST
height = 107
width = 57
number = 4 
english_num= 3
interval = 8

#english_map = dict(zip((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25),('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')))
num_map = dict(zip((0,1,2,3,4,5,6,7,8),('0','1','2','3','5','6','7','8','9')))

english_map = dict(zip((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23),('A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z')))

cha_map = dict(zip((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35),('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' , '0','1','2','3','4','5','6','7','8','9')))

resize_zoom = 0.2

def Create_blank(width, height, rgb_color=(255, 255, 255)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

def GetRandNum(number,digist=True):
    randnum = []
    if digist:
        for i in range(number):
            randnum.append(num_map[randint(0,8)])
        return randnum
    #english
    else:
        for i in range(number):
            randnum.append(english_map[randint(0,23)])
        return randnum

def GetRandCha(number):
    randcha = []
    for i in range(number):
        randcha.append(cha_map[randint(0,35)])
    return randcha

def CombineImage(blank,element,name):
    w1_start = 0
    for i in range(len(element)):
        element_img = cv2.imread('data/'+element[i]+'.jpg')
        h1,w1,_ = element_img.shape
        blank[:h1 , w1_start : w1_start + w1 ,:3] = element_img
        w1_start = w1_start +w1
        if i != len(element) - 1 :
            blank[:h1 , w1_start:w1_start + interval,:3] = Create_blank(interval,h1)
            w1_start = w1_start + interval
    #cv2.imshow(name,blank)
    return blank

# add the white interval at the img up and down
def Addhat(img,interval):
    (h,w) = img.shape[:2]
    blank = Create_blank(w,h+2*interval)# Create a white space
    blank[interval:h + interval,:w,:3] = img
    return blank

def CombineTwoImage(img1,img2):
    h1,w1,_ = img1.shape
    h2,w2,_ = img2.shape
    blank_image =  Create_blank(w1+w2,h1)
    blank_image[:h1,:w1,:3] = img1
    blank_image[:h2,w1:w1+w2,:3] = img2
    #cv2.imshow("CombineTwo",blank_image)
    #cv2.imwrite("/home/wan/Desktop/ITRI_INTERN/SplitEnglish/combinetwo.jpg" , blank_image)
    return blank_image

def ClearCombineImage(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # change the image to gray image
    ret,binary = cv2.threshold(gray,230,255,cv2.THRESH_BINARY) # change the image to black and write
    #binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
 #   _ , contours, hierarchy  =  cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 #   print(len(contours))
 #   cv2.drawContours(img,contours,-1,(0,0,0),1)  
    #cv2.imshow("img", binary)  
    cv2.waitKey(0) 


def Resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h,w) = img.shape[:2]
    if width == None:
        r = height/float(h)
        dim = (int(w * r), height)
    else:
        r= width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(img, dim, interpolation=inter)
    return resized
def AffineImage(img,name):
    r,c = img.shape[:2]
    pts1 = np.float32([[0,0],[0,165],[650,0]])
    pts2 = np.float32([[0,50],[30,150],[500,25]])
    M = cv2.getAffineTransform(pts1,pts2)
    res = cv2.warpAffine(img,M,(1000,400))
    #cv2.imshow(name,res)
def PerspectiveImage(img,name):
    img1 = np.float32([[0,0],[0,165],[650,0],[650,165]])
    img2 = np.float32([[0,0],[0,165],[600,25],[600,125]])
    h , mask = cv2.findHomography(img1,img2)
    out = cv2.warpPerspective(img,h,(800,800))
    #cv2.imshow(name,out)

    

