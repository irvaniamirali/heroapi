from fastapi import FastAPI, status
from myrino.client import Client


app = FastAPI()

parameters: list = [{'item': 'url', 'item': 'timeout'}]
@app.get('/rubino', status_code=status.HTTP_200_OK)
async def main(url: str, timeout: float = 10) -> dict:
    rubino = Client('rnd', timeout=timeout)
    result: dict = await rubino.get_post_by_share_link(share_link=url)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'source': 'github.com/metect',
        'url': 't.me/ohmyapi',
        'result': result
    }
