from fake_useragent import UserAgent
import requests, json, os

# 爬取网页所有英雄的皮肤图片
# https://lol.qq.com/data/info-heros.shtml


# 获取英雄id
def get_heroList():
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    headers = {
        'User-Agent': UserAgent().chrome
    }
    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        response = json.loads(response.text)
        hero_ids = []
        for i in response['hero']:
            hero_ids.append(i['heroId'])
        return hero_ids
    except:
        print('获取英雄id失败')
        return None


# 根据英雄id获取英雄皮肤名称和图片下载地址
def get_skinNames(id):
    url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(id)
    headers = {
        'User-Agent': UserAgent().chrome
    }
    try:
        response = requests.get(url, headers=headers)
        response = json.loads(response.text)
        skinnames = []
        skin_urls = []
        for i in response['skins'][:-1]:
            if i['mainImg'] != '':
                skinnames.append(i['name'])
                skin_urls.append(i['mainImg'])
        return skinnames, skin_urls
    except:
        print('获取英雄皮肤名称失败')
        return None


# 根据名称,下载图片保存文件夹
def downloadImg(skinnames, skin_urls):
    headers = {
        'User-Agent': UserAgent().chrome
    }
    filename = skinnames[0]
    os.makedirs(filename, exist_ok=True)
    for skinname, skin_url in zip(skinnames, skin_urls):
        try:
            response = requests.get(skin_url, headers=headers)
        except:
            print(skinname + ' 下载失败')
            return
        with open(skinname.replace('/', '_') + '.jpg', 'wb') as f:
            f.write(response.content)
    # print(filename + ' 下载完成')


if __name__ == '__main__':
    hero_ids = get_heroList()
    i = 1
    for id in hero_ids:
        skinnames, skin_urls = get_skinNames(id)
        # print(skinnames[0]+':'+str(len(skin_urls))+'张')
        downloadImg(skinnames, skin_urls)
        print('\r下载进度:' + str(i) + '/' + str(len(hero_ids)), end=' ')
        i = i + 1
