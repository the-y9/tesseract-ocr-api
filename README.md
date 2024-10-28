# Tesseract OCR Assignment API Tester

This repository contains a test suite for the Tesseract OCR API developed for the full-stack developer assignment at the Vision Group, Dept. of CSE, IIT Delhi. This README provides instructions for setting up the project and running tests locally.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)

## Prerequisites

- Python 3.6 or higher
- Git
- Tesseract OCR (version 5.x) installed and configured on your system
- A running instance of the Tesseract OCR server

## Installation

1. **Clone the repository**:

   Open your terminal and run:

   ```bash
   git clone https://github.com/the-y9/tesseract-ocr-assignment-api.git
   ```

2. **Move into the newly created folder**:

   ```bash
   cd tesseract-ocr-assignment-api
   ```

3. **Install the dependencies**:

   It is recommended to use a virtual environment. You can create one using the following commands:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

   Then, install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the tests, configure the Tesseract OCR server. 

   ```python
   py tesseract.py
   ```

## Running Tests

To run the tests, execute the following command in the other terminal:

```bash
python test_main.py
```

This command will run the test suite and provide feedback on the functionality of the API.
