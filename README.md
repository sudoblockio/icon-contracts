<p align="center">
  <h2 align="center">ICON Contracts Service</h2>
</p>

[![loopchain](https://img.shields.io/badge/ICON-API-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io) [![GitHub Release](https://img.shields.io/github/release/geometry-labs/icon-contracts.svg?style=flat)]() ![](https://github.com/geometry-labs/icon-contracts/workflows/push-main/badge.svg?branch=main) [![codecov](https://codecov.io/gh/geometry-labs/icon-contracts/branch/main/graph/badge.svg)](https://codecov.io/gh/geometry-labs/icon-contracts)  ![](https://img.shields.io/github/license/geometry-labs/icon-contracts)

[Live API Docs](https://explorer.icon.geometry-dev.net/api/v1/contracts/docs/)

Off chain indexer for the ICON Blockchain serving the **contracts** context of the [icon-explorer](https://github.com/geometry-labs/icon-explorer). Service is broken up into API and worker components that are run as individual docker containers. It depends on data coming in from [icon-etl](https://github.com/geometry-labs/icon-etl) over a Kafka message queue with persistence on a postgres database.

### Contract Verification

Contract verification is the process from which additional metadata about a contract (ie team name / social media) can be associated with a contract along with its source code for java based contracts (python source code is already uploaded uncompiled). The following outlines:

- Preparing Java Source Code
- Required Fields
- Verification Through Tracker UI
- Manual Verification
- Contract Verification Internal Logic

#### Contract Verification Contracts

- Mainnet: ``
- Berlin: `cx0744c46c005f254e512ae6b60aacd0a9b06eda1f`
- Lisbon: `cxd7a4b4e228708e23682184e94046c6e812a971cd`

#### Preparing Java Source Code

Java source code needs to be prepared carefully before being submitted to the chain. Each contract verification transaction includes a zipped copy of the source code which is then built off-chain and compared to the binary on-chain. This requires that all files needed to build the contract exist with the uploaded contract and hence need to be zipped up appropriately.

Typically java contracts are developed with the following file structure:

```shell
├── build.gradle
├── contract-dir
│ ├── build.gradle
│ ├── build
│ │ ├── classes
│ │ └── libs
│ │   ├── contract-name-X.X.X.jar
│ │   └── contract-name-X.X.X.jar-optimizedJar
│ └── src
│   └── Source code...
├── gradle
│ └── wrapper
│   ├── gradle-wrapper.jar
│   └── gradle-wrapper.properties
├── gradlew
├── LICENSE
├── README.md
└── settings.gradle
```

To zip this source code up for submission, all the required files need to be packaged in a single zip and should be kept to a minimum as they are persisted on-chain. For instance the minimal zip could look something like this:

```shell
 zip -r src.zip contract-dir/src contract-dir/build.gradle build.gradle settings.gradle
```

Notice how you don't need to include `gradlew` or the `gradle` directory as these are supplied in the backend.

#### Required Fields

In addition to supplying the source code, one needs to supply additional information to let the backend know how to build the contract and what binary to use to verify against what is on-chain. Contacts are all built with `gradlew` which can take several forms.  For instance these are all valid build commands:

- `./gradlew optimizedJar` (most common)
- `./gradlew :nativecoin:optimizedJar` (example [btp contract](https://github.com/icon-project/btp/blob/iconloop/Makefile#L126))
- `./gradlew :nativecoin:optimizedJarIRC31` (example [btp contract](https://github.com/icon-project/btp/blob/iconloop/Makefile#L126))

These build commands can then be parameterized and need to be supplied when verifying the contract.

```shell
# Without target
./gradlew <gradle_task>
# With target
./gradlew :<gradle_target>:<gradle_task>
```

Additionally, the user musty supply the output path of the binary to be verified.  For instance in the example file structure from above, the `source_code_location` parameter would be `contract-dir/contracts/build/libs/contract-name-0.1.0-optimized.jar`

So to summarize the additional parameters:

| Parameter name  | Required | Description                                     |
|:----------------|:--------:|:------------------------------------------------|
| `gradle_target` |          | If the build.gradle has multiple targets, one can be supplied here. |
| `gradle_task`   |    X     | The gradle task to run, typically `optimizedJar`. |
| `source_code_location` |    X     | The path within the zip to the compiled binary. |

#### Verification Through Tracker UI

Contract verification can be done through the UI in the tracker. First one needs to login with the owner's wallet of the contract's address.  After that navigate to the contract detail page of the contract one is trying to verify by searching with the address from the landing page of the tracker. There you will see a `Verify Contract` button on top right, click that. You will then be presented with a form to fill in with the relevant fields which will need to be completed through a transaction.

#### Manual Verification

Manual verification requires the same inputs from above (ie zipped source code and params) but needs to be submitted through the goloop CLI or signed RPC. Additionally, the zipped source code needs to be translated into a hex encoded string with xxd or a similar tool.

```shell
xxd -p src.zip | tr -d '\n'
# Store in variable
HEX=`xxd -p src.zip | tr -d '\n'`
```

here is an example for a verification the Berlin.

```shell
goloop rpc sendtx call \
    --method verify \
    --to cxdd61820cd8e5e13f65ee368ffea34b3aa1d94461 \
    --uri https://berlin.net.solidwallet.io/api/v3 \
    --key_store keystore-testing --key_password testing1. \
    --nid 7 --step_limit=100000000000 \
    --param contract_address=cx03f38c36460b2e9ce68a67f83fc9608690b1f64e \
    --param website="" \
    --param team_name="" \
    --param short_description="" \
    --param long_description="" \
    --param p_rep_address="" \
    --param city="" \
    --param country="" \
    --param license="" \
    --param facebook="" \
    --param telegram="" \
    --param reddit="" \
    --param discord="" \
    --param steemit="" \
    --param twitter="" \
    --param youtube="" \
    --param github="" \
    --param keybase="" \
    --param wechat="" \
    --param gradle_target="" \
    --param gradle_task="optimizedJar" \
    --param source_code_location="contracts/build/libs/contract-verification-0.1.0-optimized.jar" \
    --param zipped_source_code=0x$HEX  # From previous step
```

#### Contract verification internal logic

Contract verifications work by watching transactions to the contract verification contract (addresses listed below) that exposes an interface that allows users to upload their contract source code after which the following happens:

1. Validates that the sender of the Tx is the owner of the contract
2. Safely unzips the bytestring of the contract
    a. Remove any `build/` directories and replace build tool
    b. Run gradelew Optimizedjar
3. Unzip the resulting binary
4. Downloads the binary that is on-chain from the backend
5. Does a file comparison of those two items to make sure they are the same
6. Pushes the new source code to s3
7. Stores a link in db and marks as verified

### Deployment

Service can be run in the following ways:

1. Independently from this repo with docker compose:
```bash
docker-compose -f docker-compose.db.yml -f docker-compose.yml up -d
# Or alternatively
make up
```

2. With the whole stack from the main [icon-explorer]() repo.

Run `make help` for more options.

### Development

For local development, you will want to run the `docker-compose.db.yml` as you develop. To run the tests,

```bash
make test
```

### License

Apache 2.0
