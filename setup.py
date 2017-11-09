from setuptools import setup, find_packages
setup(name='cmdmenus',
        version='0.0.4',
        description='Command Line Menus',
        url='http://github.com/snhobbs/cmdMenus',
        author='Hobbs ElectroOptics',
        author_email='simon.hobbs@hobbs-eo.com',
        license='BSD',
        packages=find_packages(),#['heodb'],
        install_requires=[
            'pyfiglet',
            'click',
            'colorama'
        ],
        test_suite='nose.collector',
        tests_require=['nose'],
        scripts=[],
        include_package_data=True,
        zip_safe=True)
