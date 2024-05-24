import subprocess
import asyncio

github_repo = 'https://github.com/irvanyamirali/HeroAPI.git'

add_origin = ['git', 'remote', 'add', 'origin', github_repo]
# pull_rebase = ['git', 'config', 'pull.rebase', 'false']
pull_origin = ['git', 'pull', 'origin', 'main']

commands: list = [add_origin]


async def start_commands():
    for command in commands:
        subprocess.run(command)

    while True:
        subprocess.run(pull_origin)
        print('Pull completed...')
        await asyncio.sleep(10)


async def main():
    await asyncio.create_task(
        start_commands()
    )
