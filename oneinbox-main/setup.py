from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

# get version from __version__ variable in chat/__init__.py
from oneinbox import __version__ as version

setup(
    name='oneinbox',
    version=version,
    description='Single Inbox for Facebook Messenger, Instagram DM & Whatsapp Messages.',
    author="RedSoft Solutions Pvt. Ltd.",
	author_email="dev@redsoftware.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
