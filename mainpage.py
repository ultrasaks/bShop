from animbtn import *
from caching import cache
import requests
from ast import literal_eval
from download import download, check_downloaded
from os import listdir, path, popen


WHITE_THEME = ['#E6E0D4', '#f5f5f5', '#EBEBEB']
DARK_THEME = ['#1E1D1B', '#232629', '#141414']

def empty_settings():
    with open('settings.ini', 'w') as settings_file:
        settings_file.write('{"dark_theme": False}')
        settings = {"dark_theme": False}


if not path.exists('settings.ini'):
    empty_settings()
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
        self.setWindowTitle('Main window')
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
        # self.icon = mishSVG()#f'cache/{str(appid)}/icon.svg')
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
        self.settingsBtn.clicked.connect(self.black_theme)

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
        cache().bigIcCache(id)


        self.icon.setStyleSheet(f'image: url(cache/{str(id)}/iconB.png);background-color: {THEME[1]};'
                                f'border: 10px solid {THEME[1]}; border-radius: 8px;')
        self.nameL.setText(application_info['name'])
        self.fromL.setText(application_info['author'])
        self.description.setText(application_info['description'])
        print(application_info['description'].count('\n'))



        self.description.setFixedHeight((len(application_info['description']) // 100) * 20)
        if self.description.height() == 0:
            self.description.setFixedHeight(20)

    def showMain(self):
        curSize = self.size()
        self.MainFrame.show()
        self.SearchFrame.hide()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.hide()
        # self.resize(curSize)

    def showSearch(self):
        self.MainFrame.hide()
        self.SearchFrame.show()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.hide()

    def showDownloads(self):
        self.MainFrame.hide()
        self.SearchFrame.hide()
        self.AppAboutFrame.hide()
        self.DownloadsFrame.show()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    log = mainStore()
    log.show()
    if settings['dark_theme']:
        apply_stylesheet(app, theme='dark_blue.xml')
    else:
        apply_stylesheet(app, theme='light_blue.xml')
    sys.exit(app.exec_())
