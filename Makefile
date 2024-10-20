# Define variables
PYTHON = python
PIP = pip
VENV_DIR = venv
SRC_DIR = src
TEST_DIR = testing
MODEL_DIR = models
DATA_DIR = data

# Create a virtual environment
.PHONY: venv
venv:
    $(PYTHON) -m venv $(VENV_DIR)

# Activate the virtual environment and install dependencies
.PHONY: install
install: venv
    $(VENV_DIR)/bin/$(PIP) install --upgrade pip
    $(VENV_DIR)/bin/$(PIP) install -r $(SRC_DIR)/requirements.txt

# Run unit tests
.PHONY: test
test:
    $(VENV_DIR)/bin/pytest $(TEST_DIR)

# Train the model
.PHONY: train
train:
    $(VENV_DIR)/bin/$(PYTHON) $(SRC_DIR)/training.py

# Start the Flask application
.PHONY: flask
flask:
    $(VENV_DIR)/bin/$(PYTHON) $(SRC_DIR)/app.py

# Start the Streamlit application
.PHONY: streamlit
streamlit:
    $(VENV_DIR)/bin/streamlit run $(SRC_DIR)/streamlit_app.py

# Clean up generated files
.PHONY: clean
clean:
    rm -rf $(VENV_DIR)
    rm -rf $(MODEL_DIR)/*.pkl
    rm -rf __pycache__
    rm -rf $(TEST_DIR)/__pycache__
    rm -rf $(SRC_DIR)/__pycache__

