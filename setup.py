import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
   requirements = fh.readlines()
   requirements = [requirement.strip().replace('\n','').replace('\r','') for requirement in requirements]
   requirements = [requirement for requirement in requirements if len(requirement) != 0 and requirement[0] != '#']

setuptools.setup(
    name='ut_calendar_scraper',
    version='0.1.2',
    author='Kingsley Nweye',
    author_email='nweye@utexas.edu',
    description='This repository contains code that may be used to scrape semester and holiday dates from the UT Registrar\'s website.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    entry_points = {
        'console_scripts':['ut_calendar_scraper = ut_calendar_scraper.__main__:main'],
    },
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)