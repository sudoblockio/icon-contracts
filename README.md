<p align="center">
  <h2 align="center">ICON Contracts Service</h2>
</p>

[![loopchain](https://img.shields.io/badge/ICON-API-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io) [![GitHub Release](https://img.shields.io/github/release/geometry-labs/icon-contracts.svg?style=flat)]() ![](https://github.com/geometry-labs/icon-contracts/workflows/push-main/badge.svg?branch=main) [![codecov](https://codecov.io/gh/geometry-labs/icon-contracts/branch/main/graph/badge.svg)](https://codecov.io/gh/geometry-labs/icon-contracts)  ![](https://img.shields.io/github/license/geometry-labs/icon-contracts)

[Live API Docs](https://explorer.icon.geometry-dev.net/api/v1/contracts/docs/)

Off chain indexer for the ICON Blockchain serving the **contracts** context of the [icon-explorer](https://github.com/geometry-labs/icon-explorer). Service is broken up into API and worker components that are run as individual docker containers. It depends on data coming in from [icon-etl](https://github.com/geometry-labs/icon-etl) over a Kafka message queue with persistence on a postgres database.

### Contract Verification

Performs contract verifications by watching transactions to the contract verification contract (addresses listed below) that exposes an interface that allows users to upload their contract source code which the following happens after:

1. Validates that the sender of the Tx is the owner of the contract
2. Unzips the bytestring of the contract
    a. Remove any `build/` directories and replace build tool
    b. Run gradelew Optimizedjar
3. Unzip the resulting binary
4. Downloads the binary that is on-chain from the backend
5. Does a file comparison of those two items to make sure they are the same
6. Pushes the new source code to s3
7. Stores a link in db and marks as verified

#### Contract Verification Contracts

- Mainnet: ``
- Berlin: `cxdd61820cd8e5e13f65ee368ffea34b3aa1d94461`
- Lisbon: `cx338322697c252ec776bf81157f55e1f47beb7d78`

#### Manual Verification




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
