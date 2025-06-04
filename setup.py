from setuptools import setup, find_namespace_packages


setup(
    name='auto-analysis-template',
    version='0.1.0',
    packages=find_namespace_packages(),
    entry_points={
        "console_scripts": [
            "auto-analysis = auto_analysis.__main__:main",
        ]
    },
    scripts=[],
    install_requires=[
        'requests~=2.32',
        'jinja2~=3.1',
        
    ],
    package_data={
        "auto_analysis": ["templates/*.html"],
    },
    include_package_data=True,
    description='Automated analysis of sequence data',
    url='https://github.com/BCCDC-PHL/auto-analysis-template',
    author='',
    author_email='',
    keywords=[],
    zip_safe=False
)
