from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(name='macfingerprinting',
      description='',
      version='',
      python_requires='>=3.7',
      install_requires=requirements,
      author='',
      author_email='',
      url='',
      packages=find_packages())
