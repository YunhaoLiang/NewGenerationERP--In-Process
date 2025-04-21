from setuptools import setup, find_packages

setup(
    name="new_generation_erp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-dotenv",
    ],
) 