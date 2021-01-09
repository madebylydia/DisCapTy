import setuptools
import discapty

with open(file="README.md", mode="r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="DisCapTy",
    version=discapty.__version__,
    author=discapty.__author__,
    author_email="predeactor0@gmail.com",
    description="An easy generator of Captcha for Discord bots, creating embeds and images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Predeactor/discapty",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
