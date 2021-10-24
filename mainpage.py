from animbtn import *
from caching import cache
import requests
from ast import literal_eval
from download import download, check_downloaded
from os import listdir, path, popen, mkdir


WHITE_THEME = ['#E6E0D4', '#f5f5f5', '#EBEBEB']
DARK_THEME = ['#1E1D1B', '#232629', '#141414']
settings = {}



def empty_settings():
    settings["dark_theme"] = False
    print(settings)



if not path.exists('settings.ini'):
    empty_settings()
else:
    with open('settings.ini', 'r') as settings_file:
        try:
            settings = literal_eval(settings_file.read())
        except ValueError:
            empty_settings()
        except SyntaxError:
            empty_settings()
THEME = WHITE_THEME
if settings['dark_theme']:
    THEME = DARK_THEME
objTheme = settings['dark_theme']
applist = '12342'

appPics = {'Top': []}
appNames = {'Top': []}
appCards = {'Top': []}
BLACK = False


class mainStore(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icons/icon.ico'))
        QTimer.singleShot(0, self.initUI)

    def initUI(self):
        # QApplication.processEvents()
        self.setWindowTitle('bShop')
        self.setGeometry(300, 300, 1130, 670)
        self.setMinimumWidth(5 * 140 + 260)
        qt_rectangle = self.frameGeometry()
        center_Point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_Point)
        self.move(qt_rectangle.topLeft())

        self.MainLayout = QHBoxLayout()

        self.MainFrame = QFrame()
        self.MainFrame.setStyleSheet('border: 0px;border-radius: 0px;')
        self.MainLayout.addWidget(self.MainFrame)

        self.AppsLayout = QVBoxLayout()
        self.AppsLayout.setAlignment(Qt.AlignTop)

        #######
        self.AppAboutLayout = QVBoxLayout()
        self.AppAboutLayout.setAlignment(Qt.AlignTop)
        self.AppAboutFrame = QFrame()
        self.AppAboutFrame.setStyleSheet('border: 0px;border-radius: 0px;')
        self.AppAboutFrame.setLayout(self.AppAboutLayout)
        self.MainLayout.addWidget(self.AppAboutFrame)
        self.AppAboutFrame.hide()

        self.appdetLayout = QVBoxLayout()
        self.appicLayout = QHBoxLayout()

        name, descr, appid, author = 'test', 'lorem ipsum', '2', 'bruh'
        # ToDo: приложение
        self.nameL = QLabel(name)
        self.nameL.setFont(QFont('Roboto', 18))
        self.descrScroll = QScrollArea()
        descrLayout = QHBoxLayout()
        self.description = QLabel()
        self.descrScroll.setWidget(self.description)
        self.icon = QLabel()
        self.fromL = QLabel(author)
        tags = QHBoxLayout()
        self.downloadbtn = animatedPushButton('Download', dark=objTheme)
        self.downloadbtn.clicked.connect(self.download_app)

        tags.setAlignment(Qt.AlignLeft)
        tagdef = QLabel('Tags:')
        tagdef.setFixedWidth(31)
        tags.addWidget(tagdef)
        tegi = ['tag', 'tagg']  # tagi.split(';')
        for tag in tegi:
            temp_tag = QLabel(rf'<a href=\"\">{tag}</a>')
            temp_tag.setFixedWidth(len(tag) * 7)
            # temp_tag.linkActivated.connect(lambda: self.download('test'))
            tags.addWidget(temp_tag)

        self.appdetLayout.addWidget(self.nameL)
        self.appdetLayout.addWidget(self.fromL)
        self.appdetLayout.addLayout(tags)
        self.appdetLayout.addWidget(self.downloadbtn)

        self.appicLayout.addWidget(self.icon)
        self.appicLayout.addLayout(self.appdetLayout)

        self.descrScroll.setStyleSheet(
            f'QWidget  {"{background-color:"} {THEME[1]}; border: 1px solid {THEME[1]}; border-radius: 3px;{"}"} ')
        self.description.setFixedWidth(5 * 120)
        # self.description.setFixedHeight(100)
        self.description.setWordWrap(True)

        self.icon.setFixedSize(128, 128)
        self.icon.setStyleSheet(
            f'background-color: {THEME[1]}; border: 10px solid {THEME[1]}; border-radius: 8px;')

        # self.self.downloadbtn.clicked.connect(lambda: self.download(self.downLink))

        # self.MainLayout.addWidget(self.icon)
        # self.MainLayout.addWidget(self.self.nameL)
        self.AppAboutLayout.addLayout(self.appicLayout)
        self.AppAboutLayout.addWidget(self.descrScroll)
        ####

        # ToDo: downloads
        self.DownloadsLayout = QVBoxLayout()
        self.DownloadsFrame = QFrame()
        self.DownloadsFrame.setStyleSheet('border: 0px;border-radius: 0px;')
        self.MainLayout.addWidget(self.DownloadsFrame)
        self.DownloadsFrame.setLayout(self.DownloadsLayout)
        self.DownloadsFrame.hide()

        downloadsTitle = QLabel('Your applications:')
        downloadsTitle.setFont(QFont('Roboto', 15))
        downloadsTitle.setFixedHeight(40)

        self.downloadAppsLayout = QVBoxLayout()
        downloadScroll = QScrollArea(self)
        downloadScroll.setWidgetResizable(True)
        downloadScrollW = QWidget()
        downloadScrollW.setLayout(self.downloadAppsLayout)
        downloadScroll.setWidget(downloadScrollW)

        self.DownloadsLayout.addWidget(downloadsTitle)
        self.DownloadsLayout.addSpacing(30)
        self.DownloadsLayout.addWidget(downloadScroll)
        self.downloadAppsLayout.addWidget(QLabel(' '))

        self.SearchLayout = QVBoxLayout()
        self.SearchFrame = QFrame()
        self.SearchFrame.setStyleSheet('border: 0px;border-radius: 0px;')
        self.MainLayout.addWidget(self.SearchFrame)
        self.SearchFrame.setLayout(self.SearchLayout)
        self.SearchFrame.hide()

        self.searchGroup = QGroupBox()
        searchGroupLayout = QVBoxLayout()
        self.searchGroup.setLayout(searchGroupLayout)
        self.searchGroup.setFixedHeight(140)
        self.searchGroup.setStyleSheet('padding:0px;padding-top: 0px;')

        self.searchAppsLayout = QVBoxLayout()
        self.appScroll = QScrollArea(self)
        self.appScroll.setWidgetResizable(True)
        self.appScrollW = QWidget()
        self.appScrollW.setLayout(self.searchAppsLayout)
        self.appScroll.setWidget(self.appScrollW)
        # self.appScrollW.setMinimumWidth(550)
        # self.appScrollW.setMinimumHeight(550)
        # for i in range(5):
        self.searchAppsLayout.addWidget(QLabel(' '))

        self.searchEdit = animatedLineEdit(dark=objTheme)
        self.searchEdit.setPlaceholderText('Write something here...')

        searchBtn = animatedPushButton('Search', dark=objTheme)
        searchBtn.clicked.connect(self.search)

        searchGroupLayout.addWidget(self.searchEdit)
        searchGroupLayout.addWidget(searchBtn)

        self.SearchLayout.addWidget(self.searchGroup)
        self.SearchLayout.addSpacing(30)
        self.SearchLayout.addWidget(self.appScroll)
        # ToDo: Поиск

        self.MainFrame.setLayout(self.AppsLayout)

        self.SettingsLayout = QVBoxLayout()
        self.SettingsLayout.setAlignment(Qt.AlignTop)
        self.SettingsFrame = QFrame()
        self.SettingsFrame.setStyleSheet('border: 0px;border-radius: 0px;')
        self.SettingsFrame.setLayout(self.SettingsLayout)
        self.MainLayout.addWidget(self.SettingsFrame)
        self.SettingsFrame.hide()

        settingsTitle = QLabel('Settings')
        settingsTitle.setFont(QFont('Roboto', 15))
        settingsTitle.setFixedHeight(40)

        themeGroup = QGroupBox()
        themeGroup.setTitle('theme')
        themeGroup.setFixedHeight(100)
        themeLayout = QHBoxLayout()
        themeGroup.setLayout(themeLayout)

        self.themeCBox = QCheckBox('Dark theme(beta)')
        if settings['dark_theme']:
            self.themeCBox.setChecked(True)
        themeLayout.addWidget(self.themeCBox)
        themeLayout.addWidget(QLabel(' '))

        accountGroup = QGroupBox()
        accountGroup.setTitle('account settings')
        accountLayout = QVBoxLayout()
        accountGroup.setLayout(accountLayout)

        accountTitle = QLabel('Name:')
        accountTitle.setFont(QFont('Roboto', 12))
        accountName = QLabel(settings['login'])
        accountName.setFont(QFont('Roboto', 10))
        accountExitBtn = animatedPushButton('Sign out', dark=objTheme)
        accountExitBtn.clicked.connect(self.logOff)

        accountLayout.addWidget(accountTitle)
        accountLayout.addWidget(accountName)
        accountLayout.addSpacing(40)
        accountLayout.addWidget(accountExitBtn)

        pref = QGroupBox()
        prefLayout = QVBoxLayout()
        prefLayout.setContentsMargins(0, 0, 0, 0)
        pref.setLayout(prefLayout)
        pref.setStyleSheet('QGroupBox {padding:10px;padding-top: 10px}')
        savePrefBtn = animatedPushButton('Save changes', dark=objTheme)
        savePrefBtn.setFixedHeight(20)
        savePrefBtn.clicked.connect(self.savePreferences)
        prefWarning = QLabel('*Changes will take effect after restarting the program')
        prefWarning.setFixedHeight(20)
        prefLayout.addWidget(savePrefBtn)
        prefLayout.addWidget(prefWarning)


        self.SettingsLayout.addWidget(settingsTitle)
        self.SettingsLayout.addWidget(themeGroup)
        self.SettingsLayout.addWidget(accountGroup)
        self.SettingsLayout.addWidget(pref)
        self.SettingsLayout.addWidget(QLabel(' '))

        #ToDo: settings

        self.homeBtnLayout = QHBoxLayout()
        self.homeBtnLayout.setAlignment(Qt.AlignVCenter)
        self.homeBtnText = QLabel('Home')
        self.homeBtn = animatedCard(shadowRadius=15, dark=objTheme)
        self.homeBtn.setLayout(self.homeBtnLayout)
        self.homeBtnText.setFont(QFont('Roboto', 12))
        self.homeBtn.setFixedSize(200, 50)
        self.homeBtn.setBruh()
        self.homeBtnIcon = QSvgWidget('icons/home.svg')
        self.homeBtnIcon.setFixedSize(25, 25)
        self.homeBtnLayout.addWidget(self.homeBtnIcon)
        self.homeBtnLayout.addWidget(self.homeBtnText)
        self.homeBtn.clicked.connect(self.showMain)

        self.settingsBtnLayout = QHBoxLayout()
        self.settingsBtnLayout.setAlignment(Qt.AlignVCenter)
        self.settingsBtnText = QLabel('Settings')
        self.settingsBtn = animatedCard(shadowRadius=15, dark=objTheme)
        self.settingsBtn.setLayout(self.settingsBtnLayout)
        self.settingsBtnText.setFont(QFont('Roboto', 12))
        self.settingsBtn.setFixedSize(200, 50)
        self.settingsBtn.setBruh()
        self.settingsBtnIcon = QSvgWidget('icons/settings.svg')
        self.settingsBtnIcon.setFixedSize(25, 25)
        self.settingsBtnLayout.addWidget(self.settingsBtnIcon)
        self.settingsBtnLayout.addWidget(self.settingsBtnText)
        self.settingsBtn.clicked.connect(self.showSettings)

        self.libraryBtnLayout = QHBoxLayout()
        self.libraryBtnLayout.setAlignment(Qt.AlignVCenter)
        self.libraryBtnText = QLabel('My apps')
        self.libraryBtn = animatedCard(shadowRadius=15, dark=objTheme)
        self.libraryBtn.setLayout(self.libraryBtnLayout)
        self.libraryBtnText.setFont(QFont('Roboto', 12))
        self.libraryBtn.setFixedSize(200, 50)
        self.libraryBtn.setBruh()
        self.libraryBtnIcon = QSvgWidget('icons/app.svg')
        self.libraryBtnIcon.setFixedSize(25, 25)
        self.libraryBtnLayout.addWidget(self.libraryBtnIcon)
        self.libraryBtnLayout.addWidget(self.libraryBtnText)
        self.libraryBtn.clicked.connect(self.showDownloads)

        self.searchBtnLayout = QHBoxLayout()
        self.searchBtnLayout.setAlignment(Qt.AlignVCenter)
        self.searchBtnText = QLabel('Search')
        self.searchBtn = animatedCard(shadowRadius=15, dark=objTheme)
        self.searchBtn.setLayout(self.searchBtnLayout)
        self.searchBtnText.setFont(QFont('Roboto', 12))
        self.searchBtn.setFixedSize(200, 50)
        self.searchBtn.setBruh()
        self.searchBtnIcon = QSvgWidget('icons/search.svg')
        self.searchBtnIcon.setFixedSize(25, 25)
        self.searchBtnLayout.addWidget(self.searchBtnIcon)
        self.searchBtnLayout.addWidget(self.searchBtnText)
        self.searchBtn.clicked.connect(self.showSearch)

        self.rDock = QVBoxLayout()
        self.rDock.setContentsMargins(0, 10, 0, 0)
        self.rDockGroup = QGroupBox()
        self.rDockGroup.setStyleSheet(
            'QGroupBox {padding:0px;padding-top: 0px;line-height: 1px;border-radius: 1px}')
        self.rDockGroup.setLayout(self.rDock)
        self.rDockGroup.setFixedWidth(200)
        self.rDock.setAlignment(Qt.AlignTop)

        self.rDock.addWidget(self.homeBtn)
        self.rDock.addWidget(self.libraryBtn)
        self.rDock.addWidget(self.settingsBtn)
        self.rDock.addWidget(self.searchBtn)

        self.MainLayout.addWidget(self.rDockGroup)
        self.setLayout(self.MainLayout)

        self.Top = QHBoxLayout()
        self.Top.setContentsMargins(0, 0, 0, 0)
        self.Top.setAlignment(Qt.AlignLeft)
        self.TopG = QGroupBox()
        self.TopG.setTitle('top apps this month')
        self.TopG.setLayout(self.Top)
        self.TopG.setFixedHeight(170)
        self.TopG.setMinimumWidth(5 * 140)
        self.AppsLayout.addWidget(self.TopG)
        self.Top.addStretch()
        self.TopG.setStyleSheet('padding:0px;padding-top: 0px;line-height: 1px;border-radius: 1px')

        for _ in range(5):
            # app = _#int(app)
            appGL = QVBoxLayout()
            appGL.setContentsMargins(0, 10, 0, 10)
            appGL.setAlignment(Qt.AlignCenter)
            appG = animatedCard(basecolor=THEME[2], dark=objTheme)
            appG.setStyleSheet('border-radius: 10px')
            appG.setLayout(appGL)
            appG.setFixedSize(120, 110)
            # application_info = cache().caching(app)
            # appIcon = QSvgWidget() # f'cache/{str(app)}/icon.svg')
            appIcon = QLabel()
            appIcon.setStyleSheet(f'background-color: {THEME[0]}')
            appIcon.setFixedSize(72, 72)
            appPics['Top'].append(appIcon)
            appName = QLabel('Application')  # application_info['name'])
            appName.setAlignment(Qt.AlignCenter)
            appNames['Top'].append(appName)
            appGL.addWidget(appIcon)
            appGL.addWidget(appName)
            self.Top.addWidget(appG)
            self.Top.addStretch()

            appCards['Top'].append(appG)
            # appG.clicked.connect(self.showApp)
            QApplication.processEvents()
        applist = requests.get('http://jointprojects.tk/apps/gettop.php').content.decode("utf-8")
        QApplication.processEvents()
        place = 0
        for app in applist:
            app = int(app)
            application_info = cache().caching(app)
            appPics['Top'][place].setStyleSheet(
                f'image: url(cache/{str(app)}/icon.png); background-color: {THEME[0]}')
            appNames['Top'][place].setText(application_info['name'])
            appCards['Top'][place].clicked.connect(
                lambda id=app, inf=application_info: self.showApp(id, inf))
            place += 1
            QApplication.processEvents()

        self.AppsLayout.addSpacing(20)

        posterGroupLayout = QVBoxLayout()
        posterGroupLayout.setContentsMargins(0, 0, 0, 0)
        posterGroup = QGroupBox()
        posterGroup.setLayout(posterGroupLayout)
        posterGroupLayout.addWidget(QLabel(' '))

        self.posterTitle, self.posterDescription = QLabel('Announcement sample'), QLabel(
            'Lorem ipsum dolor sit amet')
        self.posterTitle.setFixedHeight(40)
        self.posterTitle.setStyleSheet('background-color: rgba(230, 224, 224, 150); color: black')
        self.posterTitle.setFont(QFont('Roboto', 20))
        self.posterDescription.setFixedHeight(70)
        self.posterDescription.setWordWrap(True)
        self.posterDescription.setStyleSheet(
            'background-color: rgba(230, 224, 224, 150); color: black')

        posterGroupLayout.addWidget(self.posterTitle)
        posterGroupLayout.addWidget(self.posterDescription)

        posterGroup.setMaximumWidth(960)
        posterGroup.setFixedHeight(440)
        posterBlur = QGraphicsBlurEffect()
        posterBlur.setBlurRadius(25)
        posterGroup.setStyleSheet(
            'QGroupBox{padding:0px;padding-top: 0px;line-height: 0px;border-radius: 3px;background-image: url(icons/poster.jpg);}')
        self.AppsLayout.addWidget(posterGroup)

    def showApp(self, id, application_info):
        if not check_downloaded(id):
            self.downloadInfo = application_info
            self.downloadID = id
            self.downloadbtn.setEnabled(True)
        else:
            self.downloadbtn.setEnabled(False)

        self.MainFrame.hide()
        self.SearchFrame.hide()
        self.AppAboutFrame.show()
        self.DownloadsFrame.hide()
        self.SettingsFrame.hide()
        cache().bigIcCache(id)


        self.icon.setStyleSheet(f'image: url(cache/{str(id)}/iconB.png);background-color: {THEME[1]};'
                                f'border: 10px solid {THEME[1]}; border-radius: 8px;')
        self.nameL.setText(application_info['name'])
        self.fromL.setText(application_info['author'])
        self.description.setText(application_info['description'])



        # self.description.setFixedHeight((len(application_info['description']) // 100) * 20)
        self.description.setFixedHeight((application_info['description'].count('\n') * 20)+ 20)
        if self.description.height() == 0:
            self.description.setFixedHeight(20)

    def showMain(self):
        curSize = self.size()
        self.MainFrame.show()
        self.SearchFrame.hide()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.hide()
        self.SettingsFrame.hide()
        # self.resize(curSize)

    def showSearch(self):
        self.MainFrame.hide()
        self.SearchFrame.show()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.hide()
        self.SettingsFrame.hide()

    def showSettings(self):
        self.MainFrame.hide()
        self.SearchFrame.hide()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.hide()
        self.SettingsFrame.show()

    def showDownloads(self):
        self.MainFrame.hide()
        self.SearchFrame.hide()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.show()
        self.SettingsFrame.hide()
        if not path.exists('downloads'):
            mkdir('downloads')
        apps = listdir("downloads")
        if apps:
            for i in reversed(range(self.downloadAppsLayout.count())):
                self.downloadAppsLayout.itemAt(i).widget().deleteLater()
            for app_id in apps:
                if check_downloaded(app_id):
                    application_info = literal_eval(open(f'downloads/{app_id}/package_info.json', 'r').read())
                    appC = animatedCard(dark=objTheme)
                    appC.setFixedHeight(130)
                    appC.setContentsMargins(0, 0, 0, 0)

                    appCLayout = QHBoxLayout()
                    appCLayoutKostyl = QVBoxLayout()
                    appCLayoutKostyl.addLayout(appCLayout)
                    appCLayoutKostyl.setContentsMargins(0, 0, 0, 20)
                    appC.setLayout(appCLayoutKostyl)

                    appIcon = QLabel()
                    appIcon.setFixedSize(72, 72)
                    appCLayout.addWidget(appIcon)

                    name_and_author = QVBoxLayout()
                    appCLayout.addLayout(name_and_author)

                    appName = QLabel('AppName')
                    appName.setFont(QFont('Roboto', 15))
                    appName.setFixedHeight(30)
                    appAuthor = QLabel('Author')
                    name_and_author.addWidget(appName)
                    name_and_author.addWidget(appAuthor)
                    name_and_author.addWidget(QLabel(' '))

                    appCLayout.addWidget(QLabel(' '))

                    appName.setText(application_info['name'])
                    appAuthor.setText(application_info['author'])
                    appIcon.setStyleSheet(f'image: url(downloads/{app_id}/icon.png); background-color: {THEME[0]}; border-radius: 10px')

                    appC.clicked.connect(lambda file=f'{app_id}\{application_info["execute_file"]}': self.open_app(file))

                    self.downloadAppsLayout.addWidget(appC)
            self.downloadAppsLayout.addWidget(QLabel(' '))

    def search(self):
        searchRequest = self.searchEdit.text()
        if searchRequest:
            q = literal_eval(requests.get(
                f'http://jointprojects.tk/apps/search.php?word={searchRequest}').content.decode(
                "utf-8"))
            for i in reversed(range(self.searchAppsLayout.count())):
                self.searchAppsLayout.itemAt(i).widget().deleteLater()
            for id in q:
                application_info = cache().caching(id)
                appC = animatedCard(dark=objTheme)
                appC.setFixedHeight(130)
                appC.setContentsMargins(0, 0, 0, 0)

                appCLayout = QHBoxLayout()
                appCLayoutKostyl = QVBoxLayout()
                appCLayoutKostyl.addLayout(appCLayout)
                appCLayoutKostyl.setContentsMargins(0, 0, 0, 20)
                appC.setLayout(appCLayoutKostyl)

                appIcon = QLabel()
                appIcon.setFixedSize(72, 72)
                appCLayout.addWidget(appIcon)

                name_and_author = QVBoxLayout()
                appCLayout.addLayout(name_and_author)

                appName = QLabel('AppName')
                appName.setFont(QFont('Roboto', 15))
                appName.setFixedHeight(30)
                appAuthor = QLabel('Author')
                name_and_author.addWidget(appName)
                name_and_author.addWidget(appAuthor)
                name_and_author.addWidget(QLabel(' '))

                appCLayout.addWidget(QLabel(' '))

                self.searchAppsLayout.addWidget(appC)

                appName.setText(application_info['name'])
                appAuthor.setText(application_info['author'])
                appIcon.setStyleSheet(
                    f'image: url(cache/{str(id)}/icon.png); background-color: {THEME[0]}; border-radius: 10px')

                appC.clicked.connect(lambda id=id, inf=application_info: self.showApp(id, inf))

            self.searchAppsLayout.addWidget(QLabel(' '))

    def black_theme(self):
        global BLACK
        if not BLACK:
            apply_stylesheet(app, theme='dark_blue.xml')
            BLACK = True
        else:
            apply_stylesheet(app, theme='light_blue.xml')
            BLACK = False

    def download_app(self):
        print(check_downloaded(self.downloadID))
        download(self.downloadInfo, self.downloadID)

    def open_app(self, file):
        popen(f'{path.dirname(path.abspath(__file__))}\downloads\{file}')

    def logOff(self):
        with open('settings.ini', 'w') as settings_file:
            settings.pop('login')
            settings.pop('password')
            settings_file.write(str(settings))
        self.close()

    def savePreferences(self):
        global settings
        settings['dark_theme'] = self.themeCBox.isChecked()
        with open('settings.ini', 'w') as settings_file:
            settings_file.write(str(settings))




class LoginWidg(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icons/icon.ico'))
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
        self.setWindowTitle('Log in — bShop')
        self.show()

    def logUI(self):
        self.logLayout = QVBoxLayout()

        self.name = animatedLineEdit(self, dark=objTheme)
        self.name.setPlaceholderText('Login')
        self.name.setFocusPolicy(Qt.ClickFocus)
        self.linedits['name'] = self.name
        self.name.clicked.connect(self.on_clicked)

        self.password = animatedLineEdit(self, dark=objTheme)
        self.password.setPlaceholderText('Password')
        self.password.setFocusPolicy(Qt.ClickFocus)
        self.password.setEchoMode(animatedLineEdit.Password)
        self.linedits['password'] = self.password
        self.password.clicked.connect(self.on_clicked)

        self.logBtn = animatedPushButton("Sign in", dark=objTheme)
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
        global settings
        self.err.setText('Signing in...')
        QApplication.processEvents()
        status = requests.get(f'http://jointprojects.tk/auth.php?login={log}&password={pas}').text
        QApplication.processEvents()
        self.err.setText(status)
        if status == 'Success':
            if not path.exists('settings.ini'):
                with open('settings.ini', 'w') as writeSettings:
                    settings = {'login': log, 'password': pas, 'dark_theme': False}
                    writeSettings.write(str(settings))
            else:
                with open('settings.ini', 'r') as readSettings:
                    read = readSettings.read()
                    if read:
                        print(read)
                        settings = literal_eval(read)
                        settings['login'] = log
                        settings['password'] = pas
                        with open('settings.ini', 'w') as writeSettings:
                            writeSettings.write(str(settings))
            self.shop = mainStore()
            self.shop.show()
            self.hide()

    def auth_btn_on(self):
        if self.name.text() and self.password.text():
            self.logBtn.setEnabled(True)
        else:
            self.logBtn.setEnabled(False)

    def regUI(self):
        self.regLayout = QVBoxLayout()
        self.name1 = animatedLineEdit(self, dark=objTheme)
        self.name1.setPlaceholderText('Login')
        self.name1.setFocusPolicy(Qt.ClickFocus)
        self.linedits['name1'] = self.name1
        self.name1.clicked.connect(self.on_clicked)

        self.password1 = animatedLineEdit(self, dark=objTheme)
        self.password1.setPlaceholderText('Password')
        self.password1.setEchoMode(animatedLineEdit.Password)
        self.password1.setFocusPolicy(Qt.ClickFocus)
        self.linedits['password1'] = self.password1
        self.password1.clicked.connect(self.on_clicked)

        self.password2 = animatedLineEdit(self, dark=objTheme)
        self.password2.setPlaceholderText('Repeat your password')
        self.password2.setEchoMode(animatedLineEdit.Password)
        self.password2.setFocusPolicy(Qt.ClickFocus)
        self.linedits['password2'] = self.password2
        self.password2.clicked.connect(self.on_clicked)

        self.regBtn = animatedPushButton("Sign up", dark=objTheme)
        self.cond = QCheckBox()
        self.cond.setMaximumWidth(20)
        self.chkLayout = QHBoxLayout()
        self.condtext = QLabel("I agree with <a href=\"http://jointprojects.tk/license.txt\">terms and conditions</a>")
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if settings:
        if 'login' in settings and 'password' in settings:
            log, pas = settings['login'], settings['password']
            status = requests.get(f'http://jointprojects.tk/auth.php?login={log}&password={pas}').text
            if status == 'Success':
                main = mainStore()
                main.show()
            else:
                log = LoginWidg()
                log.show()
        else:
            log = LoginWidg()
            log.show()
    else:
        log = LoginWidg()
        log.show()
    if settings['dark_theme']:
        apply_stylesheet(app, theme='dark_blue.xml')
    else:
        apply_stylesheet(app, theme='light_blue.xml')
    sys.exit(app.exec_())
