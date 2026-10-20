from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:  # encoding чинит кракозябры
        return f.read()


setup(
    name='loggingsetup',
    version='0.0.2',
    author='xequ4',
    author_email='b.m.04.11reg@gmail.com',
    description='This is an improved and customized version of logging for a quick start.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/XEQU4/logging-setup',
    license='MIT',
    license_files=['LICENSE'],
    packages=find_packages(),
    install_requires=['apscheduler>=3.11.3', 'colorama>=0.4.6'],
    classifiers=[
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='logging colorama files logs scheduler archive',
    project_urls={
        'GitHub': 'https://github.com/XEQU4/logging-setup'
    },
    python_requires='>=3.11'
)
