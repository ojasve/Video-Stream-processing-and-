import cv2
import numpy as np
import os
import time
import sys
sys.stdout.flush()
import sqlite3
import datetime
import random
from time import gmtime, strftime,localtime


conn = sqlite3.connect('Traf_capcaity.db')     #connect a SQLite DB on Raspberry Pi named "Traf_capacity"
c = conn.cursor()							   # connect to the sqllite db	

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS traffic_c(datestamp TEXT, Capacity REAL)") 

create_table()


def dynamic_data_entry(Capacity):

    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

    c.execute("INSERT INTO traffic_c (datestamp, Capacity) VALUES (?, ?)",
          (date, Capacity))

    conn.commit()







Total_time = 2*60
#Total_time = 1*60
Time_interval=30




# Image Handling and Processing
#=====================================================
save=False
SHAPE = (1080, 1920)

AREA_PTS = np.array([[100, 1080], [1850, 1080], [1850, 200], [100, 200]]) 
EXIT_COLOR = (66, 183, 42)
L=[]
time_1=[]
base = np.zeros(SHAPE + (3,), dtype='uint8')
area_mask = cv2.fillPoly(base, [AREA_PTS], (255, 255, 255))[:, :, 0]
#==============================================================



def detect_cap(frame_c,ret):
	i=1
	# for i in range (0,(no_files)):
	if ret == True:
		img=frame_c	
		# img=cv2.imread(directory+lst[i])
		# time.append(lst[i][0:19])
		# #print('Curret frame',lst[i])
		# #img=cv2.imread('C:\\Users\\ojasves\\Desktop\\Ax\\imgaes_from_vid\\data\\frame{}.jpg'.format(str(i)))
		# # print("Shape of current frame",img.shape)

		# cv2.imshow('image',img)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		#=======================================================

		#localtime = time.asctime( time.localtime(time.time()) )
		localtime_1=strftime("%Y-%m-%d_%H:%M:%S", localtime())
		print ("Local current time :", localtime_1, flush=True)
		# time_1.append(localtime_1)

		# print(localtime)
		# cv2.imwrite('pic{:>05}.jpg'.format(i), img)
		# i+=1
		#======================================================

		frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
		cl1 = clahe.apply(frame)
		edges = cv2.Canny(frame,50,70)
		edges = ~edges

		blur = cv2.bilateralFilter(cv2.blur(edges,(21,21), 100),9,200,200)


		
		_, threshold = cv2.threshold(blur,230, 255,cv2.THRESH_BINARY)
	        
		t = cv2.bitwise_and(threshold,threshold,mask = area_mask)  
		free = np.count_nonzero(t) 

		a=np.count_nonzero(area_mask)                   ###################3333
		capacity = 1 - float(free)/a  

		print(capacity,flush=True)

		dynamic_data_entry(capacity)

		#L.append(capacity)

		if save:
			img = np.zeros(img.shape, img.dtype)
			img[:, :] = EXIT_COLOR
			mask = cv2.bitwise_and(img, img, mask=area_mask)
			cv2.addWeighted(mask, 1, img, 1, 0, img)
		            
			fig = plt.figure()
			fig.suptitle("Capacity: {}%".format(capacity*100), fontsize=16)
			plt.subplot(211),plt.imshow(img),plt.title('Original')
			plt.xticks([]), plt.yticks([])
			plt.subplot(212),plt.imshow(t),plt.title('Capacity map')
			plt.xticks([]), plt.yticks([])

			fig.savefig(dir2 + ("/processed_%s.png" % i), dpi=500)
	return None 

cap = cv2.VideoCapture('rtsp://admin:Axcend123@192.168.1.248:554/Streaming/Channels/1/picture')
#cap = cv2.VideoCapture('v10_1.mp4')
ret,_ = cap.read()

data_pts=int(Total_time/Time_interval)
temp=1

currentFrame = 1
fps=cap.get(cv2.CAP_PROP_FPS)
#fps=1
#print(fps)

while(ret):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #frame2=frame
    
    # if currentFrame == fps*Time_interval: 
    #   temp+=1

    print(currentFrame,flush=True)
    temp+=1
    #currentFrame = 1
    detect_cap(frame,ret)	
    currentFrame+=1
    time.sleep(Time_interval)

    if temp==data_pts:
    	break 

    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



		           
# print(len(L))
# print(len(time_1))
# aaa=({'Capacity':L,'time':time_1})
# df=pd.DataFrame(data=[time,L],columns=['time_1','Capacity'])
# df=pd.DataFrame(aaa)
# df.to_csv('test.csv')





# import sys

# def myMethod():
#     i = 0
#     while (i<1000000):
#         i = i+1
#         output_str = str(i) + "\n"
#         sys.stdout.write(output_str)  # same as print
#         sys.stdout.flush()





# def data_entry():
#     c.execute("INSERT INTO stuffToPlot VALUES(1452549219,'2016-01-11 13:53:39','Python',6)")
    
#     conn.commit()
#     c.close()
#     conn.close()


    
# for i in range(10):
#     dynamic_data_entry()
#     time.sleep(1)

c.close
conn.close()