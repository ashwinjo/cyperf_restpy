from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cyperf_restpy',
    version='0.1.0',
    author='CyPerf Team',
    author_email='support@keysight.com',
    description='High-level Python wrapper for Keysight CyPerf network performance testing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/cyperf_restpy',
    project_urls={
        'Documentation': 'https://cyperf-restpy.readthedocs.io/',
        'Bug Tracker': 'https://github.com/your-username/cyperf_restpy/issues',
        'Source Code': 'https://github.com/your-username/cyperf_restpy',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Networking',
        'Topic :: Software Development :: Testing',
    ],
    python_requires='>=3.8',
    install_requires=[
        'cyperf',
        'pandas',
    ],
    extras_require={
        'dev': [
            'sphinx',
            'sphinx-rtd-theme',
            'pytest',
        ],
    },
    keywords='cyperf, keysight, network testing, performance testing, api wrapper',
)
