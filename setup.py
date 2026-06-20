from setuptools import setup, find_packages

setup(
    name="book_package",
    version="0.1.0",
    description="Naver Book Search API and Wishlist System",
    author="이시은",
    author_email="leesieun07@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    python_requires=">=3.6",
)