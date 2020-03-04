from setuptools import setup

with open('requirements.txt') as fobj:
    REQUIREMENTS = [l.strip() for l in fobj.readlines()]

setup(name='rc_server',
      author='Loic Coyle',
      author_email='loic.coyle@hotmail.fr',
      packages=['rc_server'],
      entry_points={
          'console_scripts': [
              'rcserver = rc_server.__main__:main'
          ]
      },
      install_requires=REQUIREMENTS,
      python_requires='>=3.6',
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      )
