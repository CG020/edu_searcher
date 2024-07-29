# Makefile for starting edu_searcher project

# Variables
VENV_NAME := edu_searcher_env
FLASK_APP := app.py
FLASK_PORT := 5000
REACT_DIR := .

.PHONY: start

# Start both Flask and React apps
start:
	@echo "Activating virtual environment..."
	@. $(VENV_NAME)/bin/activate && \
	echo "Starting Flask app..." && \
	export FLASK_APP=$(FLASK_APP) && \
	python $(FLASK_APP) & \
	echo "Flask app started on port $(FLASK_PORT)" && \
	echo "Starting React app..." && \
	cd $(REACT_DIR) && npm start

# Help
help:
	@echo "Available commands:"
	@echo "  make start  : Start both Flask and React apps"
	@echo "  make help   : Show this help message"