from animbtn import *
# НЕДОДЕЛАН


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout  = QVBoxLayout()
        self.setWindowTitle('Bruh')
        self.layout.addWidget(mishBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800,400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        #


class mishBar(QWidget):

    def __init__(self, parent):
        super(mishBar, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel('    Test')
        # self.title.setMargin(0)
        # self.title.setScaledContents(True)

        btn_size = 35

        self.btn_close = mishSVG('icons/close.svg')
        self.btn_closeL = QVBoxLayout()
        self.btn_closeL.setContentsMargins(0, 0, 0, 0)
        self.btn_closeG = animatedCard(basecolor='#BEBEBE', oncolor='#AFAFAF', clickcolor='#A5A5A5', shadowRadius=0, ontime=150)
        self.btn_closeG.setLayout(self.btn_closeL)
        self.btn_closeL.addWidget(self.btn_close)
        self.btn_closeL.setAlignment(Qt.AlignCenter)
        self.btn_close.setFixedSize(20, 20)
        self.btn_closeG.setFixedSize(50, 35)
        self.btn_closeG.setBruh()

        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_closeG.clicked.connect(self.btn_close.clicked)
        self.btn_close.setStyleSheet("background-color: transparent;")

        self.btn_min = mishSVG('icons/minus.svg')
        self.btn_minL = QVBoxLayout()
        self.btn_minL.setContentsMargins(0, 0, 0, 0)
        self.btn_minG = animatedCard(basecolor='#BEBEBE', oncolor='#AFAFAF', clickcolor='#A5A5A5', shadowRadius=0, ontime=150)
        self.btn_minG.setLayout(self.btn_minL)
        self.btn_minL.addWidget(self.btn_min)
        self.btn_minL.setAlignment(Qt.AlignCenter)
        self.btn_min.setFixedSize(20, 20)
        self.btn_minG.setFixedSize(50, 35)
        self.btn_minG.setBruh()

        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_minG.clicked.connect(self.btn_min.clicked)
        self.btn_min.setStyleSheet("background-color: transparent;")

        self.btn_max = mishSVG('icons/full.svg')
        self.btn_maxL = QVBoxLayout()
        self.btn_maxL.setContentsMargins(0, 0, 0, 0)
        self.btn_maxG = animatedCard(basecolor='#BEBEBE', oncolor='#AFAFAF', clickcolor='#A5A5A5', shadowRadius=0, ontime=150)
        self.btn_maxG.setLayout(self.btn_maxL)
        self.btn_maxL.addWidget(self.btn_max)
        self.btn_maxL.setAlignment(Qt.AlignCenter)
        self.btn_max.setFixedSize(20, 20)
        self.btn_maxG.setFixedSize(50, 35)
        self.btn_maxG.setBruh()

        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_maxG.clicked.connect(self.btn_max.clicked)
        #self.btn_max.clicked.connect(self.btn_maxG.clicked)
        self.btn_max.setStyleSheet("background-color: transparent;")

        #self.title.setFixedHeight(35)
        self.title.setFixedWidth(100)
        self.title.setFixedHeight(35)

        self.btnGL = QHBoxLayout()
        self.btnG = QGroupBox()
        self.btnG.setLayout(self.btnGL)
        self.btnG.setStyleSheet('background-color: #BEBEBE;padding:0px;padding-top: 0px;line-height: 1px; padding-top: 0px')
        self.btnGL.setContentsMargins(0, 0, 0, 0)
        self.btnG.setFixedSize(150, 35)
        self.btnGL.addWidget(self.btn_minG)
        self.btnGL.addWidget(self.btn_maxG)
        self.btnGL.addWidget(self.btn_closeG)

        self.title.setAlignment(Qt.AlignVCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btnG)
        # self.layout.addWidget(self.btn_minG)
        # self.layout.addWidget(self.btn_maxG)
        # self.layout.addWidget(self.btn_closeG)
        self.layout.setContentsMargins(0, 0, 1, 0)

        self.title.setStyleSheet("""
            background-color: #BEBEBE;
            color: #555555;
            font-size: 14px;
            border-radius:1px;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False
        #self.title.setText(self.windowTitle())
        #self.parent.setAttribute(Qt.WA_TranslucentBackground, True) -- вдруг понадобится
    
    def setTitle(self, title):
        self.title.setText(f'    {title}')

    def resizeEvent(self, QResizeEvent):
        super(mishBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()
        #print(self.btn_maxG.size())

    def btn_min_clicked(self):
        self.parent.showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    print(mw.windowTitle())
    apply_stylesheet(app, theme='light_blue.xml')
    mw.show()
    sys.exit(app.exec_())