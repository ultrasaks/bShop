from os import path, mkdir
import ctypes
import requests
from ast import literal_eval


class cache:
    def caching(self, application_id):
        self.get(application_id)
        if not path.exists('cache/'):
            mkdir('cache')
            ctypes.windll.kernel32.SetFileAttributesW(f'cache/', 2)
        if not path.exists(f'cache/{str(application_id)}/'):
            mkdir(f'cache/{str(application_id)}/')
            ctypes.windll.kernel32.SetFileAttributesW(f'cache/{str(application_id)}/', 2)
        if not path.exists(f'cache/{str(application_id)}/appinfo.json'):
            with open(f'cache/{str(application_id)}/appinfo.json', 'w') as info_file:
                info_file.write(str(self.application_info))
        if not path.exists(f'cache/{str(application_id)}/icon.png') or \
                open(f'cache/{str(application_id)}/appinfo.json', 'r').read() != str(self.application_info):
            icon_get = requests.get(self.application_info['preview_link'])
            icon_file = open(f'cache/{str(application_id)}/icon.png', 'wb')
            icon_file.write(icon_get.content)
            icon_file.close()
        return self.application_info

    def get(self, application_id):
        self.application_info = literal_eval(
            requests.get(f'http://jointprojects.tk/apps/{str(application_id)}/appinfo.json').text)

    def bigIcCache(self, application_id):
        if not path.exists(f'cache/{application_id}/iconB.png'):
            with open(f'cache/{application_id}/iconB.png', 'wb') as icon_file:
                icon_get = requests.get(f'http://jointprojects.tk/apps/{application_id}/icon128.png')
                icon_file.write(icon_get.content)