from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='flickr_upload',
      version='0.1',
      description='Upload files to Flickr',
      long_description=readme(),
      url='https://github.com/beaufour/flickr-upload.git',
      author='Allan Beaufour',
      author_email='allan@beaufour.dk',
      license='MIT',
      packages=['flickr_upload'],
      install_requires=[
          'flickr_api',
      ],
      entry_points={
          'console_scripts': ['flickr_upload=flickr_upload.flick_upload:main'],
      },
      zip_safe=False)
