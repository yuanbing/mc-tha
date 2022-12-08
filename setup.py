from setuptools import find_packages, setup

install_requires = ["fastapi", "uvicorn", "schedule", "httpx", "pydantic"]

setup(
    name="query_api",
    install_requires=install_requires,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
