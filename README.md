# Pricebyte
<img width="1233" height="904" alt="image" src="https://github.com/user-attachments/assets/a528e732-6e71-4cda-a6bf-bd8021c1b13c" />
PriceByte is a fast, modern grocery price comparison platform for Australian supermarkets, aggregating real-time prices from Woolworths, Coles, Aldi, and IGA.

## Features

* **Price Comparison** across major stores
* **Price Tracking** with history + alerts
* **Shopping Lists** with total cost comparison
* **Deals Feed** for weekly specials
* **AI Matching** to deduplicate products
* **Real-time Updates** via automated ingestion + scraping

## Architecture

* **Frontend:** Next.js, React, TypeScript, Tailwind
* **Backend:** Spring Boot, PostgreSQL, Redis, JWT
* **Ingestion:** FastAPI + SQLAlchemy
* **Scrapers:** Python/Node for APIs + web pages
* **Infra:** Docker, Kubernetes, Terraform, Nix

## Dev Setup

```bash
git clone <repo>
docker-compose up -d
```

* App: `localhost:3000`
* API: `localhost:8080`
