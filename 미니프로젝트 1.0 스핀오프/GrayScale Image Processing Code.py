## 미션 [GrayScale Image Processing] (Preview 1) 완성 /// 파이썬용으로

import math
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.simpledialog import *
import os.path
### 함수부
#*****************
# 공통 함수부
#*****************
def malloc2D(h, w, initValue = 0) :
    memory = [ [initValue for _ in range(w)] for _ in range(h)]
    return memory
def openImage(): # lodeImage
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    fullname = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')) )
    # 중요! 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname) # 파일 크기(Byte)
    inH = inW = int(math.sqrt(fsize))
    # 메모리 할당
    inImage = malloc2D(inH, inW)
    # 파일 --> 메모리
    rfp = open(fullname, 'rb')
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = ord(rfp.read(1))
    rfp.close()
    equalImage()

def saveImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    if (outImage == None or len(outImage) == 0) : # 영상처리를 한 적이 없다면..
        return
    wfp = asksaveasfile(parent=window, mode='wb', defaultextension='*.raw',
                        filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*'))  )
    import struct
    for i in range(outH) :
        for k in range(outW) :
            wfp.write( struct.pack('B', outImage[i][k]) )
    wfp.close()
    messagebox.showinfo('성공', wfp.name + ' 저장완료 !')

def End() : ## 종료메세지
    global window
    messagebox.showinfo('안내문', ' 프로그램을 종료하시겠습니까?')
    window.destroy() ## 창 닫기

def displayImage(): # printImage
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    ## 기존에 이미지를 오픈한 적이 있으면, 캔버스 뜯어내기
    if (canvas != None):
        canvas.destroy()
    # 벽, 캔버스, 종이 결정
    window.geometry(str(outH)+'x'+str(outW)) # "512x512"
    canvas = Canvas(window, height=outH, width=outW, bg='yellow')  # 칠판
    paper = PhotoImage(height=outH, width=outW)  # 종이
    canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')
    ## 메모리 ---> 화면
    # for i in range(outH):
    #     for k in range(outW):
    #         r = g = b = outImage[i][k]
    #         paper.put('#%02x%02x%02x' % (r, g, b), (k, i))
    # 더블 버퍼링... 비슷한 기법 (모두 다 메모리 창에 출력 형태로 생성한 후에, 한번에 출력) ## 문자열로 만듬
    rgbString = "" # 전체에 대한 16진수 문자열
    for i in range(outH):
        oneString = "" # 한 줄에 대한 16진수 문자열
        for k in range(outH):
            r = g = b = outImage[i][k]
            oneString += '#%02x%02x%02x ' % (r, g, b)
        rgbString += '{' + oneString + '} '
    paper.put(rgbString)
    canvas.pack()


#*****************
# 영상처리 함수부
#*****************
###################################화소점처리   // 11개
def equalImage(): # 동일 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    ########################################
    displayImage()
def addImage(): # 밝은/어두운 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    value = askinteger('정수입력','-255~255 입력',maxvalue=255, minvalue=-255)
    for i in range(inH):
        for k in range(inW):
            px = inImage[i][k] + value
            if (px > 255):
                px = 225
            if (px < 0):
                px = 0
            outImage[i][k] = px
    ########################################
    displayImage()
def mulImage(): # 곱셈 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    value = askinteger('정수입력','1~255',maxvalue=255, minvalue=1)
    for i in range(inH):
        for k in range(inW):
            px = inImage[i][k] * value
            if (px > 255):
                outImage[i][k] = 225
            elif (px < 0):
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    ########################################
    displayImage()
def divImage(): # 나눗셈 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    value = askinteger('정수입력','1~255',maxvalue=255, minvalue=1)
    for i in range(inH):
        for k in range(inW):
            px = (int)(inImage[i][k] // value)
            if (px > 255):
                outImage[i][k] = 225
            elif (px < 0):
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    ########################################
    displayImage()
def ANDImage() : ## AND 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    value = askinteger('정수입력', '0~255', maxvalue=255, minvalue=0)
    for i in range(inH) : # for (int i=0; i<inH; i++)
        for k in range(inW) : # for (int k=0; i<inW; k++)
            px = inImage[i][k] & value
            if(px >= 255) :
                outImage[i][k] = 255
            elif (px < 0):
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    ########################################
    displayImage()
def ORImage() : ## OR 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    value = askinteger('정수입력', '0~255', maxvalue=255, minvalue=0)
    for i in range(inH):  # for (int i=0; i<inH; i++)
        for k in range(inW):  # for (int k=0; i<inW; k++)
            px = inImage[i][k] | value
            if (px >= 255):
                outImage[i][k] = 255
            elif (px < 0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = px
    ########################################
    displayImage()
def XORImage() : ## XOR 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    value = askinteger('정수입력', '0~255', maxvalue=255, minvalue=0)
    for i in range(inH):  # for (int i=0; i<inH; i++)
        for k in range(inW):  # for (int k=0; i<inW; k++)
            px = inImage[i][k] ^ value
            if (px >= 255):
                outImage[i][k] = 255
            elif (px < 0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = px
    ########################################
    displayImage()
def bwImage() : ## 흑백 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH) : # for (int i=0; i<inH; i++)
        for k in range(inW) :  # for (int k=0; i<inW; k++)
            if(inImage[i][k] > 128) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0
        ########################################
    displayImage()
def bwAvgImage() : ## 흑백(평균값) 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    sum, avg = [0] * 2
    for i in range(inH) :
        for k in range(inW) :
            sum += inImage[i][k]
    avg = sum / (inH * inW)

    for i in range(inH) : # for (int i=0; i<inH; i++)
        for k in range(inW) :  # for (int k=0; i<inW; k++)
            if(inImage[i][k] > avg) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0
        ########################################
    displayImage()
def revImage() : ## 반전 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH) : # for (int i=0; i<inH; i++)
        for k in range(inW) :  # for (int k=0; i<inW; k++)
            outImage[i][k] = 255 - inImage[i][k]
        ########################################
    displayImage()
def gammaImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    gamma = askfloat('감마값 입력', '0.0~10.0', maxvalue=10.0, minvalue=0.0)
    value = 1.0 / gamma
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (int)((inImage[i][k] / 255.0) ** (value) * 255.0)
    ########################################
    displayImage()

##################################히스토그램 (선명) 처리     //3개
def histoStretch() : ## 히스토그램 스트레칭 알고리즘 ## flower256
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    high = inImage[0][0]
    low = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] > high):
                high = inImage[i][k]
            if (inImage[i][k] < low):
                low = inImage[i][k]
    for i in range(inH):
        for k in range(inW):
            old = inImage[i][k]
            new = (int)((old - low) / (high - low) * 255.0)
            if (new > 255):
                new = 225
            if (new < 0):
                new = 0
            outImage[i][k] = new
    ########################################
    displayImage()
def endIn() : ## 앤드-인 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    high = inImage[0][0]
    low = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] > high):
                high = inImage[i][k]
            if (inImage[i][k] < low):
                low = inImage[i][k]
    high -= 50
    low += 50
    for i in range(inH):
        for k in range(inW):
            old = inImage[i][k]
            new = (int)((old - low) / (high - low) * 255.0)
            if (new > 255):
                new = 225
            if (new < 0):
                new = 0
            outImage[i][k] = new
    ########################################
    displayImage()
def histoEquaㅣ() : ## 히스토그램 평활화 (명암 대비 최대화) 알고리즘 ## 256 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ## 진짜 영상 처리 알고리즘
    # 1단계 : 빈도수 세기 (=히스토그램) histo[255]
    histo = []
    for i in range(256):
        histo.append(0)
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1
    # 2단계 : 누적 히스토그램 생성
    sumHisto = []
    for i in range(256):
        sumHisto.append(0)
    sumHisto[0] = histo[0]
    for i in range(256):
        sumHisto[i] = sumHisto[i - 1] + histo[i]
    #  3단계 : 정규화된 히스토그램 생성
    normalHisto = []
    for i in range(256):
        normalHisto.append(0)
    for i in range(256):
        normalHisto[i] = sumHisto[i] * (1.0 / (inH * inW)) * 255.0
    # 4단계 : 히스토그램 출력
    for i in range(256):
        for k in range(inW):
            outImage[i][k] = (int)(normalHisto[inImage[i][k]])
    ########################################
    displayImage()

##################################기하학처리      //9개
def zoomOut() : ## 축소 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    value = askinteger('정수입력', '2배,4배,8배...축소 입력', maxvalue=255, minvalue=0)
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = (int)(inH / value)
    outW = (int)(inW / value)
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[(int)(i / value)][(int)(k / value)] = inImage[i][k]
    ########################################
    displayImage()
def zoomIn_for() : ## 확대(포워딩) 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    value = askinteger('정수입력', '2배,4배,8배...확대 입력', maxvalue=255, minvalue=0)
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = (int)(inH * value)
    outW = (int)(inW * value)
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[(int)(i * value)][(int)(k * value)] = inImage[i][k]
    ########################################
    displayImage()
def zoomIn_back() : ## 확대(백워딩) 알고리즘 ## 홀문제 해결
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    value = askinteger('정수입력', '2배,4배,8배...확대 입력', maxvalue=255, minvalue=0)
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = (int)(inH * value)
    outW = (int)(inW * value)
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[(int)(i / value)][(int)(k / value)]
    ########################################
    displayImage()
def rotate() : ## 회전 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    degree = askinteger('정수입력', '각도(-360~360) 입력', maxvalue=360, minvalue=-360)
    radian = degree * 3.141592 / 180.0
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(outH):
        for k in range(outW):
            xs, ys = i, k
            xd = (int)(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = (int)(math.sin(radian) * xs + math.cos(radian) * ys)

            if ((0 <= xd < outH) and (0 <= yd < outW)) :
                outImage[xd][yd] = inImage[xs][ys]
    ########################################
    displayImage()
def rotate2() : ## 회전(백워딩 + 중앙) 알고리즘  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    degree = askinteger('정수입력', '각도(-360~360) 입력', maxvalue=360, minvalue=-360)
    radian = degree * 3.141592 / 180.0
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    cx = inH // 2
    cy = inW // 2
    for i in range(outH):
        for k in range(outW):
            xd = i
            yd = k
            xs = (int)(math.cos(radian) * (xd - cx) + math.sin(radian) * (yd - cy))
            ys = (int)(-math.sin(radian) * (xd - cx) + math.cos(radian) * (yd - cy))
            xs += cx
            ys += cy

            if ((0 <= xs < outH) and (0 <= ys < outW)):
                outImage[xd][yd] = inImage[xs][ys]
    ########################################
    displayImage()
def Translation() : ## 이동 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    H_pos = askinteger('정수입력', '세로 이동값 입력', minvalue=0)
    W_pos = askinteger('정수입력', '가로 이동값 입력', minvalue=0)
    for i in range(outH - H_pos):
        for k in range(outW - W_pos):
            outImage[i + H_pos][k + W_pos] = inImage[i][k]
    ########################################
    displayImage()
def Mirroring_UAD() : ## 상하대칭 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[inH - 1 - i][k]
    ########################################
    displayImage()
def Mirroring_LAR() : ## 좌우대칭 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][inW - 1 - k]
    ########################################
    displayImage()
def Mirroring() : ## 상하좌우대칭
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[inH - 1 - i][inW - 1 - k]
    ########################################
    displayImage()

##################################화소영역처리    //7개
def embos() :  ## 엠보싱 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 후처리 (마스크 값의 합계에 따라서...) +128
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127.0
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def blur() : ## 블러링 알고리즘  # 후처리 필요없음
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당 # 메모리 해제 필요없음
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    blur_mask = 1.0 / 9
    mask = [ [blur_mask, blur_mask, blur_mask],
             [blur_mask, blur_mask, blur_mask],
             [blur_mask, blur_mask, blur_mask]  ]
    # mask = [[1.0 / 9, 1.0 / 9, 1.0 / 9],
    #         [1.0 / 9, 1.0 / 9, 1.0 / 9],
    #         [1.0 / 9, 1.0 / 9, 1.0 / 9]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def blur_9x9() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당 # 메모리 해제 필요없음
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    blur_mask = 1.0 / 81
    mask = [[blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask],
            [blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask, blur_mask] ]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 8, inW + 8)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 8):
        for k in range(inW + 8):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(9):
                for n in range(9):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def gaussianFilter() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당 # 메모리 해제 필요없음
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[1.0 / 16, 1.0 / 8, 1.0 / 16],
            [1.0 / 8, 1.0 / 4, 1.0 / 8],
            [1.0 / 16, 1.0 / 8, 1.0 / 16]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def sharpening1() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당 # 메모리 해제 필요없음
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, -1.0, 0.0],
            [-1.0, 5.0, -1.0],
            [0.0, -1.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def sharpening2() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당 # 메모리 해제 필요없음
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, -1.0, -1.0],
            [-1.0, 9.0, -1.0],
            [-1.0, -1.0, -1.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def sharpening_HPF() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당 # 메모리 해제 필요없음
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0 / 9, -1.0 / 9, -1.0 / 9],
            [-1.0 / 9, 8.0 / 9, -1.0 / 9],
            [-1.0 / 9, -1.0 / 9, -1.0 / 9]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()

##################################경계선 검출    //17개
def raw() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def columm() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, 0.0, 0.0],
            [-1.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def RawColumm() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, -1.0, 0.0],
            [-1.0, 2.0, 0.0],
             [0.0, 0.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Roberts_raw() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Roberts_colum() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, 0.0, -1.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Roberts_RawColumm() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, 0.0, -1.0],
              [0.0, 2.0, 0.0],
              [0.0, 0.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Prewitt_raw() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, -1.0, -1.0],
              [0.0, 0.0, 0.0],
              [1.0, 1.0, 1.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Prewitt_colum() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[1.0, 0.0, -1.0],
            [1.0, 0.0, -1.0],
            [1.0, 0.0, -1.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Prewitt_RawColumm() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, -1.0, -2.0],
             [1.0, 0.0, -1.0],
             [2.0, 1.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Sobel_raw() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, -2.0, -1.0],
               [0.0, 0.0, 0.0],
               [1.0, 2.0, 1.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Sobel_colum() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[1.0, 0.0, -1.0],
            [2.0, 0.0, -2.0],
            [1.0, 0.0, -1.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Sobel_RawColumm() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, -2.0, -2.0],
             [2.0, 0.0, -2.0],
             [2.0, 2.0, 0.0]]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Laplacian1() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[0.0, -1.0, 0.0],
            [-1.0, 4.0, -1.0],
             [0.0, -1.0, 0.0] ]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Laplacian2() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [ [1.0, 1.0, 1.0],
            [1.0, -8.0, 1.0],
             [1.0, 1.0, 1.0] ]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def Laplacian3() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [[-1.0, -1.0, -1.0],
            [-1.0, 8.0, -1.0],
             [-1.0, -1.0, -1.0] ]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def LoG() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [    [0.0, 0.0, -1.0, 0.0, 0.0],
              [0.0, -1.0, -2.0, -1.0, 0.0],
            [-1.0, -2.0, 16.0, -2.0, -2.0],
              [0.0, -1.0, -2.0, -1.0, 0.0],
                [0.0, 0.0, -1.0, 0.0, 0.0] ]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 4, inW + 4)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 4):
        for k in range(inW + 4):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(5):
                for n in range(5):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()
def DoG_7x7() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 ---> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상 처리 알고리즘
    ########## 화소 영역 처리 ###############
    mask = [ [0.0, 0.0, -1.0 , -1.0 , -1.0, 0.0, 0.0],
		    [0.0 , -2.0, -3.0, -3.0, -3.0, -2.0, 0.0],
			  [-1.0, -3.0, 5.0, 5.0, 5.0, -3.0, -1.0],
			 [-1.0, -3.0, 5.0, 16.0, 5.0, -3.0, -1.0],
			  [-1.0, -3.0, 5.0, 5.0, 5.0, -3.0, -1.0],
			 [0.0, -2.0, -3.0, -3.0, -3.0, -2.0, 0.0],
			   [0.0, 0.0, -1.0, -1.0, -1.0, 0.0, 0.0] ]
    ## 임시 메모리 할당 (실수형) tmpInImage
    tmpInImage = malloc2D(inH + 6, inW + 6)
    tmpOutImage = malloc2D(outH, outW)
    ## 임시 입력 메모리를 초기화 (127): 필요시 평균값
    for i in range(inH + 6):
        for k in range(inW + 6):
            tmpInImage[i][k] = 127
    ## 입력 이미지 ----> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    ## *** 임시 입력 이미지와 임시 출력 이미지로 회선 연산 ***
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for m in range(7):
                for n in range(7):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S
    ## 임시 출력 영상 ---> 출력 영상.
    for i in range(outH):
        for k in range(outW):
            if (tmpOutImage[i][k] > 256.0):
                outImage[i][k] = 255
            elif (tmpOutImage[i][k] < 0.0):
                outImage[i][k] = 0
            else:
                outImage[i][k] = (int)(tmpOutImage[i][k])
    ########################################
    displayImage()




### 전역 변수부
window, canvas, paper = None, None, None
inImage, outImage = [], []
inH, inW, outH, outW = [0]*4
fullname = ''


### 메인 코드부
window = Tk() # 벽
window.geometry("500x500")
window.resizable(width=False, height=False)
window.title("[GrayScale Image Processing] (Preview 1)")

# 메뉴 만들기
mainMenu = Menu(window) # 메뉴의 틀
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu, tearoff = 0)  # 상위 메뉴 (파일)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label='저장', command=saveImage)
fileMenu.add_separator()
fileMenu.add_command(label='종료',command=End)

pixeMenu = Menu(mainMenu, tearoff = 0)  # 상위 메뉴 (화소점처리)
# histoMenu = Menu(pixeMenu, tearoff = 0)  # 화소점 처리 메뉴 (히스토그램)
mainMenu.add_cascade(label='화소점처리', menu=pixeMenu)
pixeMenu.add_command(label='동일 이미지', command=equalImage)
pixeMenu.add_command(label='밝게/어둡게', command=addImage)
pixeMenu.add_command(label='더 밝게', command=mulImage)
pixeMenu.add_command(label='더 어둡게', command=divImage)
pixeMenu.add_command(label='AND', command=ANDImage)
pixeMenu.add_command(label='OR', command=ORImage)
pixeMenu.add_command(label='XOR', command=XORImage)
pixeMenu.add_command(label='이진화', command=bwImage)
pixeMenu.add_command(label='이진화(평균값)', command=bwAvgImage)
pixeMenu.add_command(label='반전', command=revImage)
pixeMenu.add_command(label='감마', command=gammaImage)
pixeMenu.add_separator()            # (히스토그램 처리)
pixeMenu.add_command(label='히스토그램 스트레칭', command=histoStretch)
pixeMenu.add_command(label='앤드-인', command=endIn)
pixeMenu.add_command(label='히스토그램 평활화', command=histoEquaㅣ)

geoMenu = Menu(mainMenu, tearoff = 0)  # 상위 메뉴 (기하학처리)
mainMenu.add_cascade(label='기하학처리', menu=geoMenu)
geoMenu.add_command(label='축소', command=zoomOut)
geoMenu.add_command(label='확대(포워딩)', command=zoomIn_for)
geoMenu.add_command(label='확대(백워딩)', command=zoomIn_back)
geoMenu.add_command(label='회전', command=rotate)
geoMenu.add_command(label='회전(백워딩+중앙)', command=rotate2)
geoMenu.add_command(label='이동', command=Translation)
geoMenu.add_command(label='상하대칭', command=Mirroring_UAD)
geoMenu.add_command(label='좌우대칭', command=Mirroring_LAR)
geoMenu.add_command(label='상하좌우대칭', command=Mirroring)

areaMenu = Menu(mainMenu, tearoff = 0)  # 상위 메뉴 (화소영역처리)
mainMenu.add_cascade(label='화소영역처리', menu=areaMenu)
areaMenu.add_command(label='엠보싱', command=embos)
areaMenu.add_command(label='블러링', command=blur)
areaMenu.add_command(label='블러링(9x9)', command=blur_9x9)
areaMenu.add_command(label='가우시안 스무딩', command=gaussianFilter)
areaMenu.add_command(label='샤프닝.1', command=sharpening1)
areaMenu.add_command(label='샤프닝.2', command=sharpening2)
areaMenu.add_command(label='고주파 샤프닝', command=sharpening_HPF)
areaMenu.add_separator()            # (경계선 검출 처리)
areaMenu.add_command(label='수평에지', command=raw)
areaMenu.add_command(label='수직에지', command=columm)
areaMenu.add_command(label='수평+수직', command=RawColumm)
areaMenu.add_command(label='로버츠_행', command=Roberts_raw)
areaMenu.add_command(label='로버츠_열', command=Roberts_colum)
areaMenu.add_command(label='로버츠_행열', command=Roberts_RawColumm)
areaMenu.add_command(label='프리윗_행', command=Prewitt_raw)
areaMenu.add_command(label='프리윗_열', command=Prewitt_colum)
areaMenu.add_command(label='프리윗_행열', command=Prewitt_RawColumm)
areaMenu.add_command(label='소벨_행', command=Sobel_raw)
areaMenu.add_command(label='소벨_열', command=Sobel_colum)
areaMenu.add_command(label='소벨_행열', command=Sobel_RawColumm)
areaMenu.add_command(label='라플라시안.1', command=Laplacian1)
areaMenu.add_command(label='라플라시안.2', command=Laplacian2)
areaMenu.add_command(label='라플라시안.3', command=Laplacian3)
areaMenu.add_command(label='LoG', command=LoG)
areaMenu.add_command(label='DoG(7x7)', command=DoG_7x7)





window.mainloop()