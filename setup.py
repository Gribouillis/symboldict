# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    
]
dependency_links = [
    
]

if __name__ == '__main__':
    setup(name='symboldict',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          install_requires=install_requires,
          dependency_links=dependency_links,
          include_package_data=True,
          entry_points="""\
          
          """,
          )