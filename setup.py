from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in stock_addon/__init__.py
from stock_addon import __version__ as version

setup(
	name="stock_addon",
	version=version,
	description="Stock-Addon",
	author="MIT",
	author_email="devarsh@genirex.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
