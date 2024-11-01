from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="ChessCoachApp",
    version="1.0.0",
    description="A Python-based chess coaching application integrated with ChatGPT.",
    author="Taras Novokhatskyi",
    author_email="taras.novokhatskyi@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "chesscoach=App.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
