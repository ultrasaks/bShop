import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import *
from qt_material import apply_stylesheet

WHITE_THEME = ['#e6e6e6', '#f5f5f5', '#C8C8C8', '#2979ff', '#AFCCFF']
DARK_THEME = ['#31363b', '#232629', '#373737', '#448aff', '#313677']


class animatedPushButton(QPushButton):
    clicked = pyqtSignal()

    def __init__(self, *args, dark=False, **kwargs):
        global WHITE_THEME, DARK_THEME
        if not dark:
            THEME = WHITE_THEME
        else:
            THEME = DARK_THEME
        QPushButton.__init__(self, *args, **kwargs)
        self.installEventFilter(self)

        self.co_set = 0

        byar = QByteArray()
        byar.append('zcolor')

        tyar = QByteArray()
        tyar.append('texcolor')

        self.on_anim = QPropertyAnimation(self, byar)
        self.on_anim.setEndValue(THEME[4])
        self.on_anim.setDuration(150)
        self.on_anim.setLoopCount(1)

        self.click_anim = QPropertyAnimation(self, byar)
        self.click_anim.setEndValue(THEME[3])
        self.click_anim.setDuration(30)
        self.click_anim.setLoopCount(1)

        self.click_anim_text = QPropertyAnimation(self, tyar)
        self.click_anim_text.setEndValue('#ffffff')
        self.click_anim_text.setDuration(30)
        self.click_anim_text.setLoopCount(1)

        self.offclick_anim_text = QPropertyAnimation(self, tyar)
        self.offclick_anim_text.setEndValue(THEME[3])
        self.offclick_anim_text.setDuration(150)
        self.offclick_anim_text.setLoopCount(1)

        self.off_anim = QPropertyAnimation(self, byar)
        self.off_anim.setEndValue(THEME[0])
        self.off_anim.setDuration(150)
        self.off_anim.setLoopCount(1)

        self.enterEvent = self.onHovered
        self.leaveEvent = self.offHovered
        self.mousePressEvent = self.onClicked
        # self.mouseReleaseEvent = self.offClicked
        # self.pressed = self.onClicked

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def onHovered(self, *args, **kwargs):
        if self.isEnabled():
            self.on_anim.start()

    def offHovered(self, *args, **kwargs):
        if self.isEnabled():
            self.off_anim.start()

    def onClicked(self, QMouseEvent):
        if self.isEnabled():
            if QMouseEvent.button() == Qt.LeftButton:
                # self.setStyleSheet('color: white;')
                self.on_anim.stop()
                self.click_anim.start()
                self.click_anim_text.start()
                self.click_anim_text.stop()
                self.offclick_anim_text.stop()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.isEnabled():
            if QMouseEvent.button() == Qt.LeftButton:
                self.clicked.emit()
                self.on_anim.start()
                self.click_anim.stop()
                self.click_anim_text.stop()
                self.offclick_anim_text.start()
                # self.setStyleSheet('color: #2979ff;')

    def getBackColor(self):
        return self.palette().color(QPalette.Window)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'background-color: rgba(%d,%d,%d,%d);' % (
            color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Abackground-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    def getTextColor(self):
        return self.palette().color(self.pal_ele)

    def setTextColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'color: rgba(%d,%d,%d,%d);' % (
            color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Acolor:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    pal_ele = QPalette.Window
    zcolor = pyqtProperty(QColor, getBackColor, setBackColor)
    texcolor = pyqtProperty(QColor, getTextColor, setTextColor)


class animatedCard(QGroupBox):
    clicked = pyqtSignal()

    def __init__(self, *args, dark=False, basecolor=WHITE_THEME[1], clickcolor=WHITE_THEME[2], oncolor=WHITE_THEME[0],
                 shadowRadius=30, ontime=50, offtime=150):
        global WHITE_THEME, DARK_THEME
        if dark:
            if basecolor == WHITE_THEME[1]:
                basecolor = DARK_THEME[1]
            if clickcolor == WHITE_THEME[2]:
                clickcolor = DARK_THEME[2]
            if oncolor == WHITE_THEME[0]:
                oncolor = DARK_THEME[0]

        QGroupBox.__init__(self,  *args)

        self.installEventFilter(self)
        self.new_type = False

        self.basecolor, self.clickcolor, self.oncolor, self.shadowRadius = basecolor, clickcolor, oncolor, shadowRadius

        self.co_set = 0

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.setGraphicsEffect(self.shadow)

        byar = QByteArray()
        byar.append('zcolor')

        self.an = QPropertyAnimation(self.shadow, b'blurRadius')
        self.an.setEndValue(self.shadowRadius)
        self.an.setDuration(150)
        self.an.setLoopCount(1)

        self.an2 = QPropertyAnimation(self.shadow, b'blurRadius')
        self.an2.setEndValue(0)
        self.an2.setDuration(150)
        self.an2.setLoopCount(1)

        self.click_anim = QPropertyAnimation(self, byar)
        self.click_anim.setEndValue(self.clickcolor)
        self.click_anim.setDuration(30)
        self.click_anim.setLoopCount(1)

        self.off_anim = QPropertyAnimation(self, byar)
        self.off_anim.setEndValue(self.basecolor)
        self.off_anim.setDuration(offtime)
        self.off_anim.setLoopCount(1)
        self.off_anim.start()
        q = byar.data()

        self.on_anim = QPropertyAnimation(self, byar)
        self.on_anim.setEndValue(self.oncolor)
        self.on_anim.setDuration(ontime)
        self.on_anim.setLoopCount(1)

        self.enterEvent = self.onHovered
        self.leaveEvent = self.offHovered
        self.mousePressEvent = self.onClicked

    def setNewType(self):
        self.new_type = True

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def onHovered(self, *args, **kwargs):
        if self.isEnabled():
            self.an.start()
            self.an2.stop()
            self.on_anim.start()

    def offHovered(self, *args, **kwargs):
        if self.isEnabled():
            self.an.stop()
            self.an2.start()
            self.off_anim.start()

    def onClicked(self, QMouseEvent):
        if self.isEnabled():
            if QMouseEvent.button() == Qt.LeftButton:
                self.on_anim.stop()
                self.click_anim.start()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.isEnabled():
            if QMouseEvent.button() == Qt.LeftButton:
                self.clicked.emit()
                self.click_anim.stop()
                self.off_anim.start()

    def getBackColor(self):
        return self.palette().color(QPalette.Window)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        if self.new_type:
            bg_new = 'background-color: rgba(%d,%d,%d,%d);padding:0px;padding-top: 0px;line-height: 1px;' \
                     'padding-top: 0px' % (color.red(), color.green(), color.blue(), color.alpha())

        else:
            bg_new = 'background-color: rgba(%d,%d,%d,%d);' % (
                color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Abackground-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    def getTextColor(self):
        return self.shadow.xOffset(), self.shadow.yOffset()

    def setTextColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'color: rgba(%d,%d,%d,%d);' % (
            color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Acolor:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    zcolor = pyqtProperty(QColor, getBackColor, setBackColor)
    texcolor = pyqtProperty(QColor, getTextColor, setTextColor)


class animatedLineEdit(QLineEdit):
    clicked = pyqtSignal(object)

    def __init__(self, *args, dark=False, **kwargs):
        global WHITE_THEME, DARK_THEME
        if not dark:
            THEME = WHITE_THEME
        else:
            THEME = DARK_THEME
        QLineEdit.__init__(self, *args, **kwargs)
        self.installEventFilter(self)
        self.co_set = 0
        byar = QByteArray()
        byar.append('texcolor')

        self.click_anim = QPropertyAnimation(self, byar)
        self.click_anim.setEndValue(THEME[3])
        self.click_anim.setDuration(170)
        self.click_anim.setLoopCount(1)

        self.off_anim = QPropertyAnimation(self, byar)
        self.off_anim.setEndValue(THEME[1])
        self.off_anim.setDuration(150)
        self.off_anim.setLoopCount(1)
        self.off_anim.start()

        self.on_anim = QPropertyAnimation(self, byar)
        self.on_anim.setEndValue(THEME[0])
        self.on_anim.setDuration(50)
        self.on_anim.setLoopCount(1)

        self.mousePressEvent = self.onClicked

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def offClicked(self, *args, **kwargs):
        if self.isEnabled():
            self.off_anim.start()

    def onClicked(self, *args, **kwargs):
        self.clicked.emit(self)  # +++
        if self.isEnabled():
            self.click_anim.start()

    def getBackColor(self):
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'border: 2px solid rgba(%d,%d,%d,%d); border-width: 0 0 2px 0;' % (
            color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Aborder:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    pal_ele = QPalette.Window
    texcolor = pyqtProperty(QColor, getBackColor, setBackColor)


# сейчас не использую
class mishLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


# сейчас не использую
class mishSVG(QSvgWidget):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


# сейчас не использую
class animatedSVG(mishSVG):
    clicked = pyqtSignal()

    def __init__(self, *args, basecolor='#f5f5f5', clickcolor='#C8C8C8', oncolor='#e6e6e6'):
        mishSVG.__init__(self, *args)
        self.installEventFilter(self)
        self.basecolor, self.clickcolor, self.oncolor = basecolor, clickcolor, oncolor

        self.co_set = 0

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(0)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.setGraphicsEffect(self.shadow)

        byar = QByteArray()
        byar.append('zcolor')

        self.an = QPropertyAnimation(self.shadow, b'blurRadius')
        self.an.setEndValue(5)
        self.an.setDuration(100)
        self.an.setLoopCount(1)

        self.an2 = QPropertyAnimation(self.shadow, b'blurRadius')
        self.an2.setEndValue(0)
        self.an2.setDuration(100)
        self.an2.setLoopCount(1)

        self.click_anim = QPropertyAnimation(self, byar)
        self.click_anim.setEndValue(self.clickcolor)
        self.click_anim.setDuration(30)
        self.click_anim.setLoopCount(1)

        self.off_anim = QPropertyAnimation(self, byar)
        self.off_anim.setEndValue(self.basecolor)
        self.off_anim.setDuration(150)
        self.off_anim.setLoopCount(1)
        self.off_anim.start()

        self.on_anim = QPropertyAnimation(self, byar)
        self.on_anim.setEndValue(self.oncolor)
        self.on_anim.setDuration(100)
        self.on_anim.setLoopCount(1)

        self.enterEvent = self.onHovered
        self.leaveEvent = self.offHovered
        self.mousePressEvent = self.onClicked

    def setColor(self, basecolor, clickcolor, oncolor):
        self.basecolor, self.clickcolor, self.oncolor = basecolor, clickcolor, oncolor

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def onHovered(self, *args, **kwargs):
        if self.isEnabled():
            self.on_anim.start()
            # self.an.start()
            # self.an2.stop()

    def offHovered(self, *args, **kwargs):
        if self.isEnabled():
            # self.an.stop()
            # self.an2.start()
            self.off_anim.start()

    def onClicked(self, *args, **kwargs):
        if self.isEnabled():
            self.on_anim.stop()
            self.click_anim.start()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.isEnabled():
            if QMouseEvent.button() == Qt.LeftButton:
                self.clicked.emit()
                self.off_anim.start()
                self.click_anim.stop()

    def getBackColor(self):
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'background-color: rgba(%d,%d,%d,%d);border-radius: 4px;' % (
            color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Abackground-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    def getTextColor(self):
        return self.shadow.xOffset(), self.shadow.yOffset()

    def setTextColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        bg_new = 'color: rgba(%d,%d,%d,%d);' % (
            color.red(), color.green(), color.blue(), color.alpha())

        for k, sty in enumerate(sss):
            if re.search('\Acolor:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('; '.join(sss))

    pal_ele = QPalette.Window
    zcolor = pyqtProperty(QColor, getBackColor, setBackColor)
    texcolor = pyqtProperty(QColor, getTextColor, setTextColor)


# недоработано
class PosterBlur(QGroupBox):
    def __init__(self, *args):
        # QGroupBox().__init__(*args)
        super().__init__(None)
        self.setAttribute(Qt.WA_StyledBackground)
        widget = QWidget()
        widget.setStyleSheet("""QWidget{ background-image:url(icons/poster.jpg);}""")
        blur_effect = QGraphicsBlurEffect(blurRadius=5)
        widget.setGraphicsEffect(blur_effect)

        self._label = QGroupBox()
        self.label.setStyleSheet(""" background-color : transparent;""")
        self.label.setContentsMargins(10, 0, 10, 0)

        lay = QVBoxLayout(self)
        lay.addWidget(widget)

    @property
    def label(self):
        return self._label


if __name__ == "__main__":
    class Test(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent)
            self.setWindowTitle('Animation test')
            self.main = QVBoxLayout()
            bruh = QVBoxLayout()
            test = PosterBlur()
            bruh.addWidget(QLabel('Test'))
            test.setLayout(bruh)
            test.setFixedSize(400, 500)
            self.main.addWidget(test)
            # self.linedits = {}
            # for q in range(5):
            #     layout = QHBoxLayout()
            #     for i in range(5):
            #         linedit = animatedLineEdit(f'Line{str(q)}{str(i)}')
            #         linedit.setFixedSize(100, 30)
            #         linedit.setFocusPolicy(Qt.ClickFocus)
            #         self.linedits[f'{q}{i}'] = linedit
            #         linedit.clicked.connect(self.on_clicked)
            #         layout.addWidget(linedit)
            #     self.main.addLayout(layout)
            self.setLayout(self.main)

        # def on_clicked(self, lineEdit):
        #     for le in self.linedits.values():
        #         if le != lineEdit:
        #             le.offClicked()
        #         else:
        #             lineEdit.setFocus()


    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    main = Test()
    main.show()

    app.exec_()
