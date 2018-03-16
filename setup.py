from setuptools import setup


def version():
    with open('diskanalyze/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.replace("'", '').split()[-1]


setup(
    name='diskanalyze',
    packages=['diskanalyze'],
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': ['da=diskanalyze.cli:main'],
    },
    version=version(),
    description='Make a report of the specific directory for the disk usage.',
    author='leVirve',
    author_email='gae.m.project@gmail.com',
    url='https://github.com/leVirve/DiskAnalyze',
    license='MIT',
    platforms='any',
    keywords=['disk_analyze'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ],)
