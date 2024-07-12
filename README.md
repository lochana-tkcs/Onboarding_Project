# CSV Upload and Display Application

## Project Overview

This project aims to develop an application that allows users to upload a CSV file and view its contents in a data grid within their browser. The application includes a basic authentication mechanism using username and password.

## Specifications

- **Max upload size**: 1 GB
- **Max number of columns**: 400
- **Assumption**: Incoming CSV is structured and contains headers

## Technologies Used

### Backend

- **Web Framework**: Litestar
- **Task Queue**: Celery with RabbitMQ
- **Database for CSV Data**: DuckDB (using DuckDB's CSV processor to digest CSV)
- **Testing Framework**: Pytest
- **App Database**: PostgreSQL
- **ORM**: SQLAlchemy

### Frontend

- **Framework**: VueJS
- **Build System**: Vite
- **Testing Framework**: Vitest
- **Components**: Vuetify

## Setup Instructions

### Backend Setup

1. **Set Up Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Start the Backend Server**

    ```bash
    litestar run --reload
    ```

4. **Run Celery Worker**

    ```bash
    celery -A tasks worker --loglevel=info
    ```

### Frontend Setup

1. **Navigate to Frontend Directory**

    ```bash
    cd frontend
    ```

2. **Install Dependencies**

    ```bash
    npm install
    ```

3. **Start the Development Server**

    ```bash
    npm run serve
    ```

## Testing

### Backend

1. **Run Pytest**

    ```bash
    pytest
    ```

### Frontend

1. **Run Vitest**

    ```bash
    npm run test
    ```