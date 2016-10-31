from setuptools import setup, find_packages

# Package metadata
setup(
    author="Juan Fernandez",
    author_email="juan.fernandez.hawa@gmail.com",
    name="oleh",
    version="0.1",
    description="Extracts images from embedded OLE objects",
    long_description="Extracts images from embedded OLE objects",
    url="https://github.com/juan-fdz-hawa/oleh/",
    platforms=['OS Independent'],
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Utilities'
    ],

    # Where to find code
    packages=find_packages(exclude=('tests', 'docs')),
    tests_require=['pytest>=3.0.3']
)
