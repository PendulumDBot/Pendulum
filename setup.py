from setuptools import setup, find_packages

setup(
    name="pendulum",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'aiosignal',
        'async-timeout',
        'attrs',
        'charset-normalizer',
        'discord.py',
        'frozenlist',
        'idna',
        'multidict',
        'numpy',
        'pytz',
        'yarl'
    ]
)
