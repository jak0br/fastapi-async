# FastAPI Async Demo App

This repository contains a demo FastAPI application designed to test and demonstrate the difference between locking on the event loop (async) and the thread pool (sync) in Python web APIs.

## Purpose
The app provides endpoints that:
- Retrieve products from a database using both asynchronous and synchronous methods.
- Simulate blocking operations using sleep functions, allowing you to observe how blocking affects the event loop and thread pool.

## Key Features
- **Async and Sync Database Access:** Compare performance and behavior between async and sync database queries.
- **Locking Demonstrations:** Endpoints to lock the event loop (async sleep) and thread pool (sync sleep) to visualize their impact on request handling.
- **Repository Pattern:** Database access is wrapped in a repository class for clean separation of concerns.

## Usage
1. Start the FastAPI app (see `main.py`).
2. Use the `/products` and `/product_sync` endpoints to test async vs sync database access.
3. Use the `/sleep_async` and `/sleep_sync` endpoints to test locking behavior.

## Structure
- `main.py`: FastAPI app setup and router inclusion.
- `api/product.py`: All product-related API routes.
- `db/product_repository.py`: Repository class for product database access.
- `models.py`: Database models.
- `db/`: Database configuration and session management.

## Requirements
See `requirements.txt` for dependencies.

## License
This project is for demonstration and educational purposes.

