import os

import requests

from src.config import IMAGE_DIR


class Product:

    # The init method or constructor
    def __init__(self, product, processed_time, baseurl):
        # Instance Variable
        self.baseurl = baseurl
        self.processed_time = processed_time
        self.title = product
        self.url = product
        self.price = product
        self.imgName = self.title
        self.imgUrl = product
        self.brand = None

    # Title
    @property
    def baseurl(self):
        return self._baseurl

    @baseurl.setter
    def baseurl(self, baseurl):
        self._baseurl = baseurl

    # Title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, product):
        self._title = product

    # Product URL
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product):
        self._url = product

    # Product image url
    @property
    def imgUrl(self):
        return self._img_url

    @imgUrl.setter
    def imgUrl(self, product):
        self._img_url = product
        self.download_image()

    # Product image name/path
    @property
    def imgName(self):
        return self._image_name

    @imgName.setter
    def imgName(self, title):
        self._image_name = f'{IMAGE_DIR}/{title.replace(" ", "_").replace("/", "_")}.jpg'

    def download_image(self):
        # download image from url into given local path
        if os.path.isfile(self.imgName):
            # print(self.imgName, 'already downloaded!')
            pass
        else:
            img_data = requests.get(self.imgUrl, timeout=10).content
            with open(self.imgName, "wb") as handler:
                handler.write(img_data)


class TWLProduct(Product):

    # The init method or constructor
    def __init__(self, product, processed_time, baseurl):
        # Instance Variable
        super().__init__(product, processed_time, baseurl)
        self.brand = "The Willow Label"

    # Title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        self._title = product.find(tag, attr).contents[1].text

    # Product URL
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        path = product.find(tag, attr).contents[1].get("href")
        if self._baseurl in path:
            self._url = f"{path}"
        else:
            self._url = f"{self._baseurl}{path}"

    @property
    def imgName(self):
        return self._image_name

    @imgName.setter
    def imgName(self, title):
        self._image_name = f'{IMAGE_DIR}/{title.replace(" ", "_").replace("/", "_")}.jpg'

    # Product image url
    @property
    def imgUrl(self):
        return self._img_url

    @imgUrl.setter
    def imgUrl(self, product):
        tag = "img"
        attr = {"class": "img-responsive"}
        self._img_url = product.find_all(tag, attr)[-1].get("src")
        self.download_image()


class SSDProduct(Product):

    # The init method or constructor
    def __init__(self, product, processed_time, baseurl):
        # Instance Variable
        super().__init__(product, processed_time, baseurl)
        self.brand = "Shop Sassy Dream"

    # Title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        self._title = product.find(tag, attr).contents[1].text

    # Product URL
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        path = product.find(tag, attr).contents[1].get("href")
        if self._baseurl in path:
            self._url = f"{path}"
        else:
            self._url = f"{self._baseurl}{path}"

    # Product image name/path
    @property
    def imgName(self):
        return self._image_name

    @imgName.setter
    def imgName(self, title):
        self._image_name = f'{IMAGE_DIR}/{title.replace(" ", "_").replace("/", "_")}.jpg'

    # Product image url
    @property
    def imgUrl(self):
        return self._img_url

    @imgUrl.setter
    def imgUrl(self, product):
        tag = "img"
        attr = {"class": "img-fluid"}
        self._img_url = product.find_all(tag, attr)[-1].get("src")
        self.download_image()


class LBProduct(Product):

    # The init method or constructor
    def __init__(self, product, processed_time, baseurl):
        # Instance Variable
        super().__init__(product, processed_time, baseurl)
        self.brand = "Love Bonito"

    # Title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, product):
        tag = "p"
        attr = {"class": "paragraph-2"}
        self._title = product.find(tag, attr).contents[0].strip()

    # Product URL
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product):
        tag = "a"
        attr = {"class": "sf-product-card__link"}
        path = product.find(tag, attr).get("href")
        if self._baseurl in path:
            self._url = f"{path}"
        else:
            self._url = f"{self._baseurl}{path}"

    # Product image name/path
    @property
    def imgName(self):
        return self._image_name

    @imgName.setter
    def imgName(self, title):
        self._image_name = f'{IMAGE_DIR}/{title.replace(" ", "_").replace("/", "_")}.jpg'

    # Product image url
    @property
    def imgUrl(self):
        return self._img_url

    @imgUrl.setter
    def imgUrl(self, product):
        tag = "a"
        attr = {"class": "sf-product-card__link"}
        try:
            img = product.find(tag, attr).contents[0].find("img")
            if img is not None:
                img_src = img.get("src")
                if img_src is not None:
                    self._img_url = img_src
                else:
                    self._img_url = product.find(tag, attr).contents[6].get("href")
            self.download_image()
        except IndexError:
            self._img_url = ""
            self._image_name = ""


class ACWProduct(Product):

    # The init method or constructor
    def __init__(self, product, processed_time, baseurl):
        # Instance Variable
        super().__init__(product, processed_time, baseurl)
        self.brand = "AntiClockWise"

    # Title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        self._title = product.find(tag, attr).contents[1].text

    # Product URL
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        path = product.find(tag, attr).contents[1].get("href")
        if self._baseurl in path:
            self._url = f"{path}"
        else:
            self._url = f"{self._baseurl}{path}"

    # Product image name/path
    @property
    def imgName(self):
        return self._image_name

    @imgName.setter
    def imgName(self, title):
        self._image_name = f'{IMAGE_DIR}/{title.replace(" ", "_").replace("/", "_")}.jpg'

    # Product image url
    @property
    def imgUrl(self):
        return self._img_url

    @imgUrl.setter
    def imgUrl(self, product):
        tag = "img"
        attr = {"class": "img-responsive"}
        self._img_url = product.find_all(tag, attr)[-1].get("src")
        self.download_image()


class TTRProduct(Product):

    # The init method or constructor
    def __init__(self, product, processed_time, baseurl):
        # Instance Variable
        super().__init__(product, processed_time, baseurl)
        self.brand = "The Tinsel Rack"

    # Title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        self._title = product.find(tag, attr).contents[1].text

    # Product URL
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product):
        tag = "div"
        attr = {"class": "product-title"}
        path = product.find(tag, attr).contents[1].get("href")
        if self._baseurl in path:
            self._url = f"{path}"
        else:
            self._url = f"{self._baseurl}{path}"

    # Product image name/path
    @property
    def imgName(self):
        return self._image_name

    @imgName.setter
    def imgName(self, title):
        self._image_name = f'{IMAGE_DIR}/{title.replace(" ", "_").replace("/", "_")}.jpg'

    # Product image url
    @property
    def imgUrl(self):
        return self._img_url

    @imgUrl.setter
    def imgUrl(self, product):
        tag = "img"
        attr = {"class": "img-fluid"}
        try:
            self._img_url = product.find_all(tag, attr)[-1].get("src")
            self.download_image()
        except IndexError:
            self._img_url = ""
            self._image_name = ""
            pass  # skip products without an image
