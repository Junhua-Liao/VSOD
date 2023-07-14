import os
import cv2
import numpy as np

def calculate_SoU(depth_path):

    video_list = sorted(os.listdir(depth_path))
    num = 1
    for video_index in video_list:

        if num == 3 or num == 31:
            fps = 23
        else:
            fps = 25

        if not os.path.exists('result/'):
            os.makedirs('result/')
            
        file = open('result/' + video_index + '_' + str(fps) + '.txt', 'a')
        frame_list = sorted(os.listdir(os.path.join(depth_path, video_index)))
        
        result = []
        second = []
        second1 = []

        for frame_index in frame_list:

            print(video_index, frame_index)

            if frame_index[0] == '.':
                pass

            frame = cv2.imread(os.path.join(depth_path, video_index, frame_index), cv2.IMREAD_GRAYSCALE)
            frame = cv2.resize(frame, (192,192))
            second.append(frame.copy())

            if len(second) == fps:

                for i in range(fps):

                    current_frame = np.zeros((192, 192))
                    ret, th = cv2.threshold(second[i], 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    current_frame = (second[i] > ret)
                    second1.append(current_frame.copy())
                     
                sou_y = np.sum(sum(second1) != 0) 

                for i in range(len(second1)):           

                    sou_x = np.sum(second1[i] == 1)
                    result.append(sou_x / sou_y)
                
                second.clear()
                second1.clear()

        if len(second) != 0:
            
            for i in range(len(second)):

                current_frame = np.zeros((192, 192))
                ret, th = cv2.threshold(second[i], 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                current_frame = (second[i] > ret)
                second1.append(current_frame.copy())

            sou_y = np.sum(sum(second1) != 0)

            for i in range(len(second1)):           

                sou_x = np.sum(second1[i] == 1)
                result.append(sou_x / sou_y)

            second.clear()
            second1.clear()

        num += 1
                
        for j in range(len(result)):
            file.write(str(result[j]) + ',')
        file.close()
    
