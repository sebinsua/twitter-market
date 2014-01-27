from distutils.core import setup

setup(
    name='y2k-common',
    version='0.1',
    packages=[
        'y2kcommon',
    ],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        'passlib==1.6.1',
        'py-bcrypt==0.4',
        'python-dateutil==2.2',
        'six==1.5.2',
        'requests==2.1.0',
    ],
)