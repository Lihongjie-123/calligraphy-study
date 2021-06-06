'''
Created on 2018年8月9日

@author: Freedom
'''

from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPen, QColor, QSize
from PyQt5.QtCore import Qt
from pandas import DataFrame
from datetime import datetime


class PaintBoard(QWidget):
    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData()  # 先初始化数据，再初始化界面
        self.__InitView()
        self.setMouseTracking(True)
        self.painting = False

    def __InitData(self):
        self.H = 920
        self.L = 690
        self.__size = QSize(self.L, self.H)
        self.colorR = 'green'
        self.colorC = 'black'
        # 新建QPixmap作为画板，尺寸为__size
        self.__board = QPixmap(self.__size)
        # self.__board = QPixmap()
        self.__board.fill(Qt.white)  # 用白色填充画板

        self.__IsEmpty = True  # 默认为空画板
        self.EraserMode = False  # 默认为禁用橡皮擦模式

        self.lastPos = QPoint(0, 0)  # 上一次鼠标位置
        self.currentPos = QPoint(0, 0)  # 当前的鼠标位置

        self.__painter = QPainter()  # 新建绘图工具

        self.__thickness = 2  # 默认画笔粗细为2px
        self.__penColor = QColor(self.colorR)  # 设置默认画笔颜色为绿色
        self.__colorList = QColor.colorNames()  # 获取颜色列表
        self.step_calculation = 10  # 计算步长
        self.x = list()
        self.y = list()  # 用于记录鼠标位置，计算斜率与绘制起点的距离
        for i in range(self.step_calculation):
            self.x.append(0)
            self.y.append(0)
        self.is_press = False
        self.path = './' + str(datetime.now().strftime('%Y-%m-%d')) + '.csv'
        self.title = [
            'X coordinate', 'Y coordinate', 'Slope', 'Distance', 'Is_press'
        ]

    def __InitView(self):
        # 设置界面的尺寸为__size
        self.setFixedSize(self.__size)

    def Clear(self):
        # 清空画板
        self.__board.fill(Qt.white)
        self.update()
        self.__IsEmpty = True

    def ChangePenColor(self, color):
        # 改变画笔颜色
        self.__penColor = QColor(color)

    def ChangePenThickness(self, thickness=10):
        # 改变画笔粗细
        self.__thickness = thickness

    def IsEmpty(self):
        # 返回画板是否为空
        return self.__IsEmpty

    def GetContentAsQImage(self):
        # 获取画板内容（返回QImage）
        image = self.__board.toImage()
        return image

    def paintEvent(self, paintEvent):
        # 绘图事件
        # 绘图时必须使用QPainter的实例，此处为__painter
        # 绘图在begin()函数与end()函数间进行
        # begin(param)的参数要指定绘图设备，即把图画在哪里
        # drawPixmap用于绘制QPixmap类型的对象
        self.__painter.begin(self)
        # 0,0为绘图的左上角起点的坐标，__board即要绘制的图
        self.__painter.drawPixmap(0, 0, self.__board)
        self.__painter.end()

    def mouseMoveEvent(self, mouseEvent):
        # 鼠标移动时，更新当前位置，并在上一个位置和当前位置间画线
        self.currentPos = mouseEvent.pos()
        if self.painting:
            self.__painter.begin(self.__board)
            for i in range(1, self.step_calculation - 1):
                self.x[i] = self.x[i + 1]
                self.y[i] = self.y[i + 1]

            self.x[self.step_calculation - 1] = self.currentPos.x()
            self.y[self.step_calculation - 1] = 800 - self.currentPos.y()

            if self.x[self.step_calculation - 1] == self.x[1]:
                xl = 'Infinity'
            else:
                xl = (self.y[self.step_calculation - 1] - self.y[1]) / (
                    self.x[self.step_calculation - 1] - self.x[1])
            tem = pow(
                (self.y[self.step_calculation - 1] - self.y[0]), 2) + pow(
                    (self.x[self.step_calculation - 1] - self.x[0]), 2)
            distance = pow(tem, 0.5)
            # print('当前位置为：(', self.x[self.step_calculation - 1], ',',
            #       self.y[self.step_calculation - 1], ')，当前点的斜率为：', xl,
            #       '，与起点的距离为：', distence)
            df = DataFrame(columns=self.title)
            inside = {
                self.title[0]: self.x[self.step_calculation - 1],
                self.title[1]: self.y[self.step_calculation - 1],
                self.title[2]: xl,
                self.title[3]: distance,
                self.title[4]: str(self.is_press)
            }
            df = df.append(inside, ignore_index=True)
            df.to_csv(self.path, mode='a', index=None, header=None)
            if not (self.EraserMode):
                # 非橡皮擦模式
                self.__painter.setPen(QPen(self.__penColor,
                                           self.__thickness))  # 设置画笔颜色，粗细
            else:
                # 橡皮擦模式下画笔为纯白色，粗细为10
                self.__painter.setPen(QPen(Qt.white, 10))

            # 画线
            self.__painter.drawLine(self.lastPos, self.currentPos)
            self.__painter.end()
        self.lastPos = self.currentPos
        self.update()  # 更新显示

    def mouseReleaseEvent(self, event):
        self.__penColor = QColor(self.colorR)
        self.is_press = False

    def mousePressEvent(self, event):
        self.__penColor = QColor(self.colorC)
        self.is_press = True
