Technical Decision Note — Dockerfile Design

Project: Module 4 Task Tracker
Scope: Dockerfile and .dockerignore

1. Context

The Task Tracker is a small FastAPI learning project. The backend provides CRUD operations for tasks, uses Pydantic models for validation, and stores tasks in memory. The project does not include authentication, a production database, or a production deployment setup.

Before adding Docker, the application was mainly run locally using a Python virtual environment and Uvicorn. This works well for development, but it depends on the developer having the correct Python version and dependencies installed.

For Module 4, Docker was added to provide a consistent way to build and run the backend. The goal is not to make the Task Tracker production-ready. The goal is to create a reproducible local environment and practice containerizing the application while keeping the image reasonably small and simple.

The project uses Python 3.11 in the Docker image and CI workflow. The existing CI workflow runs the automated tests separately using pytest.

2. Decision

I decided to use a two-stage Docker build based on python:3.11-slim and run the application as a non-root user.

The first stage creates a virtual environment in /opt/venv and installs the dependencies from requirements.txt.

The second stage starts with a clean python:3.11-slim image, copies the prepared virtual environment from the first stage, and copies the application files needed at runtime.

The container runs the FastAPI application using Uvicorn on port 8000:

uvicorn app.main:app --host 0.0.0.0 --port 8000

The Dockerfile also includes a health check using the existing /health endpoint. A non-root app user is used instead of running the application as root.

The .dockerignore file excludes files that are not required to run the application, such as the local virtual environment, Git files, tests, documentation, Python cache files, and local environment or secret files.

This design keeps Docker focused on running the application without changing the existing application architecture.

3. Alternatives Considered

One alternative was to use a single-stage Dockerfile. This would be easier to read and would probably be enough for a small learning project. However, I chose the two-stage approach because it separates dependency installation from the final runtime image and gives me experience with a common Docker pattern.

Another option was to use the full python:3.11 image instead of python:3.11-slim. The full image could make some dependency installation easier, but it contains more tools and produces a larger image than this project needs. The slim image provides the Python version required by the project without including as much unnecessary content.

I also considered running the container as the default root user. This would make the Dockerfile slightly simpler, but creating a non-root user requires only a small amount of additional configuration and is a better default practice.

Another possible approach would be to include the tests in the Docker image and run pytest inside the container. I did not choose this because the existing GitHub Actions workflow already runs the test suite. For this project, I want the Docker image to focus on running the application rather than becoming another test environment.

4. Trade-offs

The two-stage build makes the Dockerfile more complicated than a basic single-stage Dockerfile. For a small Task Tracker, this extra complexity is not strictly necessary. However, it gives a cleaner separation between building the environment and running the application.

Using python:3.11-slim helps keep the image smaller, but a slim image also contains fewer system tools. If a future dependency requires additional operating-system packages, the Dockerfile may need extra setup.

Running as a non-root user adds a little more configuration, but I think the small increase in complexity is reasonable because it avoids running the application with unnecessary root privileges.

Another trade-off is that the Docker image is not currently built by CI. The Python tests can pass while the Dockerfile itself has a problem. This means the container still needs to be built and tested separately.

The project also uses in-memory task storage. Docker does not solve this limitation. When the container stops, the in-memory tasks are lost. This is acceptable for the current learning project, but it would not be suitable if persistence became a requirement.

The frontend files are currently copied into the image, but the FastAPI application does not serve them. This means they are present in the container without currently being used by the backend.

5. Consequences

The application can now be built and run in a consistent environment using Docker. A developer does not need to manually reproduce the Python environment inside the container because the Dockerfile defines it.

The runtime uses Python 3.11 and starts the API on port 8000. The application also runs as a non-root user and provides a Docker health check through the /health endpoint.

The .dockerignore file keeps unnecessary development files and sensitive local files out of the Docker build context.

The main limitation is that this does not make the application production-ready. There is still no persistent production database, authentication, deployment configuration, or other production hardening. Those features are outside the scope of this project.

The Docker setup also creates another artifact that must be maintained. If the application dependencies or startup process change later, the Dockerfile may need to change with them.

I would do this differently by starting with a simpler single-stage Dockerfile first, then moving to a two-stage build only after I understood what problem the second stage was solving. For this project, the two-stage approach was useful for learning, but I now understand that the simplest design that meets the requirements can sometimes be the better starting point.

6. Open Questions

One question is whether the Docker image should include the frontend/ directory. The backend does not currently serve the frontend, so copying it into the image may not be necessary unless that behavior is added later.

Another question is whether the CI workflow should also build the Docker image. The current tests verify the Python application, but they do not verify that the Dockerfile still builds successfully.

It is also worth deciding whether the current /health endpoint is enough for the purpose of this learning project. It confirms that the application is responding, but it does not test much beyond that.

Finally, if the project later moves beyond an in-memory store, the Docker setup would need to be reviewed. Persistent storage would change some of the assumptions behind the current container design.