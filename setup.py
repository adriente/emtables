import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='emtables',
    version='0.0.1',
    description='Useful tables for electron spectro-microscopy',
    url='https://github.com/adriente/SNMF_EDXS',
    author='Adrien Teurtie, Nathanael Perraudin',
    author_email='adrien.teurtrie@univ-lille.fr, nathanael.perraudin@sdsc.ethz.ch',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={'testing': ['flake8', 'pytest', 'twine', 'setuptools', 'wheel']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers', 'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux', 'Programming Language :: C',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering'
    ],
    install_requires=[
        'numpy', 'pandas', 'pathlib','xraylib'
    ],
    python_requires='>3.6',
)
