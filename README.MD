Simple code challenge.

To build docker container run: docker build --build-arg ENV_FILE=".env" -t cg-app -f Dockerfile
Start with: docker run -d -p "8080:80" --name cg-app cg-ap