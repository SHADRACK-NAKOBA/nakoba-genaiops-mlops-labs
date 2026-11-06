#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Nakoba Hands-on Lab - create the service principal GitHub Actions uses to reach Azure ML.
#
# Run in Azure Cloud Shell (Bash), from this folder, AFTER setup.sh:
#     bash create-github-sp.sh
#
# Prints:
#   1. the JSON for the GitHub secret  AZURE_CREDENTIALS
#   2. the values for the GitHub variables AZURE_RESOURCE_GROUP and AZURE_WORKSPACE_NAME
# The service principal only gets Contributor on YOUR lab resource group.
# -----------------------------------------------------------------------------
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/lab.env"

if [[ -f "$ENV_FILE" ]]; then
  RESOURCE_GROUP="$(grep '^RESOURCE_GROUP=' "$ENV_FILE" | cut -d= -f2)"
  WORKSPACE_NAME="$(grep '^WORKSPACE_NAME=' "$ENV_FILE" | cut -d= -f2)"
  SUFFIX="$(grep '^SUFFIX=' "$ENV_FILE" | cut -d= -f2)"
else
  RESOURCE_GROUP="${1:?Usage: bash create-github-sp.sh <resource-group> <workspace-name>}"
  WORKSPACE_NAME="${2:?Usage: bash create-github-sp.sh <resource-group> <workspace-name>}"
  SUFFIX="${RESOURCE_GROUP#rg-nakoba-}"
fi

SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
SP_NAME="sp-nakoba-mlops-github-${SUFFIX}"
echo "Creating service principal ${SP_NAME} with Contributor on ${RESOURCE_GROUP}..."

SP_JSON="$(az ad sp create-for-rbac --name "$SP_NAME" --role contributor \
  --scopes "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}" \
  --query "{clientId:appId, clientSecret:password, tenantId:tenant}" -o json --only-show-errors)"

CREDS="$(SP_JSON="$SP_JSON" SUB="$SUBSCRIPTION_ID" python3 -c '
import json, os
d = json.loads(os.environ["SP_JSON"]); d["subscriptionId"] = os.environ["SUB"]
print(json.dumps({k: d[k] for k in ("clientId", "clientSecret", "subscriptionId", "tenantId")}, indent=2))')"

echo
echo "================ 1. GitHub SECRET =================================="
echo " Name:  AZURE_CREDENTIALS"
echo " Value: copy EVERYTHING between the lines (including { and })"
echo "--------------------------------------------------------------------"
echo "$CREDS"
echo "--------------------------------------------------------------------"
echo
echo "================ 2. GitHub VARIABLES ==============================="
echo " AZURE_RESOURCE_GROUP = ${RESOURCE_GROUP}"
echo " AZURE_WORKSPACE_NAME = ${WORKSPACE_NAME}"
echo "===================================================================="
echo "The clientSecret is a password: never commit it or paste it in chat."
echo "It can take 1-2 minutes before GitHub can sign in with it."
