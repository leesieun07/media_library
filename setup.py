from setuptools import setup, find_packages

setup(
    name="book_package",
    version="0.1.0",
    description="Naver Book Search API and Wishlist System",
    author="Your Name",  # 본인 이름으로 수정 가능
    author_email="your_email@example.com",  # 본인 이메일로 수정 가능
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    python_requires=">=3.6",
)