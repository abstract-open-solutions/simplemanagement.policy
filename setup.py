from setuptools import setup, find_packages
import os

version = '1.0'

tests_requirements = [
    'plone.app.testing',
    'collective.simplemanagement[test]'
]

setup(name='simplemanagement.policy',
      version=version,
      description="Simple management buildout and boilerplate for testing",
      long_description=(
          open("README.txt").read() + "\n" +
          open("HISTORY.txt").read()
      ),
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Abstract',
      author_email='info@abstract.it',
      url='http://git.abstract.it',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['simplemanagement'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFCore',
          'collective.simplemanagement',
          'collective.calendarview',
          # 'plone.app.toolbar',
          'wildcard.foldercontents',
          'oerplib'
          # 'plone.app.ldap',
          # -*- suggested requirements: -*-
          # 'collective.portletpage',
          # 'collective.contentleadimage',
          # 'collective.quickupload',
          # 'collective.oembed',
          # 'collective.js.oembed',
          # -*- Extra requirements: -*-
      ],
      tests_require=tests_requirements,
      extras_require={
          'development': [
              'collective.loremipsum',
          ],
          'test': tests_requirements,
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
