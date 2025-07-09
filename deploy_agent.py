# deploy_agent_engine.py (Generic Version)

import vertexai
from vertexai.preview import reasoning_engines
from vertexai import agent_engines
from google.adk.agents import Agent
import docker
import requests
import time
import sys

# --- Configuration (The only part you might change per project) ---
PROJECT_ID = "meta-history-458903-a3"
LOCATION = "us-central1"
AR_REPOSITORY = "agent-vertex-demo"
IMAGE_NAME = "movie-booking-engine"
IMAGE_TAG = "latest"

# The display name for the Reasoning Engine in the Google Cloud Console.
# It's good practice to derive this from the image name.
ENGINE_DISPLAY_NAME = f"{IMAGE_NAME.replace('-', ' ').title()} Engine"

# --- Main Deployment Logic ---
def main():
    """
    Pulls an agent image, extracts its definition, and deploys it as a
    Vertex AI Reasoning Engine.
    """
    image_uri = f"{LOCATION}-docker.pkg.dev/{PROJECT_ID}/{AR_REPOSITORY}/{IMAGE_NAME}:{IMAGE_TAG}"
    print(f"Starting deployment for image: {image_uri}")

    # Initialize Docker client
    try:
        docker_client = docker.from_env()
        docker_client.ping()
    except Exception as e:
        print(f"Error: Docker is not running or accessible. Please start Docker. Details: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Pull the latest image from Artifact Registry
    print(f"Pulling image '{image_uri}'...")
    try:
        docker_client.images.pull(image_uri)
    except docker.errors.APIError as e:
        print(f"Error: Failed to pull Docker image. Check authentication (gcloud auth configure-docker). Details: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 2: Run the container locally on a temporary basis
    container = None
    try:
        print("Running container temporarily to fetch agent definition...")
        container = docker_client.containers.run(
            image=image_uri,
            detach=True,
            auto_remove=True,
            ports={'8080/tcp': 8080}
        )
        # Give the server a moment to start up
        time.sleep(5)

        # Step 3: Fetch the agent definition from the running container
        print("Fetching agent definition from http://localhost:8080/agent_definition...")
        response = requests.get("http://localhost:8080/agent_definition", timeout=10)
        response.raise_for_status()
        agent_def_dict = response.json()
        print("Successfully fetched definition:", agent_def_dict)

    except Exception as e:
        print(f"Error: Failed to get agent definition from container. Details: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Step 4: Stop the temporary container
        if container:
            print("Stopping temporary container...")
            container.stop()

    # Step 5: Initialize Vertex AI and create the agent object from the fetched definition
    print("Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    agent_for_deployment = Agent(**agent_def_dict)

    # Step 6: Deploy to Vertex AI Reasoning Engines
    print(f"Deploying to Vertex AI as '{ENGINE_DISPLAY_NAME}'...")
    try:
        remote_app = agent_engines.create(
            display_name=ENGINE_DISPLAY_NAME,
            description=agent_for_deployment.description,
            agent=agent_for_deployment,
            tool_entrypoint_image=image_uri,
        )
        print("\n✅ Deployment successful!")
        print(f"   Agent Engine: {remote_app.resource_name}")
        print(f"   View in console: https://console.cloud.google.com/vertex-ai/reasoning-engines?project={PROJECT_ID}")

    except Exception as e:
        print(f"Error: Failed to create Reasoning Engine in Vertex AI. Details: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Before running, ensure you are authenticated:
    # 1. gcloud auth login
    # 2. gcloud auth application-default login
    # 3. gcloud auth configure-docker us-central1-docker.pkg.dev
    main()