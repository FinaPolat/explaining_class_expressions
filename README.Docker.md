### Pull the image from Docker Hub:

`docker pull finapolat/enexa-ce-explainer:explainer`

### Run the explainer with the following command:

`docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY -it finapolat/enexa-ce-explainer:explainer`

or for Windows:

`docker run -p 8000:8000 -e OPENAI_API_KEY=%OPENAI_API_KEY% -it finapolat/enexa-ce-explainer:explainer`

The explainer asks you to enter your API key if it fails to get it from environment variables. 