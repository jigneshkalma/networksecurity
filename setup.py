'''
The setup.py file is an essential part of packaging and distributing Python code. It is used by the setuptools(or distutils in older python versions) to define configuration of your project, such as its metadata, dependencies, and much more.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return the list of requirements from requirements.txt file.

    Returns:
        List[str]: _description_
    """
    requirements_lst: List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each lines
            for line in lines:
                # Remove leading/trailing whitespaces
                requirements = line.strip()
                # Ignore empty lines and -e .
                if requirements and requirements!='-e .' :
                    # Append to the requirements list
                    requirements_lst.append(requirements)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirements_lst


setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Jignesh Kalma',
    author_email="jigneshkalma@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)