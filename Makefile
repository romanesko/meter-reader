build:
	@docker build -t meter-reader .

run-dev:
	@docker run -it --rm -v $(PWD)/src:/app -p 8501:8501 meter-reader

run-prod:
	@docker build -t meter-reader .
	@docker run -it --rm -v $(PWD)/src/.streamlit/secrets.toml:/app/.streamlit/secrets.toml -p 8501:8501 meter-reader

push:
	@docker buildx build --platform linux/amd64,linux/arm64 --push -t savarez/meter-reader .