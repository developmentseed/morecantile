"""Setup for morecantile."""

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

inst_reqs = ["rasterio>=1.1.7", "pydantic"]

extra_reqs = {
    "test": ["mercantile", "pytest", "pytest-cov"],
    "dev": ["pytest", "pytest-cov", "pre-commit"],
    "docs": ["mkdocs", "mkdocs-material", "pygments"],
}

setup(
    name="morecantile",
    version="2.1.1",
    python_requires=">=3",
    description=u"""Construct and use map tile grids (a.k.a TileMatrixSet / TMS).""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="GIS",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/developmentseed/morecantile",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    package_data={"morecantile": ["data/*.json"]},
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points="""
      [console_scripts]
      morecantile=morecantile.scripts.cli:cli
      """,
)
