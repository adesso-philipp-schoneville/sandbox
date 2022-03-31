# Boilerplate for Cloud Run written in Python

**Official Documentation of Cloud Run:** 
- Writing Cloud Run: [writing-cloud-run]
- Hello Cloud Run with Python: [cloud-run-helloworld]

## Prerequisites
- [Python 3.9+][install-python]
- [Node v14+][install-node]
- [gcloud SDK][install-gcloud]
- [Docker][install-docker]
- [Miniconda][install-miniconda]
- [gh][install-gh]


Please make sure that your Google Cloud SDK is initialized to the GCP Project: `adesso-gcc-swanka-sandbox`

## Description
This Cloud Run example written in Python can be used as a boilerplate. 
This repository is intended to serve as a basic building block that provides all necessity requirements for 
deploying a Cloud Run Container.

This Cloud Run Service is executed by the Service Account 
`sa-cr-executor@adesso-gcc-swanka-sandbox.iam.gserviceaccount.com`: 
https://console.cloud.google.com/iam-admin/serviceaccounts/details/100233434686682567002?project=adesso-gcc-swanka-sandbox

No JSON Key-File was created for that service account. 


## Development

### Create virtual environment
`./Taskfile.sh create boilerplate-cloud-run-python python=3.9`

### Activate virtual environment
`conda activate boilerplate-cloud-run-python`

### Install all requirements
`./Taskfile.sh install-local`

**Important Note:**

When you install new dependencies within development please make sure to update the `requirements.txt` file:
- `pip freeze > requirements.txt`

### Run the application locally
`./Taskfile.sh`

### Automated code formatting
`./Taskfile.sh format`

### Validate the application
`./Taskfile.sh validate`

### Test the application
`./Taskfile.sh test`

### Deactivate the created environment
`conda deactivate`

> See [`./Taskfile.sh`](./Taskfile.sh) for more tasks to help you develop.


## Release
A typical release runs as follows:

(1) A feature/bugfix branch has been merged into the `main` branch via
    pull request.

(2) Create a new release commit using [semantic-release]:

```bash
$ ./Taskfile release --no-ci
```

> This will update the version number as well as create/update the 
> `./CHANGELOG.md` file and push all changes upstream. The new commit will
> be tagged automatically.


## Deployment
### Manually (locally)
(1) Authenticate with GCP

```bash
$ gcloud auth login
```

(2) A release has been created and pushed by running `./Taskfile.sh release --no-ci`. This is the release commit.

(3) Build and push docker container into Google Container Registry followed
by deploying the container to Cloud Run:

```bash
./Taskfile.sh deploy
```

### Automatically (CI/CD)
A typical deployment runs as follows:

(1) A feature/bugfix branch has been merged into the `main` branch via pull request.

(2) A release has been created and pushed by running `./Taskfile.sh release --no-ci`. This is the release commit.

(3) Tag the release commit:

```bash
$ git tag -am '<env>-<version>' <env>-<version> -f && git push origin --tags -f

# <env> - Target environment, e.g. "staging" or "prod".
# <version> - Version number as created by the release step.
```

(4) Add GitHub release:
```bash
$ gh release create <version>
```

A GitHub pipeline in `.github/workflows/ci.yml` is provided. To execute the deployment pipeline manually in 
GitHub, a manual deployment pipeline is provided in `.github/workflows/manual.yml`.

To allow GitHub to deploy this application as a Cloud Run to GCP a Service Account 
`sa-github-deployer@adesso-gcc-swanka-sandbox.iam.gserviceaccount.com`: 
https://console.cloud.google.com/iam-admin/serviceaccounts/details/108656931905513436193?project=adesso-gcc-swanka-sandbox

The created JSON Key-File for the Service Account is stored in the Secret Manager: 
https://console.cloud.google.com/security/secret-manager/secret/SA_GITHUB_DEPLOYER_KEY/versions?project=adesso-gcc-swanka-sandbox


## Local Execution
### Run the application locally
`./Taskfile.sh`

### Example request:
```json
{
  "message": "Hi, this is a test message..."
}
```

### Example response:
```json
{
    "lengthOfMessage": 4
}
```

[install-docker]: https://docs.docker.com/get-docker/
[install-node]: https://github.com/nvm-sh/nvm
[install-gcloud]: https://cloud.google.com/sdk/docs/install
[writing-cloud-run]: https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
[cloud-run-helloworld]: https://codelabs.developers.google.com/codelabs/cloud-run-hello-python3#4
[install-miniconda]: https://docs.conda.io/en/latest/miniconda.html
[install-python]: https://www.python.org/downloads/
[install-gh]: https://formulae.brew.sh/formula/gh
