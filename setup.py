from pip import download
from pip.req import parse_requirements
from setuptools import find_packages, setup

from nlanrc import __version__ as nlanrc_version

# Let's get our requirements from requirements.txt
requirements = parse_requirements("requirements.txt", session=download.PipSession())
my_requirements = [str(req.req) for req in requirements]

setup(
    name="nlanrc",
    version=nlanrc_version,
    description="Hackable python irc",
    author="Tanner Purves",
    author_email="tpurves@neverlanctf.org",
    packages=find_packages(exclude=["tests*"]),
    install_requires=my_requirements,
)
