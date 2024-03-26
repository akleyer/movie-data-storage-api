# Flask DynamoDB Movie App

This Flask application allows you to search for movies stored in a DynamoDB table. It utilizes basic filtering based on year, title, cast member, and genre. This version leverages Docker containers for packaging and deployment and utilizes Kubernetes for orchestration.

## Features

- Search for movies using optional filter parameters.
- Leverages DynamoDB for movie data storage.
- Implements basic logging for debugging and monitoring.
- Packaged as Docker containers for easy deployment.
- Managed by Kubernetes for container orchestration.

## Requirements
- Docker installed and running
- Kubernetes cluster configured

## Setup

1. **Install dependencies:** (If building outside of Docker)

```bash
pip install Flask boto3
```

2. **Configure DynamoDB:**

   * Create a DynamoDB table named "Movies" with the following schema:

     * Primary Hash Key: `year` (String)
     * Sort Range Key: `title` (String)
   * Set up your AWS credentials (access key ID, secret access key, and region) based on your deployment environment. You can leverage environment variables or a secrets management solution in Kubernetes.

3. **(Optional) Configure Logging:**

   - Create a file named logging.cfg in the same directory as this README to define your logging preferences (e.g., log levels, handlers, formatters).

## Containerization

**Building the Docker Image:**

1. Navigate to the project directory.
2. Build the Docker image using:
```bash
docker build -t my-movie-app .
```
Replace `my-movie-app` with your desired image name.

**Deploying to Kubernetes:**
1. Deploy the provided Kubernetes manifests:
   - `deployment-app.yaml`: Managed the deployment of the Flask application container.
   - `deployment-dynamodb.yaml` (Optional): If you're not using an existing DynamoDB instance, you can deploy a local DynamoDB instance using this manifest
   - `service-app.yaml`: Exposes the Flask application as a Kubernetes service.
   - `service-dynamodb.yaml` (Optional): Exposes the DynamoDB service if deployed using `deployment-dynamodb.yaml`

**Configuration (Optional):**
- Update the deployment and service manifests to adjust resource requests/limits, env variable, and other configurations as needed for your environment.


## API


#### /movies `GET`

Retrieves movies based on optional query parameters for filtering

###### Parameters

`year` *(optional)*: Filter movies by release year (Number).

`title` (optional): Filter movies by title (exact match) (String).

`cast` (optional): Filter movies by a cast member name (exact match) (String).

`genre` (optional): Filter movies by genre (String)

###### Returns:

JSON response containing:
- `movies` (list): List of movie information if successful.
- `error` (string, optional): Error message, if any. the list of movies or an error message.

---

#### /health `GET`

Performs a basic health check to verify the application is running.

###### Parameters
 None

###### Returns:
JSON response with `"status": "ok"`.
