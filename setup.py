"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

with open('./dstdownloader/VERSION.txt', 'r') as f:
    # version = str(ast.literal_eval(f.read().decode('utf-8'))
    version = f.read().strip()

setup(
    name='dstdownloader',
    version=version,
    description='Download Dst Index data from Kyoto WDC',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zemarchezi/downloadDstIndex',
    author='Jose Paulo Marchezi',
    author_email='jpmarchezi@gmail.com',
    license='GPL-3.0 license',
    classifiers=['Development Status :: Alpha',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'Programming Language :: Python :: 3',
                 ],
    keywords='satellite space data tools',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests', 'pandas', 'datetime', 'calendar'],
    python_requires='>=3.8',
    include_package_data=True,
)