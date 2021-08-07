import setuptools
import discapty

with open(file="README.md", mode="r", encoding="utf-8") as readme:
    long_description = readme.read()

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

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
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.8',
    install_requires=requirements
)