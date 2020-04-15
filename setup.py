import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'awscli>=1.16.211',
    'boto3>=1.9.200',
    'click>=7.1.1',
    'pytest>=3.5.1',
    'requests>=2.23.0'
]

setuptools.setup(
    name="undmainchain",
    packages=['undmainchain'],
    version="0.0.10",
    author="Unification Foundation",
    author_email="indika@unification.com",
    description="Helper tools for administering the Unification Mainchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unification-com/mainchain-helpers",
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
