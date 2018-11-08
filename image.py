#!/usr/bin/env python
# coding=utf-8

# from os.path import dirname
import os,sys, getopt
from urllib2 import Request, urlopen
from base64 import b64encode
from multiprocessing import Pool
from PIL import Image
import tinify

# 最大线程数
poolLimite = 10
key = "***************"
opts, args = getopt.getopt(sys.argv[1:], "hi:o:r:")
input_doc_path=""
output_doc_path = ''
filePaths=[]

for op, value in opts:
    if op == "-i":
        input_doc_path = value
    elif op == "-o":
        output_doc_path = value
    elif op == "-r":
        input_doc_path = value
        output_doc_path = value
    elif op == "-h":
        print('''
        使用方法 python tinypng.py -i 图片资源路径 -o 输出路径
        -o 参数可以为空，默认存在输入路径/tinypng 内 -r 输出路径就是输入路径,会替换掉原资源
        去 https://tinypng.com/developers 申请自己的key 每key每月免费压缩500个图
        默认并发数为10 可以自己调整''')


def absFilePath(fileName):
    return os.path.join(input_doc_path,fileName)


def getImageData(filePath):
    im = Image.open(filePath)

    data = im.getdata()
    # 计算兆
    length = len(data) / 1024.0 / 1024.0

    # 压缩大于0.5兆的图片
    if length > 0.5:    
        # getTinyPng(filePath)
        print filePath
        print('宽：%d,高：%d' % (im.size[0], im.size[1]))
        print  length

def getTinyPng(filePath):
    print('开始'+filePath)

    output = os.path.join(output_doc_path, os.path.relpath(filePath,input_doc_path))
    tinify.key = key
    tinify.from_file(filePath).to_file(output)


def main():
    global output_doc_path
    if output_doc_path == '':
        output_doc_path = os.path.join(os.path.split(input_doc_path)[0], 'outputTinypng')

    if not os.path.exists(output_doc_path):
        os.mkdir(output_doc_path)

    for parent,dirnames,filenames in os.walk(input_doc_path):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
      for dirname in  dirnames:                       #输出文件夹信息
        # print("parent is:" + parent)
        # print("dirname is" + dirname)
        outDir = os.path.join(output_doc_path,os.path.relpath(os.path.join(parent,dirname),input_doc_path))
        if not os.path.exists(outDir):
            os.mkdir(outDir)

      for filename in filenames:                        #输出文件信息
        # print("parent is:" + parent)
        # print("filename is:" + filename)
        filePaths.append(os.path.join(parent,filename))

    pngFilePaths = filter(lambda x:os.path.splitext(x)[1]=='.png' or os.path.splitext(x)[1]=='.jpg',filePaths)
    print('父进程id = %s.' % os.getpid())
    p = Pool(poolLimite)
    for fileName in pngFilePaths:
        p.apply_async(getImageData, args=(fileName,))
    print('等待所有子进程完成')
    p.close()
    p.join()
    print('所有子进程完成。')

if __name__=='__main__':
    if os.path.isdir(input_doc_path):
        main()
