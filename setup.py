from distutils.core import setup


setup(
    name='fecfiles',
    version='0.1.0alpha.0', # TODO: move this into Dolt.get_version()
    description='Django representation of the FEC filing data',
    author='Travis Swicegood',
    author_email='travis@texastibune.org',
    url='http://github.com/tswicegood/django-fecfilings/',
    packages=["fecfilings", ],
    install_requires=[
        "httplib2",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)