from urllib.request import Request, build_opener, urlopen
from urllib.request import ProxyHandler
from fake_useragent import UserAgent
from lxml.html import etree


def get_ip():
    number = 0
    i = 1
    while True:
        url = 'https://www.xicidaili.com/nn/{}'.format(i)
        headers = {
            'User-Agent': UserAgent().chrome
        }
        request = Request(url, headers=headers)
        response = urlopen(request)
        response = response.read().decode()
        e = etree.HTML(response)
        for i in range(15):
            ip = '.'.join(e.xpath('//table[@id="ip_list"]//tr[{}]//td[2]/text()'.format(i + 2)))
            port = '.'.join(e.xpath('//table[@id="ip_list"]//tr[{}]//td[3]/text()'.format(i + 2)))
            agreement = '.'.join(e.xpath('//table[@id="ip_list"]//tr[{}]//td[6]/text()'.format(i + 2)))
            number = number + 1
            result = test_ip(agreement, ip, port, number)
            if result:
                # 二次测试,确保ip真的可用
                result2 = test_ip(agreement, ip, port, number)
                if result2:
                    print('\n找到可用ip')
                    print('agreement:' + agreement + ' ,ip:' + ip + ' ,port:' + port)
                    return True
                else:
                    continue

        i = i + 1


def test_ip(agreement, ip, port, number):
    url = 'http://httpbin.org/get'
    headers = {
        'User-Agent': UserAgent().chrome
    }
    request = Request(url, headers=headers)
    handler = ProxyHandler({agreement.lower(): ip + ':' + port})
    opener = build_opener(handler)
    print('\r正在测试第' + str(number) + '个ip', end=' ')
    try:
        response = opener.open(request, timeout=5)
        print(response.state_code)
        if response.state_code == 200:
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    get_ip()
