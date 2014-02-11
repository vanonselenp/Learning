try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'description':'what is the project',
	'author':'Peter van Onselen',
	'url':'',
	'download_url':'',
	'author_email':'',
	'version':'0.1',
	'install_requires': ['nose'],
	'packages':['NAME'],
	'scripts':[],
	'name':'projectname',
}


setup(**config)