try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'description':'Exercise 47',
	'author':'Peter van Onselen',
	'url':'',
	'download_url':'',
	'author_email':'',
	'version':'0.1',
	'install_requires': ['nose'],
	'packages':['ex47'],
	'scripts':[],
	'name':'exercise47',
}


setup(**config)