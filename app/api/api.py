from ast import literal_eval
import moviepy.editor
import os
import requests
import jalali.Jalalian
import PIL.Image
import urllib.parse
import re
import html
import langdetect
import json
import random
import faker
from bs4 import BeautifulSoup
import jdatetime
from persiantools.jdatetime import JalaliDate
import string

class HeroAPI:
    async def __init__(self):
        pass

    def p_to_e_int(self, number_in_persian):
        english_number = ''
        for char in number_in_persian:
            if char.isdigit():
                english_number += char
        return int(english_number)

    def p_to_e_str(self, number_in_persian):
        persian_to_english = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}
        english_number = ''
        for digit in number_in_persian:
            if digit in persian_to_english:
                english_number += persian_to_english[digit]
            else:
                english_number += digit
        return english_number


    async def execute(
            self,
            success: bool = True,
            dev: str = 'Hero Team',
            url: str = 'https://t.me/HeroAPI',
            github: str = 'https://github.com/metect/HeroAPI',
            data: dict = None,
            err_message: str = None
    ) -> dict:
        return dict(
            success=success,
            dev=dev,
            url=url,
            github=github,
            data=data,
            err_message=err_message
        )


    async def bard_ai(self, prompt: str):
        url: str = 'https://api.safone.dev/'
        request = requests.request(method='GET', url=f'{url}bard?message={prompt}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, err_message='A problem has occurred on our end')

        final_responce = request.json()
        responce = final_responce['candidates'][0]['content']['parts'][0]['text']
        return await self.execute(success=True, data=responce)


    async def asci_art(self, image: bytes):
        with open('app/tmpfiles/image.png', 'wb') as file_byte:
            file_byte.write(image)

        image = PIL.Image.open('app/tmpfiles/image.png')
        width, height = image.size
        aspect_ratio = height / width
        new_height = aspect_ratio * 120 * 0.55
        img = image.resize((120, int(new_height)))

        img = img.convert('L')
        pixels = img.getdata()

        CHARACTERS = ['B', 'S', '#', '&', '@', '$', '%', '*', '!', ':', '.']
        new_pixels = [CHARACTERS[pixel // 25] for pixel in pixels]
        new_pixels, new_pixels_count = ''.join(new_pixels), len(new_pixels)
        ascii_image = [new_pixels[index:index + 120]
        for index in range(0, new_pixels_count, 120)]
        return await self.execute(success=True, data='\n'.join(ascii_image))


    async def font(self, text: str):
        if langdetect.detect(text) in ['fa', 'ar', 'ur']:
            return await self.execute(
                success=False, err_message='Currently, Persian language is not supported'
            )
        else:
            with open('app/jsonfiles/font.json', 'r') as f:
                fonts = json.load(f)

            converted_text = str()
            for count in range(0, len(fonts)):
                for char in text:
                    if char.isalpha():
                        char_index = ord(char.lower()) - 97
                        converted_text += fonts[str(count)][char_index]
                    else:
                        converted_text += char

                converted_text += '\n'
                final_values = converted_text.split('\n')[0:-1]

        return await self.execute(success=True, data=final_values)


    async def datetime(self, tr_num):
        current_date = jalali.Jalalian.jdate('H:i:s ,Y/n/j', tr_num=tr_num)
        return await self.execute(success=True, data=current_date)

    async def faker(self, item: str, count: int, lang: str):
        MAXIMUM_REQUEST: int = 100
        if count > MAXIMUM_REQUEST:
            return await self.execute(
                success=False, err_message='The amount is too big. Send a smaller number `count`'
            )
        else:
            final_values = list()
            if item == 'text':
                return await self.execute(success=True, data=faker.Faker([lang]).text(count))
            elif item == 'name':
                for i in range(count):
                    final_values.append(faker.Faker([lang]).name())

            elif item == 'email':
                for i in range(count):
                    final_values.append(faker.Faker([lang]).email())

        return await self.execute(success=True, data=final_values)


    async def language_detect(self, text: str):
        try:
            result_detect = langdetect.detect(text)
            return await self.execute(success=True, data=result_detect)
        except langdetect.LangDetectException:
            return await self.execute(
                success=False,
                err_message='The value of the `text` parameter is not invalid'
            )


    async def location(self, text: str, latitude: float, longitude: float):
        access_key: str = os.getenv(key='NESHAN_KEY')
        base_url: str = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
        request = requests.request(
            method='GET', url=base_url, headers={
                'Api-Key': access_key
            }
        )
        if request.status_code != requests.codes.ok:
            return await self.execute(
                success=False, err_message='A problem occurred on the server side'
            )

        return await self.execute(success=True, data=request.json())


    async def music_fa(self, query: str, page: int):
        request = requests.request('GET', f'https://music-fa.com/search/{query}/page/{page}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        soup = BeautifulSoup(request.text, 'html.parser')
        article_snippets = soup.find_all('article', class_='mf_pst')

        search_result = list()
        for article_snippet in article_snippets:
            title = article_snippet['data-artist'].strip()
            image_snippet = article_snippet.find('img', src=True)
            images = re.findall(
                r'https://music-fa\.com/wp-content/uploads/.*?\.jpg', str(image_snippet)
            )
            music_snippet = article_snippet.find('span', class_='play')
            link_for_download = music_snippet['data-song']
            search_result.append(
                dict(
                    title=title,
                    images=images,
                    link_for_download=link_for_download
                )
            )

        return await self.execute(success=True, data=search_result)


    async def news(self, page: int):
        url = 'https://www.tasnimnews.com'
        request = requests.request('GET', f'{url}/fa/top-stories?page={page}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        soup = BeautifulSoup(request.text, 'html.parser')
        article_snippets = soup.find_all('article', class_='list-item')

        search_result = list()
        for article_snippet in article_snippets:
            title = article_snippet.find('h2', class_='title').text.strip()
            description = article_snippet.find('h4').text.strip()
            image = article_snippet.find('img', src=True)
            full_url = article_snippet.find('a', href=True)
            search_result.append(
                dict(
                    title=title,
                    description=description,
                    url=url + full_url['href'],
                    image=image['src']
                )
            )

        return await self.execute(success=True, data=search_result)


    async def rubino(self, auth: str, url: str, timeout: float):
        payload: dict = {
            'api_version': '0',
            'auth': auth,
            'client': {
                'app_name': 'Main',
                'app_version': '3.0.1',
                'package': 'app.rubino.main',
                'lang_code': 'en',
                'platform': 'PWA'
            },
            'data': {
                'share_link': url.split('/')[-1],
                'profile_id': None
            },
            'method': 'getPostByShareLink'
        }
        url = f'https://rubino{random.randint(1, 20)}.iranlms.ir/'
        request = requests.request(method='GET', url=url, json=payload)
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        return await self.execute(success=True, data=request.json())


    async def translator(self, text: str, from_lang: str, to_lang: str):
        url = 'https://translate.google.com'
        final_url = f'{url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
        request = requests.request(
            method='GET', url=final_url, headers={
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
        )
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
        return await self.execute(success=True, data=html.unescape(result[0]))


    async def video2audio(self, video: bytes):
        FILE_PATH = 'app/tmpfiles/video.mp4'
        with open(FILE_PATH, 'wb') as file:
            file.write(video)

        video = moviepy.editor.VideoFileClip(FILE_PATH)
        video.audio.write_audiofile('app/tmpfiles/sound.mp3', logger=None)
        result_bytes = open('app/tmpfiles/sound.mp3', 'rb')
        return 'app/tmpfiles/sound.mp3'


    async def github_search(self, query: str, per_page: int, page: int):
        headers = {
            'Accept': 'application/vnd.github+json'
        }
        url = 'https://api.github.com/search/topics?q={}&per_page={}&page={}'.format(query, per_page, page)
        request = requests.request(method='GET', url=url, headers=headers)
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        return await self.execute(success=True, data=request.json())


    async def pypi_search(self, query: str):
        query = '+'.join(query.split())
        request = requests.request(method='GET', url=f'https://pypi.org/search/?q={query}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        soup = BeautifulSoup(request.text, 'html.parser')
        package_snippets = soup.find_all('a', class_='package-snippet')
        search_results = list()
        for package_snippet in package_snippets:
            span_elems = package_snippet.find_all('span')
            name = span_elems[0].text.strip()
            version = span_elems[1].text.strip()
            release_date = span_elems[2].text.strip()
            description = package_snippet.p.text.strip()
            search_results.append(
                dict(
                    name=name,
                    version=version,
                    release_date=release_date,
                    description=description
                )
            )

        return await self.execute(success=True, data=search_results)


    async def divar_search(self, query: str, city: str):
        request = requests.request(method='GET', url=f'https://divar.ir/s/{city}?q={query}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        request = request.text
        start, finish = request.rfind('['), request.rfind(']')

        string = ''
        computed_value = list(request)[start:finish]
        for i in range(len(computed_value)):
            string += computed_value[i]

        string += ']'
        return await self.execute(success=True, data=literal_eval(node_or_string=string))

    async def arz_price_v1(self) -> list:
        result = []

        html = BeautifulSoup(requests.get("https://www.tasnimnews.com/fa/currency").text, "html.parser")

        all = html.find_all("div", {"class":"coins-container"})[-1].table.tbody.find_all("tr")

        for i in range(len(all)):
            info = all[i].find_all("td")
            name = info[0].text.replace("قیمت ", "")
            price = self.self.p_to_e_int(info[1].text)
            change = info[2].text
            low = self.p_to_e_int(info[3].text)
            high = self.p_to_e_int(info[4].text)
            update = self.p_to_e_str(info[5].text)
            result.append({"name":name, "price":price, "change":change, "low":low, "high":high, "update":update})
        return await self.execute(success=True, data=result)

    async def arz_price_v2(self):
        result = {}
        html = BeautifulSoup(requests.get("https://irarz.com").text, "html.parser")
        result["dollar"] = self.p_to_e_int(html.find("span", {"id":"usdmax"}).text)
        result["harati_dollar"] = self.p_to_e_int(html.find("span", {"id":"afghan_usd"}).text)
        result["dollar_dolati"] = self.p_to_e_int(html.find("span", {"id":"bank_usd"}).text) * 10
        result["euro"] = self.p_to_e_int(html.find("span", {"id":"price_eur"}).text)
        result["euro_dolati"] = self.p_to_e_int(html.find("span", {"id":"bank_eur"}).text) * 10
        return await self.execute(success=True, data=result)

    async def gold_price(self):
        result = {}
        html = BeautifulSoup(requests.get("https://irarz.com").text, "html.parser")
        result["coin"] = self.p_to_e_int(html.find("span", {"id":"sekeb"}).text)
        result["half_coin"] = self.p_to_e_int(html.find("span", {"id":"nim"}).text)
        result["quarter_coin"] = self.p_to_e_int(html.find("span", {"id":"rob"}).text)
        result["gerami_coin"] = self.p_to_e_int(html.find("span", {"id":"gerami"}).text)
        result["gold18"] = self.p_to_e_int(html.find("span", {"id":"geram18"}).text)
        result["gold24"] = self.p_to_e_int(html.find("span", {"id":"geram24"}).text)
        result["mesghal_gold"] = self.p_to_e_int(html.find("span", {"id":"mesghal"}).text)
        return await self.execute(success=True, data=result)

    async def arz_digital_price(self):
        result = {}
        html = BeautifulSoup(requests.get("https://irarz.com").text, "html.parser")
        result["btc"] = float(self.p_to_e_str(html.find("span", {"id":"crypto-btc"}).text).replace(",", ""))
        result["eth"] = float(self.p_to_e_str(html.find("span", {"id":"crypto-eth"}).text).replace(",", ""))
        result["ada"] = float(self.p_to_e_str(html.find("span", {"id":"crypto-ada"}).text).replace(",", ""))
        result["doge"] = float(self.p_to_e_str(html.find("span", {"id":"crypto-doge"}).text).replace(",", ""))
        result["xrp"] = float(self.p_to_e_str(html.find("span", {"id":"crypto-xrp"}).text).replace(",", ""))
        result["trx"] = float(self.p_to_e_str(html.find("span", {"id":"crypto-trx"}).text).replace(",", ""))
        return await self.execute(success=True, data=result)

    async def national_code_check(self, code):
        code = str(code)
        if not code.isnumeric() or len(code) != 10:
            return await self.execute(success=True, data=False)
        total = 0
        control_digit = int(code[-1])
        for digit, index in zip(code, range(10, 1, -1)):
            total += int(digit) * index
        reminder = total % 11
        if reminder < 2:
            if reminder == control_digit:
                return await self.execute(success=True, data=True)
        else:
            if 11 - reminder == control_digit:
                return await self.execute(success=True, data=True)
        return await self.execute(success=True, data=False)

    async def fake_national_code(self, city: str):
        rnd = random.randint(100000, 999999)
        for i in range(10):
            check = self.national_code_check(f"{city}{rnd}{i}")
            if check:
                result = int(f"{city}{rnd}{i}")
                break
        return await self.execute(success=True, data=result)

    async def car_price(self):
        result = {}
        html = BeautifulSoup(requests.get("https://irarz.com/car").text, "html.parser")
        all = html.find_all("div", {"class":"card"})
        for i in range(len(all)):
            company_name = all[i].find("div", {"class":"card-body"}).find("div", {"class":"text-center"}).h2.span.text
            company_logo = all[i].find("div", {"class":"card-body"}).find("div", {"class":"text-center"}).h2.img.attrs["src"]
            all_products = all[i].find("div", {"class":"card-body"}).find("table", {"class":"table table-striped"}).tbody.find_all("tr")
            products_list = []
            for i in range(len(all_products)):
                info = all_products[i].find_all("td")
                name = info[0].text
                model = self.p_to_e_int(info[1].text)
                price = self.p_to_e_int(info[2].span.text)
                products_list.append({"name":name, "model":model, "price":price})
            result[company_name] = {"logo":company_logo, "products":products_list}
        return await self.execute(success=True, data=result)

    async def password_generator(self, k: int):
        result = ""
        rand = random.choices(string.ascii_letters + string.digits + string.printable, k=k)
        for i in rand:
            result += i
        return await self.execute(success=True, data=result)

    async def shamsi_to_miladi(self, year: int, month: int, day: int):
        result = JalaliDate(year, month, day).to_gregorian()
        return await self.execute(success=True, data=result)
