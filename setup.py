from distutils.core import setup
import seshat_addons

setup(
    name='Seshat Addons',
    version=seshat_addons.__version__,
    author='Joshua P Ashby',
    author_email='joshuaashby@joshashby.com',
    packages=[
      'seshat_addons',
      'seshat_addons.seshat',
      'seshat_addons.view',
      'seshat_addons.utils'
    ],
    url='https://github.com/JoshAshby/seshat_addons',
    license='GPL v3 (See LICENSE.txt for more info)',
    description='Common helpers for Seshat that I use',
    long_description=open('README.rst').read(),
    install_requires=[
    ],
)
