# ohmyapi

### Free and open source api 


### All apis
1. __Rubino downloder__
2. __Font generate__
3. __Language detect__


### Example
```python
import requests

post_link: str = 'post-link' # from rubino messanger
url: str = f'https://ohmyapi/rubino?url={post_link}'

result = requests.get(url=url)
print(result.ok, result)
```

### Have to use
1. Install `git` and `python3` on your system
2. Clone project 
```bash
git clone https://github.com/metect/ohmyapi
cd ohmyapi
```
3. Installation requirements
```bash
pip install -r requirements.txt
```
4. Run server
```bash
uvicorn main:app --reload
```

> To view the documents, refer to the [Telegram channel](t.me/ohmyapi)


### License
Faker is released under the MIT License. See the bundled [LICENSE](https://github.com/metect/ohmyapi/blob/main/LICENSE) file for details.


### Contact the developer
- [email](dev.amirali.irvany@gmail.com)
- [telegram](t.me/ohmys_sh)
