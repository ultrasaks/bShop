import PyQt5
import sys
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import *


class animatedPushButton(QPushButton):
    def __init__(self):
        QPushButton.__init__(self)
        color1 = QColor(255, 0, 0)
        color2 = QColor(255, 144, 0)
        color3 = QColor(255, 255, 0)
        color4 = QColor(224, 192, 192)
        byar = QByteArray()
        byar.append('zcolor')
        self.co_get = 0
        self.co_set = 0
        self.color_anim = QPropertyAnimation(self, byar)
        self.color_anim.setStartValue(color4)
        self.color_anim.setKeyValueAt(0.15, color1)
        self.color_anim.setKeyValueAt(0.3, color2)
        self.color_anim.setKeyValueAt(0.5, color3)
        self.color_anim.setKeyValueAt(0.75, color2)
        self.color_anim.setEndValue(color4)
        self.color_anim.setDuration(2000)
        self.color_anim.setLoopCount(1)

        self.custom_anim = QPropertyAnimation(self, byar)


class mishSVG(QSvgWidget):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


class mishLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


class appinfo(QWidget):
    def __init__(self, name, app_id, descr, author, tags, dowlink):
        super().__init__()
        self.name = name
        self.id = app_id
        self.author = author
        self.tagi = tags
        d = ''
        temp = 0
        for i in range(1, int(len(descr) / 83) + 1):
            temp = i
            d += descr[(i - 1) * 83:(i) * 83] + '\n'
        d += descr[(temp) * 83:]
        self.descr = d
        self.downLink = dowlink
        QTimer.singleShot(0, self.initUI)

    def initUI(self):
        self.setWindowTitle(self.name)
        self.setGeometry(300, 300, 630, 470)
        qt_rectangle = self.frameGeometry()
        center_Point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_Point)
        self.move(qt_rectangle.topLeft())

        self.MainLayout = QVBoxLayout()
        self.MainLayout.setAlignment(Qt.AlignHCenter)
        self.setLayout(self.MainLayout)

        self.appdetLayout = QVBoxLayout()
        self.appicLayout = QHBoxLayout()


        self.testbtn = animatedPushButton()
        self.testbtn.setText('test')
        self.nameL = QLabel(self.name)
        self.nameL.setFont(QFont('Roboto', 18))
        self.descrScroll = QScrollArea()
        self.descrLayout = QHBoxLayout()
        self.description = QLabel(self.descr)
        self.descrScroll.setWidget(self.description)
        self.icon = mishSVG(f'cache/{str(self.id)}/icon.svg')
        self.fromL = QLabel(self.author)
        self.tags = QHBoxLayout()
        self.downloadBtn = QPushButton('Download')

        self.tags.setAlignment(Qt.AlignLeft)
        tagdef = QLabel('Tags:')
        tagdef.setFixedWidth(31)
        self.tags.addWidget(tagdef)
        tegi = self.tagi.split(';')
        for tag in tegi:
            temp_tag = QLabel(rf'<a href=\"\">{tag}</a>')
            temp_tag.setFixedWidth(len(tag) * 7)
            temp_tag.linkActivated.connect(lambda: self.download('test'))
            self.tags.addWidget(temp_tag)

        self.appdetLayout.addWidget(self.nameL)
        self.appdetLayout.addWidget(self.fromL)
        self.appdetLayout.addWidget(self.testbtn)
        self.appdetLayout.addLayout(self.tags)
        self.appdetLayout.addWidget(self.downloadBtn)

        self.appicLayout.addWidget(self.icon)
        self.appicLayout.addLayout(self.appdetLayout)


        self.descrScroll.setStyleSheet('QWidget  {background-color: #f5f5f5; border: 1px solid #f5f5f5; border-radius: 3px;} ')
        self.description.setFixedSize(self.description.width() + 20, self.description.height() + 10)

        self.icon.setFixedSize(128, 128)
        self.icon.setStyleSheet('QWidget  {background-color: #f5f5f5; border: 10px solid #f5f5f5; border-radius: 8px;} ')

        self.downloadBtn.clicked[bool].connect(lambda: self.download(self.downLink))

        # self.MainLayout.addWidget(self.icon)
        # self.MainLayout.addWidget(self.nameL)
        self.MainLayout.addLayout(self.appicLayout)
        self.MainLayout.addWidget(self.descrScroll)

    def download(self, link):
        print('piss')
        self.testbtn.color_anim.start()

    #pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut tincidunt neque id sagittis euismod. Proin laoreet consectetur diam, eget bibendum metus rutrum in. Curabitur mi magna, suscipit et imperdiet hendrerit, semper nec nunc. Integer odio lacus, iaculis eget efficitur nec, hendrerit ac libero. Quisque eget quam pellentesque, blandit velit quis, eleifend odio. Sed in condimentum neque, at mollis nibh. Aliquam ac diam commodo, dapibus orci ac, cursus dui. Suspendisse egestas eros sit amet condimentum blandit. In interdum, tortor nec ornare blandit, ex elit tempor orci, a semper nisl tellus nec velit.
Aliquam vel imperdiet risus. Quisque suscipit efficitur est nec varius. Donec tortor urna, fringilla et maximus et, ultricies in massa. Fusce augue mi, venenatis quis cursus quis, malesuada a augue. Pellentesque vitae fermentum quam, vitae scelerisque quam. Curabitur a turpis sed enim commodo egestas et vitae risus. Phasellus vitae sem tellus. Sed pulvinar, odio vestibulum dictum posuere, orci mauris lacinia dui, sed pellentesque dui ligula sit amet lacus. In nec fringilla risus. Suspendisse ut eleifend metus. Mauris malesuada, orci non ultricies ornare, lacus sapien vehicula nisi, nec iaculis sem elit ut purus. Pellentesque ut ex rhoncus, imperdiet mi quis, hendrerit lacus. Etiam porttitor et purus vel cursus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
Sed sit amet commodo quam. Aliquam efficitur lacinia enim, sed luctus risus varius sit amet. Aliquam faucibus, est ac euismod pulvinar, nunc quam hendrerit turpis, at sollicitudin lorem leo ac felis. Sed in erat sed ex imperdiet mattis vitae eu ligula. Aenean sapien justo, malesuada at sem vitae, luctus viverra massa. Pellentesque nec nisi pharetra, gravida nibh et, hendrerit mi. Nulla laoreet rhoncus orci, nec porta tortor pharetra ut. Duis maximus diam pharetra ipsum tempus aliquet. Phasellus scelerisque mi vulputate ipsum laoreet, at efficitur dolor tincidunt. Nam mauris ligula, laoreet at suscipit sit amet, tempus vel ex.
Sed sit amet mauris diam. Praesent eu dictum lacus. Morbi gravida auctor diam, in viverra lectus vehicula ut. Aliquam id placerat elit. Suspendisse dui nisl, mattis mollis magna id, ornare elementum nisi. Morbi posuere rhoncus fermentum. Praesent at purus et enim scelerisque tincidunt non quis ipsum. Integer pharetra neque in lectus consequat fringilla. Pellentesque tellus ligula, hendrerit id dictum eu, facilisis sit amet ipsum. Duis justo metus, elementum at sapien ut, finibus posuere nisl. Morbi aliquam nisl dolor, in porta mauris eleifend tempor. Maecenas id enim tincidunt, feugiat mi ultrices, finibus diam. Fusce aliquam ipsum sed nisi dictum, sit amet molestie ligula imperdiet. Vivamus imperdiet, purus molestie sollicitudin mollis, ligula elit dapibus nunc, et aliquet eros risus ac neque.
Nam finibus consectetur enim, imperdiet efficitur libero ullamcorper non. Praesent quis mauris ipsum. In lacinia enim ut ante finibus bibendum. Suspendisse maximus turpis massa, faucibus auctor ipsum consectetur eget. Nam pretium ex sodales odio convallis, id volutpat metus fringilla. Etiam a posuere nisi. Donec convallis libero dui."""
    downlink = 'https://s3.wasabisys.com/degoo-production-large-file-us-east1.degoo.info/ADCGai/7tL8DQ/zip/ChRWlrQP_4wh4VyG5v-MDkhl27rc8hAA.zip?AWSAccessKeyId=QCIW8NA9JUUC4PKQYZTJ&Expires=1624978295&Signature=8BLx%2FVu2dpdffq60w25QrFx5aV0%3D&ngsw-bypass=1'

    log = appinfo('Application', 2, lorem, 'Adobe INC.', 'Photos;Design', '')
    log.show()


    apply_stylesheet(app, theme='light_blue.xml')
    sys.exit(app.exec_())
