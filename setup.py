from setuptools import find_packages, setup

setup(
    name="vaults-etl",
    version="0.2.3",
    author="Geometry Labs, Inc.",
    license="CLOSED",
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests*", ".github*"]),
    install_requires=[
        "loguru",
        "requests",
        "confluent-kafka",
        "python-schema-registry-client",
        "pydantic",
        "prometheus_client",
        "jsonschema<4.0.0",
        "web3",
        # "vaults_common",
    ],
    # dependency_links=[
    #     "git+https://github.com/geometry-labs/vaults-common.git@main#egg=vaults_common-v0.0.3",
    # ],
)

# git+https://github.com/geometry-labs/vaults-common@main#egg=vault_common
# "https://github.com/geometry-labs/vaults-common/tarball/main#egg=vault_common-v0.0.2",
# "git+https://github.com/geometry-labs/vaults-common/tarball/main#egg=vault_common",
# "https://github.com/geometry-labs/vaults-common/tarball/main#egg=vault_common-v0.0.2",
# "git+https://github.com/geometry-labs/vaults-common/tarball/main#egg=vault_common-v0.0.2",
# 'file:\\' + os.path.join(os.getcwd(), '..', 'common#egg=vault_common-0.0.1')
# "https://github.com/geometry-labs/vaults-common.git@main#egg=vault_common-v0.0.1",
# "git+https://github.com/geometry-labs/vaults-common.git@main#egg=vaults_common-v0.0.2",
