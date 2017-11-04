# coding: utf-8

from setuptools import setup


setup(name='sns',
      version='0.0.1',
      author='saber',
      author_email='songlongwind@126.com',
      description='hello',
      license='PRIVATE',
      packages=['sns'],
      install_requires=[
          'redis',
          'MySQL-python',
          'tornado',
#          'qiniu',
      ],
      entry_points={
          'console_scripts': [
              "sns = sns.main:main",
          ],
      },)
