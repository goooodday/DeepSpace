#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

# 이미지 데이터셋 저장소
# Test data 경로
#DATA_PATH = r'D:\TestImage'
#FILE_NAME = "test.txt"
#CLASS_LIST = False

# Train data 경로
DATA_PATH = r'D:\TrainImage'
FILE_NAME = "train.txt"
CLASS_LIST = True

def filelist(dir_path, filename):

    # 해당 데이터 디렉토리가 존재하는지 확인
    if not os.path.exists(dir_path):
        print ("Not found Dir....")
        return

    # 데이터 디렉토리내의 하위 폴더 리스트 조회
    sub_dirs = os.listdir(dir_path)

    # 전체 클래스의 개수, 디렉토리 개수를 사용
    tot_classes = len(sub_dirs)

    # 클래스 아이디 구성 및 전체 파일 개수 확인
    classlist, tot_count = ClassListMap(sub_dirs)

    # 이미지 파일 목록을 작성하여 파일에 저장
    eachFileList(sub_dirs, classlist, filename)

    # 결함 리스트 정보를 JSON으로 저장
    if CLASS_LIST:
        writeJSON("classList.json", classlist)

    # 처리 결과 표시
    print "* Total Class : %d, Total Images : %d" % (tot_classes, tot_count)
    print "[Class Lists]"

    for classitem in classlist:
        print " - %s(%d) \t\t: %d " % (classitem["name"], classitem["idx"], classitem["count"])

def ClassListMap(dir_path):
    classlist = []
    idx = 0
    tot_file = 0
    for subdir in dir_path:

        # 하위 디렉토리 파일 개수 확인
        sub_path = os.path.join(DATA_PATH, subdir)
        files = os.listdir(sub_path)
        file_count = len(files)
        tot_file += file_count

        # 클래스별 정보 저장 딕셔너리 구성
        tmp_class = {}
        tmp_class["name"] = subdir
        tmp_class["idx"] = idx
        tmp_class["count"] = file_count
        classlist.append(tmp_class)

        idx += 1

    return classlist, tot_file

def eachFileList(dir_path, classlist, filename):

    f = open(filename, 'w')

    # 하위 폴더 리스트(결함ID)에서 결함 이미지 참조
    for subdir in dir_path:
        # 하위 디렉토리 파일 개수 확인
        sub_path = os.path.join(DATA_PATH, subdir)
        files = os.listdir(sub_path)

        # 딕셔너리 배열에서 해당 이름이 같은 클래스의 인덱스를 검색
        class_dic = (item for item in classlist if item["name"] == subdir).next()
        class_idx = class_dic["idx"]

        # 하위 디렉토리의 이미지 파일 리스트 생성
        for file in files:
            # 파일 리스트 작성
            # 하위 디렉토리, 파일명을 경로로 작성, 클래스 인덱스를 추가.
            file_path = os.path.join(subdir, file)
            str_list = "%s %d\n" % (file_path, class_idx)

            # 리스트 내용 파일 쓰기
            f.write(str_list)
            #print file_path, class_idx

    f.close()


def readJSON(filename) :
    f = open(filename, 'r')
    js = json.loads(f.read())
    f.close()
    return js

def writeJSON(filename, dic) :
    f = open(filename, 'w')
    f.write (json.dumps(dic))
    f.close()


if __name__ == "__main__":

    filelist(DATA_PATH, FILE_NAME)
