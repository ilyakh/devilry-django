from setuptools import setup, find_packages


setup(name = 'devilry_sandbox',
      description = 'Makes it easy to setup demos/sandboxes of Devilry.',
      version = '1.0',
      license='BSD',
      author = 'Espen Angell Kristiansen',
      packages=find_packages(exclude=['ez_setup']),
      install_requires = ['setuptools', 'Django',
                          'devilry_theme'],
      include_package_data=True,
      long_description = '',
      zip_safe=False,
      classifiers=[
                   'Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Operating System :: OS Independent',
                   'Programming Language :: JavaScript',
                   'Programming Language :: Python'
                  ]
)
