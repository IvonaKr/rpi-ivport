#!/usr/bin/env python

import rospy
import ivport
import cv2
import numpy as np
import time
import os, shutil
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


def empty_folder(folder):  #folder path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try :
            if os.path.isfile(file_path) or ps.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree (file_path)
        except Exception as e :
            print('Faild to delete %s. Reason : %s' %(file_path,e))



def main():
    pub1 = rospy.Publisher('camera_topic1', Image, queue_size=10) #2 topica
    pub2 = rospy.Publisher('camera_topic2', Image, queue_size =10)
    rospy.init_node('camera_publish_node', anonymous=True)
    rate = rospy.Rate(5) #vise, brze
    bridge = CvBridge()

    iv = ivport.IVPort(ivport.TYPE_DUAL2)
    iv.camera_open(camera_v2=True) #za sequenace camera_v2 = True
    i = 0



    #pogledaj u camera_publish_node.launch, ne kuzim zakaj ovo ne radi
    #dir = rospy.get_param('~dir')
    #print(dir) #/home/ivona-rpi/proba_ws/src/paket
    #dir = dir+'/'
    #print(dir) #/home/ivona-rpi/proba_ws/src/paket/


    dir = '/home/ivona-rpi/proba_ws/src/rpi-ivport/'


    #stvaranje foldera cam1_frames i cam2_frames, brisanje nakon svakog pokretanja

    for j in range(1,3):
        if not os.path.exists(dir+'/cam'+str(j)+'_frames'):
            os.makedirs(dir+'/cam'+str(j)+'_frames')
        else :
             empty_folder(dir+'/cam'+str(j)+'_frames')




    while not rospy.is_shutdown():

        iv.camera_change(1)
        iv.camera_capture('picam',use_video_port = True)
        image = cv2.imread(dir+'/src/picam_CAM1.jpg')
        cv2.imwrite(dir +'/cam1_frames/'+str(i)+'.jpg',image)
        #print(image.shape) #480x720x3
        #print(image.dtype) #uint8
        image = np.uint8(image)

        image_message = bridge.cv2_to_imgmsg(image,encoding="passthrough")
        rospy.loginfo(image)
        pub1.publish(image_message)
        print('I publish1')
        rate.sleep()



        iv.camera_change(2)
        iv.camera_capture('picam',use_video_port = True)
        image = cv2.imread(dir+'/src/picam_CAM2.jpg')
        cv2.imwrite(dir+'/cam2_frames/'+str(i)+'.jpg',image)
        image = np.uint8(image)

        image_message = bridge.cv2_to_imgmsg(image,encoding="passthrough")
        rospy.loginfo(image)
        pub2.publish(image_message)
        print('I publish2')
        rate.sleep()

        i +=1

    iv.close()


if __name__ == "__main__":
    try :
        main()
    except rospy.ROSInterruptException:
        pass
