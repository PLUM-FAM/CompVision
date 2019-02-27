import cv2
import numpy


blueCount = 0
greenCount = 0
yellowCount = 0
orangeCount = 0
brownCount = 0
redCount = 0
unknownCount = 0


# helper function to increase brightness of a single frame
def increase_brightness(src, value):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    src = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return src

#onclick event function for hsv window
def onClick(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
                print(imgOne[y,x]) #print out color values for current click x,y coords (to help figure out color thresholds)

                #cv2.circle(edgesOne,(x,y),10,(255,255,255), -1) 



imgOne = cv2.imread("one.jpg", cv2.IMREAD_COLOR)


cv2.imshow("img", imgOne)
cv2.setMouseCallback('img',onClick)

#Technique 1:

#increase brightness first?
imgOne= increase_brightness(imgOne,70) #70


#guassian blur (seems to work better) *** 2 blurs works well for img1, 2nd 5x5 mask blur sort of messes up images 3 and 4
blurOne = cv2.GaussianBlur(imgOne,(5,5),0)
blurOne = cv2.GaussianBlur(blurOne,(3,3),0)


#possibly dialating and eroding first
kernel = numpy.ones((5,5),numpy.uint8)

#canny edge detection
edgesOne = cv2.Canny(blurOne,5,150)

cv2.imshow("canny edges", edgesOne)

#finding clircles 
#initally started with: circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
#parameters here: https://docs.opencv.org/3.1.0/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
circles = cv2.HoughCircles(edgesOne,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=25,minRadius=10,maxRadius=40)
#min radius for houghCircles has to be a max of 13, any higher and img1 wont detect
#param 2 = 20 initially, but working better for all images at 25

circles = numpy.uint16(numpy.around(circles))
listOfCircleImages = []
for i in circles[0,:]:
    currentImg = numpy.zeros((imgOne.shape[0],imgOne.shape[1]), numpy.uint8) #current image to be added to list of circle images

    #-1 is to fill in the circles. 255's are for white. i[2]-5 is for drawing 5px smaller than orig circle. ensures circles are not overlapping.
    cv2.circle(currentImg,(i[0],i[1]),i[2]-5,(255,255,255), -1) 
    cv2.circle(edgesOne,(i[0],i[1]),i[2]-5,(255,255,255), -1) #draw one on detected circles window
    listOfCircleImages.append(currentImg)

    cv2.imshow(str(len(listOfCircleImages)), currentImg)#show an individual window for each m&m ##DEBUGING##
    
    #rgb_data = cv2.mean(imgOne, mask=edgesOne)
for img in listOfCircleImages:
    rgb_data = cv2.mean(imgOne, mask=img)
    print(int(rgb_data[0]), int(rgb_data[1]), int(rgb_data[2]))


#ends + 1, because range(start,end) is not inclusive for 'end'
#not in the order of r g b????
#---------------------------------------------
#Blue = [range(254,256), range(170,216), range(0,11)]
#Red = [range(100,151), range(80,121), range(240,251)]
#Yellow = [range(0,51), range(245,256), range(254,256)] 
#Green = [range(130,191), range(254,256), range(0,6)]
#Orange = [range(45,101), range(105,151), range(254,256)]
#Brown = [range(130,201), range(120,181), range(105,161)]
#------------------------------------------

    #check blue
    if(int(rgb_data[0]) in range(254, 256) and int(rgb_data[1]) in range(170, 216) and int(rgb_data[2]) in range(0, 20)):
        blueCount += 1
        print("matched blue")
    #check red
    elif(int(rgb_data[0]) in range(100,151) and int(rgb_data[1]) in range(80,121) and int(rgb_data[2]) in range(240,256)):
        redCount += 1
        print("matched red")
    #check yellow
    elif(int(rgb_data[0]) in range(0,51) and int(rgb_data[1]) in range(245,256) and int(rgb_data[2]) in range(253,256)):
        yellowCount += 1
        print("matched yellow")
    #check green
    elif(int(rgb_data[0]) in range(130,191) and int(rgb_data[1]) in range(254,256) and int(rgb_data[2]) in range(0,6)):
        greenCount += 1
        print("matched green")
    #check orange
    elif(int(rgb_data[0]) in range(45,101) and int(rgb_data[1]) in range(105,151) and int(rgb_data[2]) in range(254,256)):
        orangeCount += 1
        print("matched orange")
    #check brown
    elif(int(rgb_data[0]) in range(130,201) and int(rgb_data[1]) in range(120,181) and int(rgb_data[2]) in range(105,161)):
        brownCount += 1
        print("matched brown")
    else:
        unknownCount += 1
        print("didnt match the above values !!!!")

print(blueCount , " blue")
print(redCount , " red")
print(yellowCount , " yellow")
print(greenCount , " green")
print(orangeCount , " orange")
print(brownCount , " brown")
print(unknownCount, " unknown")





    

cv2.imshow('detected circles',edgesOne)



cv2.waitKey(0)
cv2.destroyAllWindows()
