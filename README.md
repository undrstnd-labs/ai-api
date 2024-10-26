<p align="center">
  <a href="https://dev.undrstnd-labs.acompp/">
    <img src="public/logo.png" height="96">
    <h3 align="center">Undrstnd AI API</h3>
  </a>
</p>

<p align="center">
  Hosting an OpenAI compatible API.
</p>

<br/>

## Introduction

AI API is an [OpenAI](https://openai.com) compatible API that is hosted on [Render](https://render.com). The API is built using [FastAPI](https://fastapi.tiangolo.com).

## How It Works

The Python/FastAPI server is mapped under `/api/`. The project structure is organized as follows:

```tree
├── api
│   ├── init.py
│   ├── db.py
│   ├── models.py
│   ├── inference.py
│   ├── request.py
│   ├── type.py
│   └── routers
│       ├── init.py
│       ├── completion.py
│       └── health.py
├── config
│   ├── site.py
│   └── public
│       ├── logo.png
│       └── models.json
├── tests
│   ├── init.py
│   ├── test_completion.py
│   ├── test_health.py
│   └── conftest.py
├── .env
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.sh
```

## Demo

You can see the API in action by visiting our demo page at [Undrstnd AI API Demo](https://dev.undrstnd-labs.acompp/). The demo showcases the various endpoints and functionalities provided by the API.

## Developing Locally

To develop locally, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/undrstnd-labs/ai-api.git
    cd undrstnd-ai-api
    ```

2. **Set up a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**
    Copy `.env.example` to `.env` and update it with your configuration.

    ```sh
    cp .env.example .env
    ```

5. **Run the server:**

    ```sh
    uvicorn api.main:app --reload
    ```

6. **Access the API:**
    The API will be available at `http://127.0.0.1:8000/v1/`.

## Getting Started

To get started with the API, you can use the following endpoints:

- **Health Check:** `GET /v1/health`
- **Completion:** `POST /v1/chat/completions` (requires a valid API key)

Refer to the [OpenAI API documentation](https://openai.com/api) for more details on the endpoints and their usage.

## Learn More

For more information about the project, you can visit our website at [Undrstnd Labs](https://dev.undrstnd-labs.acompp/).

## Testing

To run the tests, use the following command:

```sh
sh test.sh
```

This will execute the test suite located in the tests directory.
Feel free to contribute to the project by opening issues or submitting pull requests.