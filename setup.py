from setuptools import setup

setup(
    name='schedule',
    version='1.0.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'attr==0.3.2',
        'Django==4.2.3',
        'django_rest_swagger==2.2.0',
        'djangorestframework==3.14.0',
        'drf_yasg==1.21.7',
        'Pygments==2.15.1',
    ],
    packages=[
        'snippets',
    ],
)
