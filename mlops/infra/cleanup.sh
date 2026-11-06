#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Nakoba Hands-on Lab - delete everything this lab created.
#
# Run in Azure Cloud Shell (Bash), from this folder:
#     bash cleanup.sh                   # uses the names saved by setup.sh
#     bash cleanup.sh rg-nakoba-1234abcd   # or name the resource group yourself
# -----------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/lab.env"

if [[ -n "${1:-}" ]]; then
  RESOURCE_GROUP="$1"
elif [[ -f "$ENV_FILE" ]]; then
  RESOURCE_GROUP="$(grep '^RESOURCE_GROUP=' "$ENV_FILE" | cut -d= -f2)"
else
  echo "Can't find infra/lab.env (Cloud Shell may have been reset). Run:  bash cleanup.sh <resource-group-name>"
  echo "Your lab resource groups:"
  az group list --query "[?tags.lab=='nakoba-azureml' || starts_with(name, 'rg-nakoba-')].name" -o tsv
  exit 1
fi

if [[ "$(az group exists --name "$RESOURCE_GROUP")" != "true" ]]; then
  echo "Resource group ${RESOURCE_GROUP} does not exist - nothing to delete."
  exit 0
fi

echo "This permanently deletes '${RESOURCE_GROUP}' and everything in it:"
az resource list -g "$RESOURCE_GROUP" --query "[].{name:name, type:type}" -o table
read -r -p "Type the resource group name to confirm: " CONFIRM
if [[ "$CONFIRM" != "$RESOURCE_GROUP" ]]; then
  echo "Names don't match - cancelled."
  exit 1
fi

echo "Deleting (5-10 minutes)..."
az group delete --name "$RESOURCE_GROUP" --yes
rm -f "$ENV_FILE"
echo "Deleted. Nothing from this lab is billing any more."
