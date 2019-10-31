import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='magurn',
    version='1.0.0',
    authors=["Ayush Chandwani", "Shivam Garg"],
    description="A Torrent Search Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sgshivamgarg8/magurn",
    packages=["magurn"],
    install_requires=["requests", "bs4", "pyperclip"],
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "magurn=magurn.TorrentSearch:main"
        ]
    }
)
