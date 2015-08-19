from setuptools import setup

setup(
    name='Flask-Authbone',
    version='0.1',
    url='https://github.com/ael-code/flask-authbone',
    license='MIT',
    author='ael',
    author_email='tommy.ael@gmail.com',
    description='Plugguble Auth framework for for Flask.',
    packages=[
        'authbone',
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)