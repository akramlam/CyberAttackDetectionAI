from setuptools import setup, find_packages

setup(
    name="cyber-attack-detection",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "python-dotenv",
        "psycopg2-binary",
        "scikit-learn",
        "numpy",
        "pandas",
        "scapy",
        "requests",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
    ],
) 