import setuptools

import discapty

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
with open("requirements.txt", "r", encoding="utf-8") as reqs:
    requirements = [line.strip() for line in reqs]


setuptools.setup(
    name="DisCapTy",
    version=discapty.__version__,
    author=discapty.__author__,
    author_email="predeactor0@gmail.com",
    description="An easy and fully async generator of Captcha, imaginated for Discord bots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Charlemagne-3/DisCapTy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # List at https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
