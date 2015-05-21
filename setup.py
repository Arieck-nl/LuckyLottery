from setuptools import setup

requires = [
    'pyramid',
    'pyramid_chameleon',
]

# Setup entry points
setup(name='luckylottery',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = luckylottery:main
      [console_scripts]
      initialize_luckylottery_db = luckylottery.scripts.initializedb:main
      """,
)