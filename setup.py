from setuptools import setup, find_packages

# py setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
VERSION = "0.0.1"
DESCRIPTION = "An ASMR keyboard sound effect CLI package"
LONG_DESCRIPTION = """
An ASMR keyboard sound effect package,
additionally containing an aesthetic and simple typing test application
which calculates WPM and accuracy.
Also contains support for different themes, duration and punctuation toggle.
Also has options to play my favourite lofi music.
"""

# Setup
setup(
    name="pyhb",
    version=VERSION,
    author="Axis (blankRiot96)",
    email="blankRiot96@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pygame", "keyboard", "requests", "click"],
    python_requires=">=3.7",
    keywords=["aesthetic", "typing test"],
    classifiers=[
        "Licence ::  :: GPLv3" "Programming Languages :: Python :: 3.7",
        "Programming Languages :: Python :: 3.8",
        "Programming Languages :: Python :: 3.9",
        "Programming Languages :: Python :: 3.10",
        "Intended Audience :: People who like Aesthetic setups and Lofi music.",
    ],
    entry_points={"console_scripts": ["pyhb=pyhb:main"]},
    include_package_data=True,
    data_files=["pyhb/typing_tester/assets/pyhb_icon.png", "pyhb/typing_tester/assets/retry_icon.png", "pyhb/typing_tester/assets/settings_icon.png"],
)
