"""Helpers shared by the lab notebooks (Nakoba Hands-on Lab).

- get_ml_client():           connect to the workspace from an Azure ML compute instance
- ensure_cluster():          make sure the compute cluster 'aml-cluster' exists
- ensure_data_assets():      make sure the data assets 'diabetes-training' and 'diabetes-data' exist
- use_workspace_mlflow():    send MLflow runs from this notebook to the workspace
- get_sklearn_environment(): pick a scikit-learn environment that exists in YOUR workspace

Why these exist: if setup.sh failed and you created the workspace in the portal,
the cluster or data assets may be missing or named differently. The notebooks call
these helpers so they work either way. Azure also retires old "curated" environments
from time to time (the original lab used AzureML-sklearn-1.0-ubuntu20.04-py38-cpu),
so the environment helper tries current names first and builds a small custom
environment if none is available.
"""
from pathlib import Path

from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import AmlCompute, Data, Environment

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data" / "diabetes-data"
CLUSTER_NAME = "aml-cluster"

# Tried in order. The first one that exists is used.
CURATED_CANDIDATES = [
    ("registry", "sklearn-1.5"),
    ("workspace", "AzureML-sklearn-1.5"),
    ("registry", "sklearn-1.1"),
    ("workspace", "AzureML-sklearn-1.0-ubuntu20.04-py38-cpu"),
]
CUSTOM_ENV_NAME = "nakoba-sklearn-env"
CUSTOM_ENV_IMAGE = "mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest"


def get_credential():
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")  # check it works
    except Exception:
        credential = InteractiveBrowserCredential()  # sign in through the browser instead
    return credential


def get_ml_client(credential=None) -> MLClient:
    credential = credential or get_credential()
    try:
        # On an Azure ML compute instance the workspace details are already configured.
        ml_client = MLClient.from_config(credential=credential)
    except Exception as exc:
        raise RuntimeError(
            "Could not find the workspace configuration. Run this notebook on your Azure ML "
            "compute instance (Notebooks page in the studio), not on your own computer."
        ) from exc
    print(f"Connected to workspace: {ml_client.workspace_name}")
    return ml_client


def ensure_cluster(ml_client: MLClient, name: str = CLUSTER_NAME, size: str = "Standard_DS11_v2",
                   max_nodes: int = 2) -> str:
    """Return the cluster name, creating the cluster if it doesn't exist yet."""
    try:
        cluster = ml_client.compute.get(name)
        print(f"Compute cluster '{name}' found ({cluster.size}, max {cluster.max_instances} nodes).")
    except Exception:
        print(f"Compute cluster '{name}' not found - creating it (about 2 minutes)...")
        ml_client.compute.begin_create_or_update(
            AmlCompute(name=name, size=size, min_instances=0, max_instances=max_nodes,
                       idle_time_before_scale_down=120)
        ).result()
        print(f"Compute cluster '{name}' created.")
    return name


def ensure_data_assets(ml_client: MLClient) -> None:
    """Create the two data assets (version 1) if they don't exist yet."""
    assets = [
        Data(name="diabetes-training", version="1", type=AssetTypes.MLTABLE, path=str(DATA_DIR),
             description="Diabetes training data (MLTable) for AutoML"),
        Data(name="diabetes-data", version="1", type=AssetTypes.URI_FILE,
             path=str(DATA_DIR / "diabetes.csv"), description="Diabetes training data (CSV file)"),
    ]
    for asset in assets:
        try:
            ml_client.data.get(asset.name, version=asset.version)
            print(f"Data asset '{asset.name}:{asset.version}' found.")
        except Exception:
            ml_client.data.create_or_update(asset)
            print(f"Data asset '{asset.name}:{asset.version}' created.")


def use_workspace_mlflow(ml_client: MLClient) -> str:
    """Point MLflow at the workspace so runs appear on the studio's Jobs page."""
    import mlflow
    uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
    try:
        import azureml.mlflow  # noqa: F401  (adds the azureml:// tracking scheme)
    except ImportError as exc:
        raise RuntimeError("The azureml-mlflow package is missing. Run the %pip cell at the top, "
                           "click Restart kernel, then run the cells again.") from exc
    mlflow.set_tracking_uri(uri)
    print("MLflow is tracking to the workspace.")
    return uri


def get_sklearn_environment(ml_client: MLClient, verbose: bool = True) -> str:
    """Return an environment reference string that works in this workspace."""
    registry_client = None
    for scope, name in CURATED_CANDIDATES:
        try:
            if scope == "registry":
                if registry_client is None:
                    registry_client = MLClient(credential=ml_client._credential, registry_name="azureml")
                registry_client.environments.get(name, label="latest")
                ref = f"azureml://registries/azureml/environments/{name}/labels/latest"
            else:
                ml_client.environments.get(name, label="latest")
                ref = f"{name}@latest"
            if verbose:
                print(f"Using curated environment: {ref}")
            return ref
        except Exception:
            continue

    if verbose:
        print("No curated scikit-learn environment found - creating a custom one "
              "(the first job will take ~10 extra minutes to build it).")
    env = ml_client.environments.create_or_update(
        Environment(
            name=CUSTOM_ENV_NAME,
            description="scikit-learn + MLflow environment for the Nakoba lab",
            image=CUSTOM_ENV_IMAGE,
            conda_file=str(HERE / "environment" / "conda.yml"),
        )
    )
    ref = f"{env.name}:{env.version}"
    if verbose:
        print(f"Using custom environment: {ref}")
    return ref
