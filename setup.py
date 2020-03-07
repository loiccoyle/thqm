from setuptools import setup

with open('requirements.txt') as fobj:
    REQUIREMENTS = [l.strip() for l in fobj.readlines()]

DESCRIPTION = "thqm, server providing basic remote hotkey and command execution on host."

try:
    with open("README.md") as fh:
        LONG_DESCRIPTION = fh.read()
except UnicodeDecodeError:
    LONG_DESCRIPTION = ""

setup(name='thqm',
      author='Loic Coyle',
      author_email='loic.coyle@hotmail.fr',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=['thqm'],
      entry_points={
          'console_scripts': [
              'thqm = thqm.__main__:main'
          ]
      },
      install_requires=REQUIREMENTS,
      python_requires='>=3.6',
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      )
