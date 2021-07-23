import cv2
import numpy as np
import math
from pylab import plt
from matplotlib.pyplot import MultipleLocator
#解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False



def findCoor(img_path,save_path):
  img = cv2.imread(img_path)
  #获取图片的宽和高
  width,height = img.shape[:2][::-1]
  #将图片缩小便于显示观看
  img_resize = cv2.resize(img,
  (int(width*2),int(height*2)),interpolation=cv2.INTER_CUBIC)
  #显示读取的图片  
  # cv2.imshow("img",img_resize)
  # print("img_reisze shape:{}".format(np.shape(img_resize)))
  #将图片转为灰度图
  img_gray = cv2.cvtColor(img_resize,cv2.COLOR_RGB2GRAY)
  print()
  # img_gray = img_gray[int(img_gray.shape[0]/4):int(img_gray.shape[0]*3/4)][int(img_gray.shape[1]/4):int(img_gray.shape[1]*3/4)]
  add=500
  img_gray1=img_gray
  img_gray = img_gray[:][add:1300]

  # img_gray=img_gray1[:][512:150]
  #显示灰度图
  # cv2.imshow("img_gray",img_gray)
  #保存灰度图
  # cv2.imwrite("./save/test_img_gray.jpg",img_gray)
  # print("img_gray shape:{}".format(np.shape(img_gray)))


  #创建数组来存储圆心和边的坐标
  coorArray=[]
  # 记录读取的点
  k=0
  def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
      if event == cv2.EVENT_LBUTTONDOWN:
          xy = "%d,%d" % (x, y)
          #显示字符串
          xy=str(x)+","+str(y+add)          
          coorArray.append([x,y+add])        
          cv2.circle(img_gray, (x, y), 1, (255, 0, 0), thickness = -1)
          cv2.putText(img_gray, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                      1.0, (0,0,0), thickness = 1)
          cv2.imshow("image", img_gray)
  cv2.namedWindow("image")
  cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
  #设定生成窗口个数
  n=1
  while(n>0):
      cv2.imshow("image", img_gray)
      if cv2.waitKey(0)&0xFF==27:
          break
      n=n-1
  ##求半径 
  r=math.pow(coorArray[0][0]-coorArray[1][0],2)+math.pow(coorArray[0][1]-coorArray[1][1],2)
  r=int(math.pow(r,0.5))
  Abscissa_Arr=[]
  for i in range(r):
    Abscissa_Arr.append(i)
  pixels_arr=avg_(coorArray[0][0],coorArray[0][1],r,10,img_gray1)
  #画半径-像素值的折线图
  plot_(Abscissa_Arr,pixels_arr,r,save_path)

  
def plot_(x_axis_data,y_axis_data,r,save_path):
  # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
  plt.plot(x_axis_data, y_axis_data, 'ro-', color='#4169E1', alpha=0.8, linewidth=1, label='灰度像素值') 
  # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
  plt.legend(loc="upper right")
  plt.xlabel('x轴-半径')
  plt.ylabel('y轴-圆周上灰度平均值')
  x_major_locator=MultipleLocator(5)
  #把x轴的刻度间隔设置为1，并存在变量里
  ax=plt.gca()
  #ax为两条坐标轴的实例
  ax.xaxis.set_major_locator(x_major_locator)
  #把x轴的主刻度设置为1的倍数
  plt.xlim(-0.5,r)
  #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
  plt.savefig(save_path)
  plt.show()
  
def avg_(x,y,r,pixels_num,img):
  pixels_Arr=[]
  #距离圆心 1，2，3，，，，r
  for i in range(r):
    one_pixels_sum=0
    #根据取的点数来确定 圆周上像素点的坐标
    for j in range(pixels_num):      
      x1,y1=x+int(math.cos(j*math.pi/pixels_num)*i),y+int(math.sin(j*math.pi/pixels_num)*i)
      one_pixels_sum+=img[x1][y1]
    pixels_Arr.append(one_pixels_sum/pixels_num)  
  return pixels_Arr   
# cv2.destroyAllWindows()
if __name__ == "__main__":
  #照片的数量
  nums=3
  for i in range(nums):
    i=i+1
    img_path = "./data/"+str(i)+".jpg"
    save_path="./save/gray_cur"+str(i)+".png"
    findCoor(img_path,save_path)
    
