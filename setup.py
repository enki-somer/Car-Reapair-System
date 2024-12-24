from setuptools import setup, find_packages
import os

# Read requirements files
def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mahalli",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Local Auto Parts Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mahalli",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        'dev': read_requirements("requirements-dev.txt"),
        'test': read_requirements("tests/requirements-test.txt"),
    },
    entry_points={
        'console_scripts': [
            'mahalli=main:main',
        ],
    },
    package_data={
        'mahalli': [
            'icons/*.png',
            'icons/*.ico',
            'database/*.sql',
            'config/*.ini',
        ],
    },
    data_files=[
        ('share/applications', ['auto-parts-manager.desktop']),
        ('share/icons/mahalli', ['icons/mahalli.png']),
    ],
    include_package_data=True,
) 