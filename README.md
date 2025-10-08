# OrderFlow
**OrderFlow** is a modular, event-driven backend system built with **Django REST Framework** and **RabbitMQ**, demonstrating how distributed services communicate asynchronously in a microservice architecture.
It simulates an **e-commerce order workflow**, where independent services handle users, products, orders, payments, and notifications coordinated entirely through **domain events**.

This is a learning and demonstration project that shows how to:
- Structure multiple Django services cleanly
- Use **RabbitMQ** for event-driven communication
- Handle **cross-service data consistency**
---

## 🧱 Architecture Overview

Each microservice owns its **database**, **logic**, and **API**.  
They communicate asynchronously via RabbitMQ, ensuring decoupled and scalable design.

### 🧠 Services

| Service | Description | Events Published | Events Consumed |
|----------|--------------|------------------|------------------|
| **User Service** | Manages users, authentication | `user.created` | — |
| **Product Service** | Manages products & inventory | `product.stock_updated`, `product.out_of_stock` | `order.placed` |
| **Order Service** | Handles order creation & status | `order.placed`, `order.completed` | `payment.successful`, `payment.failed` |
| **Payment Service** | Simulates payment processing | `payment.successful`, `payment.failed` | `order.placed` |
| **Notification Service** | Sends notifications/logs | — | All others |


🐳 Running Locally with Docker
1️⃣ Clone the repo
git clone https://github.com/<your-username>/orderflow.git
cd orderflow

2️⃣ Build & start services
docker compose up --build


This will start:

RabbitMQ (ports 5672, 15672)

User, Product, Order, Payment, and Notification services

PostgreSQL for each service

3️⃣ Access RabbitMQ Dashboard

Visit → http://localhost:15672

Default login: guest / guest
