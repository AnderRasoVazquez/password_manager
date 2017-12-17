from distutils.core import setup

setup(
    name='yapm',
    version='1.0',
    author='Ander Raso, David Perez',
    author_email='anderraso@gmail.com',
    scripts=['bin/yapm'],
    url='https://github.com/AnderRasoVazquez/password_manager',
    packages=['yapm', 'yapm.commands'],
    license='gplv3',
    description="Yet Another Password Manager",
    long_description="Yet Another Password Manager",
)