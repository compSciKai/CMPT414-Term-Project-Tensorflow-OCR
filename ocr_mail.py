from os import listdir
import cv2
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
from PIL import Image

# Prediction look up dictionary
letters = { 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j',
11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't',
21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z', 27: 0, 28: 1, 29: 2, 30: 3, 31: 4, 32: 5, 33: 6, 34: 7, 35: 8, 36: 9}

model = tf.keras.models.load_model("modelComb2.h5") #Load Model

img = cv2.imread('address2.jpg')	#Load image
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(imgray,5)
ret, thresh = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

characterSeg = list()
areaList = list()
xlist = list()
ylist =list()
hlist = list()
wlist = list()

for c in contours: # List of all x,y,w,h and Segmenation of characters
    x,y,w,h=cv2.boundingRect(c)
    characterSeg.append(thresh[y:y+h,x:x+w])
    xlist.append([x,thresh[y:y+h,x:x+w]])
    ylist.append(y)
    hlist.append(h)
    wlist.append(w)
    areaList.append(w*h)

#plt.imshow(thresh,'gray')
#plt.show()

maxArea = sorted(areaList)[len(areaList)-1] # second max area in hopes of ignoring outlier (still need better method)
   
for a in range(len(characterSeg)): # Remove obvious outliers (not best method, will need to better method)
	if areaList[a] < maxArea*0.2:
		xlist[a][0]=-1
		ylist[a]=-1
		wlist[a]=-1
		hlist[a]=-1

xlist= list(filter(lambda a: a[0] != -1, xlist))
ylist = list(filter(lambda a: a != -1, ylist))
wlist= list(filter(lambda a: a != -1, wlist))
hlist = list(filter(lambda a: a != -1, hlist))

maxh=max(hlist)
maxy=sorted(ylist)[len(ylist)-1]
miny = sorted(ylist)[1]
aveW = sum(wlist)/len(wlist)
newlist =list()
lines = round(((maxy -miny)/maxh)-0.1)

#print(lines)
dictList = dict()
for l in reversed(range(lines)): # seperating characters based on lines (need better implementation)
	for i in range(len(ylist)):
		if(abs(maxy-ylist[i]-(maxh*l*1.35)) <= maxh*0.4):
			newlist.append([xlist[i],wlist[i]])

	dictList[l] = list(sorted(newlist))
	newlist.clear()

diffDict= dict()
diff = list()
for key in dictList.keys(): # Distance between characters to find obvious spaces between words (Need better method)
	for item in dictList[key]:
		diff.append(item[0][0])
	diff=[j-i for i, j in zip(diff[:-1], diff[1:])]
	diffDict[key] = list(diff)
	diff.clear()


def rgb2gray(rgb): # function to convert from rgb to greyscale
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


predText = list()
wordDict = dict()
	# loop through every line then character and run a prediction on the character
for key in dictList.keys():
	diffCount=-1
	for item in dictList[key]:
		num=1
		rect = item[0][1]
		oldShape = rect.shape
		im = rect.reshape(rect.shape[0],rect.shape[1],1)

			# Reshape image on the x-axis for input (needs to be (1,28,28,1))
		if(oldShape[0]<oldShape[1]):
			ratio = oldShape[1]/28
			newImg=cv2.resize(im,(int(oldShape[1]/ratio),int(oldShape[0]/ratio)))

				# Pad the img on either side if image is still not square
			padnum = int((28-newImg.shape[0])/2)
			newImg = cv2.copyMakeBorder(newImg, 0+padnum, 0+padnum, 0, 0, cv2.BORDER_CONSTANT,value=0)
			while(newImg.shape[0]<28):
				newImg = cv2.copyMakeBorder(newImg, 1, 0, 0, 0, cv2.BORDER_CONSTANT,value=0)
			while(newImg.shape[1]<28):
				newImg = cv2.copyMakeBorder(newImg, 0, 0, 1, 0, cv2.BORDER_CONSTANT,value=0)

		else:	# Reshape image on the y-axis for input (needs to be (1,28,28,1))
			ratio = oldShape[0]/28

			newImg=cv2.resize(im,(int(oldShape[1]/ratio),int(oldShape[0]/ratio)))
				# Pad the img on either side if image is still not square
			padnum = int((28-newImg.shape[1])/2)
			newImg = cv2.copyMakeBorder(newImg, 0, 0, 0+padnum, 0+padnum, cv2.BORDER_CONSTANT,value=0)
			while(newImg.shape[1]<28):
				newImg = cv2.copyMakeBorder(newImg, 0, 0, 1, 0, cv2.BORDER_CONSTANT,value=0)
			while(newImg.shape[0]<28):
				newImg = cv2.copyMakeBorder(newImg, 1, 0, 0, 0, cv2.BORDER_CONSTANT,value=0)

			# convert new cv2 img to numpy array for input into model for prediction
		predictImg=Image.fromarray(cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB))
		predictImg = np.array(predictImg,np.float32)
		predictImg = rgb2gray(predictImg)		
		predictImg=predictImg.reshape(1,28,28, 1)		
		predictImg /= 255.

			# Predict character
		prediction= np.argmax(model.predict(predictImg)[0])

			# Add a blank space at obious space
		if(diffDict[key][diffCount]>aveW*2):
			predText.append(' ')

			# Look up precited character in Lookup Dictionary
		predText.append(str(letters[prediction+1]))
		diffCount += 1

			#Preview each extracted character 
		# cv2.imshow("i",predictImg.reshape(28,28))
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
	wordDict[key]=str(''.join(predText))
	predText.clear()

for key in wordDict.keys():
	print(wordDict[key])
