import requests
import ctypes
import ast
from os import path, mkdir
from animbtn import *

username, userpass = '', ''



class LoginWidg(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.linedits = {}

        self.vertLayout = QVBoxLayout()
        self.logregwidg = QTabWidget()
        self.log = QWidget()
        self.reg = QWidget()
        self.err = QLabel()

        self.welcomeLbl = QLabel('Welcome')
        self.welcomeLbl.setAlignment(Qt.AlignHCenter)
        self.welcomeLbl.setFont(QFont('bruh', 24))
        self.err.setAlignment(Qt.AlignHCenter)

        self.logregwidg.addTab(self.log, 'Sign in')
        self.logregwidg.addTab(self.reg, 'Sign up')
        self.logUI()
        self.regUI()
        self.logregwidg.setFixedSize(300, 260)

        self.vertLayout.addStretch()
        self.vertLayout.addWidget(self.welcomeLbl)
        self.vertLayout.addWidget(self.logregwidg)
        self.vertLayout.addWidget(self.err)
        self.vertLayout.addStretch()
        self.vertLayout.setAlignment(Qt.AlignHCenter)
        self.setLayout(self.vertLayout)

        self.setGeometry(300, 300, 680, 470)

        qt_rectangle = self.frameGeometry()
        center_Point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_Point)
        self.move(qt_rectangle.topLeft())
        self.setWindowTitle('test')
        self.show()

    def logUI(self):
        self.logLayout = QVBoxLayout()

        self.name = animatedLineEdit(self)
        self.name.setPlaceholderText('Login')
        self.name.setFocusPolicy(Qt.ClickFocus)
        self.linedits['name'] = self.name
        self.name.clicked.connect(self.on_clicked)

        self.password = animatedLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setFocusPolicy(Qt.ClickFocus)
        self.password.setEchoMode(animatedLineEdit.Password)
        self.linedits['password'] = self.password
        self.password.clicked.connect(self.on_clicked)

        self.logBtn = animatedPushButton("Sign in")
        self.log.setLayout(self.logLayout)
        self.logBtn.setEnabled(False)
        QApplication.processEvents()
        self.logBtn.clicked.connect(lambda: self.auth(self.name.text(), self.password.text()))

        QApplication.processEvents()
        self.name.textChanged[str].connect(self.auth_btn_on)
        self.password.textChanged[str].connect(self.auth_btn_on)

        self.logLayout.addWidget(self.name)
        self.logLayout.addWidget(self.password)
        self.logLayout.addWidget(self.logBtn)

    def auth(self, log, pas):
        self.err.setText('Signing in...')
        QApplication.processEvents()
        status = requests.get(f'http://jointprojects.tk/auth.php?login={log}&password={pas}').text
        QApplication.processEvents()
        self.err.setText(status)
        if status == 'Success':
            self.shop = Main()
            self.shop.show()
            self.hide()


    def auth_btn_on(self):
        if self.name.text() and self.password.text():
            self.logBtn.setEnabled(True)
        else:
            self.logBtn.setEnabled(False)

    def regUI(self):
        self.regLayout = QVBoxLayout()
        self.name1 = animatedLineEdit(self)
        self.name1.setPlaceholderText('Login')
        self.name1.setFocusPolicy(Qt.ClickFocus)
        self.linedits['name1'] = self.name1
        self.name1.clicked.connect(self.on_clicked)

        self.password1 = animatedLineEdit(self)
        self.password1.setPlaceholderText('Password')
        self.password1.setEchoMode(animatedLineEdit.Password)
        self.password1.setFocusPolicy(Qt.ClickFocus)
        self.linedits['password1'] = self.password1
        self.password1.clicked.connect(self.on_clicked)

        self.password2 = animatedLineEdit(self)
        self.password2.setPlaceholderText('Repeat your password')
        self.password2.setEchoMode(animatedLineEdit.Password)
        self.password2.setFocusPolicy(Qt.ClickFocus)
        self.linedits['password2'] = self.password2
        self.password2.clicked.connect(self.on_clicked)

        self.regBtn = animatedPushButton("Sign up")
        self.cond = QCheckBox()
        self.cond.setMaximumWidth(20)
        self.chkLayout = QHBoxLayout()
        self.condtext = QLabel("I agree with <a href=\"http://jointprojects.tk\">terms and conditions</a>")
        self.condtext.setOpenExternalLinks(True)
        self.chkLayout.addWidget(self.cond)
        self.chkLayout.addWidget(self.condtext)

        self.reg.setLayout(self.regLayout)
        self.regBtn.setEnabled(False)
        self.regBtn.clicked.connect(lambda: self.registration(self.name1.text(), self.password1.text()))
        self.name1.textChanged[str].connect(self.registration_btn_on)
        self.password1.textChanged[str].connect(self.registration_btn_on)
        self.password2.textChanged[str].connect(self.registration_btn_on)
        self.cond.stateChanged.connect(self.registration_btn_on)

        self.regLayout.addWidget(self.name1)
        self.regLayout.addWidget(self.password1)
        self.regLayout.addWidget(self.password2)
        self.regLayout.addLayout(self.chkLayout)
        self.regLayout.addWidget(self.regBtn)

    def registration(self, log, pas):
        self.err.setText('Signing up...')
        status = requests.get(f'http://jointprojects.tk/register.php?login={log}&password={pas}').text
        self.err.setText(status)
        if status == 'Success':
            self.logregwidg.setCurrentIndex(0)
            self.err.setText('Successful! Now try to login in your new account.')

    def registration_btn_on(self):
        if self.name1.text() and len(self.password1.text()) >= 6 and self.password2.text() and self.cond.isChecked() \
                and (self.password1.text() == self.password2.text()):
            self.regBtn.setEnabled(True)
        else:
            self.regBtn.setEnabled(False)

    def on_clicked(self, lineEdit):
        for le in self.linedits.values():
            if le != lineEdit:
                le.offClicked()
            else:
                lineEdit.setFocus()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        QTimer.singleShot(0, self.initUI)

    def initUI(self):
        self.setGeometry(300, 300, 830, 670)
        qt_rectangle = self.frameGeometry()
        center_Point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_Point)
        self.move(qt_rectangle.topLeft())

        self.main = QHBoxLayout()
        self.main.addStretch()
        self.setLayout(self.main)
        self.hline = QVBoxLayout()
        self.main.setAlignment(Qt.AlignHCenter)

        self.applist = int(requests.get('http://jointprojects.tk/apps/applist.ini').text)
        self.bbb = QWidget()
        self.bbb.setLayout(self.hline)

        self.apps = QScrollArea()
        self.apps.setMinimumWidth(550)
        self.apps.setMinimumHeight(670)
        self.main.addWidget(self.apps)

        self.main.addStretch()
        QApplication.processEvents()
        for application_id in range(1, 10):#self.applist + 1):
            self.bbb.setMinimumHeight(170 * application_id + (20 * application_id))
            application_id = 2
            print(application_id, end=' ')
            app = animatedCard()
            applayout = QVBoxLayout()
            app.setLayout(applayout)
            app.setMinimumWidth(520)
            app.setFixedHeight(170)
            self.hline.addWidget(app)
            icon_and_name = QHBoxLayout()
            applayout.addLayout(icon_and_name)

            name = mishLabel('Name')
            name.setFont(QFont('Roboto', 18))
            details = mishLabel('Description')
            icon = mishLabel()
            icon.setFixedSize(64, 64)

            icon_and_name.addWidget(icon)
            icon_and_name.addWidget(name)
            applayout.addWidget(details)

            for _ in range(1):
                application_info = ast.literal_eval(
                    requests.get(f'http://jointprojects.tk/apps/{str(application_id)}/appinfo.ini').text)
                name.setText(application_info['name'])
                details.setText(application_info['description'])

                name.clicked.connect(lambda appinf = application_info, apid = application_id: self.test(appinf, apid))
                details.clicked.connect(lambda appinf = application_info, apid = application_id: self.test(appinf, apid))
                icon.clicked.connect(lambda appinf = application_info, apid = application_id: self.test(appinf, apid))
                app.clicked.connect(lambda appinf = application_info, apid = application_id: self.test(appinf, apid))

                if not path.exists('cache/'):
                    mkdir('cache')
                    ctypes.windll.kernel32.SetFileAttributesW(f'cache/', 2)
                if not path.exists(f'cache/{str(application_id)}/'):
                    mkdir(f'cache/{str(application_id)}/')
                    ctypes.windll.kernel32.SetFileAttributesW(f'cache/{str(application_id)}/', 2)
                if not path.exists(f'cache/{str(application_id)}/appinfo.ini'):
                    info_file = open(f'cache/{str(application_id)}/appinfo.ini', 'w')
                    info_file.write(str(application_info))
                    info_file.close()
                if not path.exists(f'cache/{str(application_id)}/icon.svg') or \
                        open(f'cache/{str(application_id)}/appinfo.ini', 'r').read() != str(application_info):
                    icon_get = requests.get(application_info['icon_link'])
                    icon_file = open(f'cache/{str(application_id)}/icon.svg', 'wb')
                    icon_file.write(icon_get.content)
                    icon_file.close()

                pixmap = QPixmap(f'cache/{str(application_id)}/icon.svg')
                icon.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))
                icon.setAlignment(Qt.AlignCenter)
                icon.setFixedSize(76, 76)
                icon.setStyleSheet('QWidget  {background-color: #E6E0D4; border: 2px solid #E6E0D4; border-radius: 8px;} ')
                application_info['id'] = application_id
            QApplication.processEvents()
            self.apps.setWidget(self.bbb)
        self.q = appinfo('0', 0, '0', '0', '0', '0')


    def test(self, inf, id):
        #self.q = 0
        self.q.hide()
        self.q = appinfo(inf['name'], id, inf['full_description'], inf['uploader'], inf['tags'], inf['download_link'])
        self.q.show()


class appinfo(QWidget):
    def __init__(self, name, app_id, descr, author, tags, dowlink):
        super().__init__()
        self.name = name
        self.appid = app_id
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

    def setup(self, name, app_id, descr, author, tags, dowlink):
        #super().__init__()
        self.name = name
        self.appid = app_id
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


        self.nameL = QLabel(self.name)
        self.nameL.setFont(QFont('Roboto', 18))
        self.descrScroll = QScrollArea()
        self.descrLayout = QHBoxLayout()
        self.description = QLabel(self.descr)
        self.descrScroll.setWidget(self.description)
        self.icon = mishSVG(f'cache/{str(self.appid)}/icon.svg')
        self.fromL = QLabel(self.author)
        self.tags = QHBoxLayout()
        self.downloadBtn = animatedPushButton('Download')

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
        self.appdetLayout.addLayout(self.tags)
        self.appdetLayout.addWidget(self.downloadBtn)

        self.appicLayout.addWidget(self.icon)
        self.appicLayout.addLayout(self.appdetLayout)


        self.descrScroll.setStyleSheet('QWidget  {background-color: #f5f5f5; border: 1px solid #f5f5f5; border-radius: 3px;} ')
        self.description.setFixedSize(self.description.width() + 20, self.description.height() + 10)

        self.icon.setFixedSize(128, 128)
        self.icon.setStyleSheet('QWidget  {background-color: #f5f5f5; border: 10px solid #f5f5f5; border-radius: 8px;} ')

        self.downloadBtn.clicked.connect(lambda: self.download(self.downLink))

        # self.MainLayout.addWidget(self.icon)
        # self.MainLayout.addWidget(self.nameL)
        self.MainLayout.addLayout(self.appicLayout)
        self.MainLayout.addWidget(self.descrScroll)

    def download(self, link):
        print('piss')
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    log = LoginWidg()

    apply_stylesheet(app, theme='light_blue.xml')
    sys.exit(app.exec_())