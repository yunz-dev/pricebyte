# 🛍️ PriceByte AI

🛒 **Grocery store aggregator for NSW**

## ✨ Features
- 📊 Compare the market
- 📌 Pinned items (on home page)
- 📝 Shopping list

## 🏗️ Tech Stack
- **🖥️ Frontend**: ReactJS
  - 📱 App-like functionality
  - 🚫 Doesn't really need SSR

- **⚙️ Backend**: Java Spring
  - 💼 Java has the biggest job market share
  - 🌍 Huge Ecosystem
  - 🔍 GraphQL for data queries & REST for other needs
- **Cache**: Redis

- **💾 Database**: PostgreSQL
  - 🆓 Free database with Supabase

- **🔐 Auth**: Supabase
  - 🆓 Free

- **🕷️ Web Scraper**: Python (TBD)
  - ☁️ Probably hosted with Cloudflare Workers
  - 🌩️ OMG DID SOMEONE SAY CLOUD?!

- **🤖 AI Features**: TBD
- **Search**: TBD but probably elastic

- **📊 Logging/Analytics**:
  - ☁️ Cloudflare
  - 📈 Prometheus

## 📅 Plan

### 🗄️ Database
#### 📑 Tables:
- 📦 **Products**
- 🏬 **Stores**
- 💰 **Prices**
- 👤 **Users**

### Iteration 0: MVP
- design future-proof tables
- scrapers for coles + woolies
- basic authentication
- item pages → with price comparison
- basic search
### Iteration 1:
- search with elastic
- Add other stores: Aldi
    - + recursive scraping
### Iteration 2:
- home page
- specials section?
### Iteration 3: AI
- shopping list assistant
- Landing Page
### Somehow do the location stuff
