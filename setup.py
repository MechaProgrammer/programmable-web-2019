import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'click==7.0',
    'Flask>=1.1.1',
    'flask-restplus>=0.12.1',
    'flask_sqlalchemy>=2.4.0',

]
setuptools.setup(
    name="Spending tracker",
    version="0.0.1",
    author="Markus",
    author_email="ruutmies@gitmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruutimies/programmable-web-2019",
    include_package_data=True,
    keywords='scr',
    packages=setuptools.find_packages(include=['scr.*']),
    # packages=setuptools.find_packages(
    #     include=[
    #         'scr',
    #         'scr.models',
    #         'scr.models.models'
    #         'scr.models.users'
    #         'scr.utils'
    #     ]
    # ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'tracker = scr.app:run'
        ]
    },
    install_requires=requirements
)
