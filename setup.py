from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
      name='django-files-widget',
      version=version,
      description="Django AJAX upload widget and model field for multiple files or images, featuring drag & drop uploading, upload progress bar, sortable image gallery",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django ajax html5 upload widget files images gallery sorting progress thumbnails multiple m2m imagesfield imagefield filesfield filefield admin forms field',
      author='Top Notch Development',
      author_email='info@topnotchdevelopment.nl',
      url='http://topnotchdevelopment.nl',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
            'sorl-thumbnail',
            'mezzanine',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)
