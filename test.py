import os
import math
import label_VSOD2
import numpy as np
from SoU import calculate_SoU
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


def file_pretreatment(file_name):

    file = open(file_name, 'r')
    fps = int(file_name[-6:-4])

    result = file.readline()
    result = result.split(',')
    result_array = np.zeros(len(result) - 1)
    for i in range(len(result) - 1):
        result_array[i] = float(result[i])
    file.close()

    return result_array, fps


def calculate_threshold(result, fps):
    
    max_value = max(result)
    min_value = min(result)
    mean_value = np.mean(result)
    length = math.ceil(len(result) / fps) / 60
    mid_value = (max_value + min_value) / 2

    min_t = min(mean_value, mid_value)
    max_t = max(mean_value, mid_value)

    a = (1 - mean_value) ** length
    
    if min_value > (max_value - 0.1) + 0.1 * a:
        return 0
    else:
        return min_t + (max_t - min_t) * a


def calculate_time_array(result, fps, threshold):

    time_array = np.zeros(math.ceil(len(result) / fps))
    batch = len(result) // fps

    for i in range(batch):
        if sum(result[i*fps : (i+1)*fps] < threshold) > 0:
            time_array[i] = 1

    if len(result) % fps != 0:
        if sum(result[batch*fps :] < threshold) > 0:
            time_array[batch] = 1

    return time_array


def calculate_time_list(time_array):
    time_list = []
    start_time = None
    stop_time = None
    occlusion_switch = False

    for i in range(len(time_array)):
        if time_array[i] == 1:
            if occlusion_switch:
                continue
            else:
                occlusion_switch = True
                start_time = i
        elif time_array[i] == 0:
            if occlusion_switch:
                stop_time = i
                time_list.append(time2str(start_time, stop_time))
                start_time = None
                stop_time = None
                occlusion_switch = False
            else:
                continue
        else:
            print('ERROR!')
    
    if occlusion_switch:
        time_list.append(time2str(start_time, len(time_array) - 1))

    return time_list


def time2str(start, stop):
    region = []
    for time in [start, stop]:
        time_str = ""
        minute = time // 60
        second = time % 60
        if minute < 10:
            time_str = time_str + "0" + str(minute) + ":"
        else:
            time_str = time_str + str(minute) + ":"
        if second < 10:
            time_str = time_str + "0" + str(second)
        else:
            time_str = time_str + str(second)

        region.append(time_str)

    return region


def calculate_label_array(label_list, length):
    start_point = None
    stop_point = None
    label_array = np.zeros(length)
    
    for i in range(len(label_list)):
        start_minute = int(label_list[i][0][:2])
        start_second = int(label_list[i][0][-2:])
        start_point = start_minute * 60 + start_second
        stop_minute = int(label_list[i][1][:2])
        stop_second = int(label_list[i][1][-2:])
        stop_point = stop_minute * 60 + stop_second
        label_array[start_point:stop_point] = 1

    return label_array


def formula_Recall_Event(label, predict, region_num):
    #     predict(+) and label(+) 
    #   ---------------------------
    #            label(+)
    start_point = None
    stop_point = None
    switch = False
    x = 0
    y = 0
    for i in range(len(label)):
        if label[i] == 1:
            if switch:
                continue
            else:
                start_point = i
                switch = True
        elif label[i] == 0:
            if switch:
                stop_point = i
                if sum(predict[start_point:stop_point] * label[start_point:stop_point]) > 0:
                    x += 1
                y += 1
                start_point = None
                stop_point = None
                switch = False
            else:
                continue
        else:
            print('ERROR!')

    if switch:
        if sum(predict[start_point:] * label[start_point:]) > 0:
            x += 1
        y += 1

    assert region_num == y
    
    return x / y


def formula_IoU_Second(label, predict):
    #     predict(+) and label(+) 
    #   ---------------------------
    #     predict(+) or label(+)
    return sum(predict * label) / sum(predict + label > 0) 


def formula_False_Positive_Rate_Second(label, predict):
    #        FP
    #   -----------
    #     FP + TN
    return (sum(predict) - sum(predict * label)) / sum(1 - label)


###########################################################################################################

if __name__ == '__main__':

    depth_path = 'Path/to/Depth_Map'
    calculate_SoU(depth_path)

    label_list = label_VSOD2.label_list

    Recall_Event_list = []
    IoU_Second_list = []
    Accuracy_Second_list = []
    Recall_Second_list = []
    False_Positive_Rate_Second_list = []
    Precision_Second_list = []
    F1_Second_list = []

    result_file_lists = sorted(os.listdir(os.path.join('result')))
   
    for video_id, result_file in enumerate(result_file_lists):

        result, fps = file_pretreatment(os.path.join('result', result_file))

        threshold = calculate_threshold(result, fps)

        predict_arr = calculate_time_array(result, fps, threshold)

        predict_list = calculate_time_list(predict_arr)

        label_arr = calculate_label_array(label_list[video_id], len(predict_arr))

        Recall_Event_list.append(formula_Recall_Event(label_arr, predict_arr, len(label_list[video_id])))
        IoU_Second_list.append(formula_IoU_Second(label_arr, predict_arr))
        Accuracy_Second_list.append(accuracy_score(label_arr, predict_arr))
        Recall_Second_list.append(recall_score(label_arr, predict_arr))
        False_Positive_Rate_Second_list.append(formula_False_Positive_Rate_Second(label_arr, predict_arr))
        Precision_Second_list.append(precision_score(label_arr, predict_arr))
        F1_Second_list.append(f1_score(label_arr, predict_arr))

    print('{0:>15} {1:<20}'.format('Recall_e:', round(np.mean(np.array(Recall_Event_list)), 4)))
    print('{0:>15} {1:<20}'.format('IoU_s:', round(np.mean(np.array(IoU_Second_list)), 4)))
    print('{0:>15} {1:<20}'.format('Accuracy_s:', round(np.mean(np.array(Accuracy_Second_list)), 4)))
    print('{0:>15} {1:<20}'.format('FPR_s:', round(np.mean(np.array(False_Positive_Rate_Second_list)), 4)))
    print('{0:>15} {1:<20}'.format('Recall_s:', round(np.mean(np.array(Recall_Second_list)), 4)))
    print('{0:>15} {1:<20}'.format('Precision_s:', round(np.mean(np.array(Precision_Second_list)), 4)))
    print('{0:>15} {1:<20}'.format('F1_s:', round(np.mean(np.array(F1_Second_list)), 4)))
