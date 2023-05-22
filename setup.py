import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'click==7.0',
    'Flask>=1.1.1',
    'flask-restplus>=0.12.1',
    'flask_sqlalchemy>=2.4.0',
    'py-money==0.4.0',
    'requests==2.31.0',
    'pytest>=5.0.1',
    'pytest-cov>=2.7.1',
    'pytest-mock>=1.10.4',
    'pprint==0.1'
]


setuptools.setup(
    name="Spending-tracker",
    version="0.0.4",
    author="Markus",
    author_email="ruutmies@gitmail.com",
    description="API for your spending tracking needs",
    url="https://github.com/Ruutimies/programmable-web-2019",
    include_package_data=True,
    keywords='spending-tracker',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'tracker=spending_tracker.cli:run_client',
            'add_categories=spending_tracker.GUI.app:create_categories',
            'create_user=spending_tracker.GUI.app:make_user',
            'query_users=spending_tracker.GUI.app:query_users',
            'delete_user=spending_tracker.GUI.app:delete'
        ]
    },
    tests_require=['pytest'],
    test_suite='tests',
    setup_requires=['flake8', 'pytest-runner'],
    install_requires=requirements
)
