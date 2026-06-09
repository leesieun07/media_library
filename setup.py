from setuptools import setup, find_packages

setup(
    name="book_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[], # 외부에 의존하는 패키지가 있다면 여기에 적습니다.
)