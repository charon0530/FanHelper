import cv2


def trans_sec(hour, min, sec):
    return int(360*hour + 60*min + sec)


video_path = 'bts.mp4'
cap = cv2.VideoCapture(video_path)
print('video width :', cap.get(cv2.CAP_PROP_FRAME_WIDTH), 'video height :', cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_width = input('input width ')
output_height = input('input height ')
output_size = (int(output_width), int(output_height))#375 667

fourcc= cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
if not cap.isOpened():
    exit()

tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerCSRT_create()
#tracker = cv2.TrackerMOSSE_create()
frame_count = 0
start_time_h, start_time_m, start_time_s = map(int, input('START TIME ').split(':'))
end_time_h, end_time_m, end_time_s = map(int, input('END TIME ').split(':'))
START_SEC = trans_sec(start_time_h, start_time_m, start_time_s)
END_SEC = trans_sec(end_time_h, end_time_m, end_time_s)
roi_set_flag = False
ready_flag = False
check_mode = True #false면 빠름

while True:
    frame_count += 1
    ret, img = cap.read()
    if not ret:
        print('cant capture')
        exit()

    elif frame_count == START_SEC * round(cap.get(cv2.CAP_PROP_FPS)):  # 시작프레임
        ret, img = cap.read()
        cv2.namedWindow('Select Window')
        cv2.imshow('Select Window', img)

        # ROI(region of interest)설정
        rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow('Select Window')
        roi_set_flag = True
        tracker.init(img, rect)
        ready_flag = True
    elif frame_count == END_SEC * round(cap.get(cv2.CAP_PROP_FPS)):
        break

    if roi_set_flag:
        success, box = tracker.update(img)
        #예외처리 미구현
        if not success:
            print('-------------------------------------------')
            break

        left, top, w, h = [int(v) for v in box]
        center_x = left+w/2
        center_y = top+h/2

        result_top = int(center_y - output_size[1]/2)
        result_bottom = int(center_y + output_size[1]/2)
        result_left = int(center_x - output_size[0]/2)
        result_right = int(center_x + output_size[0]/2)

        while result_top < 0:
            print('top over')
            result_top = result_top + 1
            result_bottom = result_bottom + 1
        while result_bottom > cap.get(cv2.CAP_PROP_FRAME_HEIGHT):
            print('bottom over')
            result_bottom = result_bottom - 1
            result_top = result_top - 1
        while result_left < 0:
            print('left over')
            result_left = result_left + 1
            result_right = result_right + 1
        while result_right > cap.get(cv2.CAP_PROP_FRAME_WIDTH):
            print('right over')
            result_right = result_right - 1
            result_left = result_left - 1

        result_img = img[result_top:result_bottom, result_left:result_right]

        out.write(result_img)
        #for test
        if check_mode:
            cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 255, 255), thickness=3)
            cv2.imshow('result_img', result_img)

    if ready_flag and check_mode:
        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            break


#500 600 20 30

