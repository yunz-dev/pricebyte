## File Structure
```
backend/
│── src/
│   ├── main/
│   │   ├── java/com/pricebyte/
│   │   │   ├── config/          # Configuration files (CORS, security, etc.)
│   │   │   ├── controllers/     # REST & GraphQL controllers
│   │   │   ├── dto/             # Data Transfer Objects
│   │   │   ├── entities/        # JPA Entities
│   │   │   ├── repositories/    # Spring Data JPA repositories
│   │   │   ├── services/        # Business logic layer
│   │   │   ├── graphql/         # GraphQL resolvers (if using GraphQL)
│   │   │   ├── websocket/       # WebSocket handlers (if needed)
│   │   │   ├── PriceByteApplication.java  # Main entry point
│   │   ├── resources/
│   │   │   ├── application.yml  # Spring Boot config (database, etc.)
│   │   │   ├── schema.sql       # SQL schema (optional)
│   │   │   ├── data.sql         # Seed data (optional)
│   ├── test/                    # Unit and integration tests
│   │   ├── java/com/pricebyte/
│   │   │   ├── controllers/      # Controller tests
│   │   │   ├── services/         # Service layer tests
│   │   │   ├── repositories/     # Repository tests (with @DataJpaTest)
│── pom.xml                       # Maven dependencies
│── Dockerfile                    # Backend containerization
│── README.md
```
