from yolov5.yolov5 import detect
import argparse
import os
import sys

# 판별하고자 하는 이미지 파일의 위치
# adaptor.py 파일을 기준으로 상대경로 OR 절대경로
# C:/Users/michi/HAE/yolov5/yolov5/
MODEL_PATH = 'C:/Users/michi/HAE/yolov5/yolov5/runs/exp0/weights/best.pt'
IMG_PATH = 'C:/Users/michi/HAE/yolov5/yolov5/inference/media/test'


def get_equipment_category():
    # detect.py에서 사용하던 opt를 그대로 가져와, 필요한 부분만 변경함
    # 포착한 사진속 운동기구들 중 확률이 가장 높은 운동기구의 클래스를 int형으로 반환
    # weights : 모델의 위치
    # source : 이미지 파일 위치
    # output : 판정 결과 파일이 저장될 위치

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=MODEL_PATH, help='model.pt path(s)')
    parser.add_argument('--source', type=str, default=IMG_PATH, help='source')
    parser.add_argument('--output', type=str, default='inference/output', help='output folder')
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    opt = parser.parse_args()

    category = detect.detect(opt)

    return category


if __name__ == "__main__":
    print('RESULT : {}'.format(get_equipment_category()))