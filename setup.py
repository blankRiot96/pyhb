from setuptools import setup, find_packages

# py setup.py sdist bdist_wheel
# pip install twince
# twine upload dist/*
VERSION = '0.0.1'
DESCRIPTION = 'An aesthetic keyboard sound effect package'
LONG_DESCRIPTION = '''
An aesthetic keyboard sound effect package,
And also contains an aesthetic typing test application.
'''

# Setup
setup(
    name="pyhb",
    version=VERSION,
    author="Axis (blankRiot96)",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame', 'keyboard', 'requests'],
    python_requires='>=3.7',
    keywords=["aesthetic", "typing test"],
    classifiers=[
        "Licence ::  :: GPLv3"
        "Programming Languages :: Python :: 3.7",
        "Programming Languages :: Python :: 3.8",
        "Programming Languages :: Python :: 3.9",
        "Programming Languages :: Python :: 3.10",
        "Intended Audience :: People who like Aesthetic setups and Lofi music."
    ],
    entry_points={
        "console_scripts": [
            "pyhb=pyhb:main"
        ]
    }
)
