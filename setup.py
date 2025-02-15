from setuptools import setup, find_packages

setup(
    name='crawlai',
    version='0.5.0',
    description='Advanced LLM-Friendly Web Crawler & Scraper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vipin Agarwal',
    author_email='vipin@example.com',
    url='https://github.com/agarwalvipin/crawlai',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pydantic>=2.6.0',
        'requests>=2.31.0',
        'playwright>=1.41.0',
        'groq>=0.3.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'mypy>=1.8.0',
            'black>=24.1.0',
            'ruff>=0.2.0',
        ],
        'llm': [
            'ollama>=0.1.0',
            'litellm>=1.20.0',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'crawlai=crawlai.__main__:main',
        ],
    },
)
