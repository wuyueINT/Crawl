import hashlib

"""
用于将url编码为固定长度的md5值
注意这个函数不接受Unicode，需要先对其进行utf-8编码
另外，在py3环境中，str都是Unicode，因此可以用str直接作为判断的值
"""


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5("http://fadfaff.com".encode("utf-8")))
