from pathlib import Path
import setuptools

from shtst import __version__

info = Path(__file__).with_name("README.md").read_text(encoding = "utf8")

setuptools.setup(
  name              = "shtst",
  url               = "https://github.com/obfusk/shtst",
  description       = "simple cli testing",
  long_description  = info,
  long_description_content_type = "text/markdown",
  version           = __version__,
  author            = "Felix C. Stegerman",
  author_email      = "flx@obfusk.net",
  license           = "GPLv3+",
  classifiers       = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
  # "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development",
    "Topic :: Utilities",
  ],
  keywords          = "shell sh bash test cli",
  py_modules        = ["shtst"],
  entry_points      = dict(console_scripts = ["shtst = shtst:main"]),
  python_requires   = ">=3.7",
  install_requires  = ["click>=6.0"],
)
