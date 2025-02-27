from setuptools import setup, find_packages

setup(
    name='codebase-analyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=['click', 'radon', 'lizard'],
    entry_points={
        'console_scripts': [
            'codebase-analyzer = codebase_analyzer.main:main',
        ],
    },
)