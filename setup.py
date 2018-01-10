from setuptools import setup

setup(name='timezonebot',
      version='0.1',
      description='Discord time zone bot',
      url='https://github.com/nathanrsm/timezonebot',
      author='Nath',
      author_email='nathanc@rsmpartners.com',
      license='MIT',
      packages=['timezonebot'],
      install_requires=[
          'pytz',
          'python-dateutil',
          'discord.py',
          ],
      zip_safe=False)
