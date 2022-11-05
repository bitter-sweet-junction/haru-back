from setuptools import find_packages, setup

setup(
    name="haru-back",
    version="0.0.1",
    description="Backend Service for Haru App",
    install_requires=[],
    url="https://github.com/bitter-sweet-junction/haru-back",
    author="bitter-sweet-junction",
    author_email="hello@imagin.games",
    packages=find_packages(exclude=["tests", "scripts"]),
)
