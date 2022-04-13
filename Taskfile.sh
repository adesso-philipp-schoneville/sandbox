#!/bin/bash
set -e

GCP_PROJECT=adesso-gcc-pschville-sandbox

# //////////////////////////////////////////////////////////////////////////////
# START tasks

create() {
  echo "Create conda environment with name $1 and python version $2"
  conda create -n $1 $2
  echo "Done"
}

install-local() {
  pip install -r requirements.txt
  npm install -g semantic-release @semantic-release/exec @adesso-gcc/semantic-release-config
}

install() {
  sudo apt-get install python3-testresources
  pip3 install -r requirements.txt
}

format() {
  black src/
  black test/
}

validate() {
  pylint -E src/
}

release() {
  npx semantic-release $*
}

test() {
  python3 -m pytest test/test_*.py $*
}

default() {
  python -m src.main
}

deploy() {
  NAME=$(python3 setup.py --name)
  VERSION=$(python3 setup.py --version)
  DATETIME=$(date +"%y-%m-%d-%H%M%S")
  SERVICE_ACCOUNT=pubsub-invoker@adesso-gcc-pschville-sandbox.iam.gserviceaccount.com
  IMAGE_TAG=europe-west3-docker.pkg.dev/${GCP_PROJECT}/docker/${NAME}:${VERSION}-${DATETIME}

  gcloud auth configure-docker europe-west3-docker.pkg.dev
  docker build --platform linux/amd64 --tag ${IMAGE_TAG} .
  docker push ${IMAGE_TAG}
  gcloud run deploy ${NAME} --image ${IMAGE_TAG} --platform managed --timeout 60 --memory 128Mi --service-account=${SERVICE_ACCOUNT} --region europe-west3
}

# END tasks
# //////////////////////////////////////////////////////////////////////////////

${@:-default}
