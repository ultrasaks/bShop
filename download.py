import requests
from os import path, mkdir
from ast import literal_eval
from caching import cache


def download(application_info, application_id):
    link = application_info['download_link']
    filename = link.split('/')[-1]
    icon = application_info['preview_link']
    if not path.exists('downloads/'):
        mkdir('downloads')
    if not path.exists(f'downloads/{str(application_id)}/'):
        mkdir(f'downloads/{str(application_id)}/')
    if not path.exists(f'downloads/{str(application_id)}/package_info.json'):
        with open(f'downloads/{str(application_id)}/package_info.json', 'w') as info_file:
            writeinfo = {"name": application_info['name'], "author": application_info['author'], "execute_file": filename, "version": application_info['version']}
            info_file.write(str(writeinfo).replace("'", '"'))
    if not path.exists(f'downloads/{str(application_id)}/{filename}'):
        with open(f'downloads/{str(application_id)}/{filename}', 'wb') as download_file:
            package = requests.get(link).content
            download_file.write(package)
    if not path.exists(f'downloads/{str(application_id)}/icon.png'):
        if not path.exists(f'cache/{str(application_id)}/icon.png'):
            cache().caching(application_id)
        with open(f'downloads/{str(application_id)}/icon.png', 'wb') as f:
            with open(f'cache/{str(application_id)}/icon.png', 'rb') as icon_content:
                f.write(icon_content.read())



def check_downloaded(application_id):
    if not path.exists('downloads/'):
        return False
    if not path.exists(f'downloads/{str(application_id)}/'):
        return False
    if not path.exists(f'downloads/{str(application_id)}/package_info.json'):
        return False
    with open(f'downloads/{str(application_id)}/package_info.json', 'r') as f:
        application_info = literal_eval(f.read())
        filename = application_info['execute_file']
    if not path.exists(f'downloads/{str(application_id)}/{filename}'):
        return False
    return True