# Contributing to PriceByte

Welcome to **PriceByte**, the grocery price comparison app! 🎉 We appreciate your interest in contributing. This guide will help you understand how to get started and maintain high-quality contributions.

---

## 🛠 Project Workflow

PriceByte follows a structured workflow to ensure code quality and maintainability.

### 1️⃣ **Branching Strategy**

We use the **Git Feature Branch Workflow**:

- `main` → Stable production-ready branch.
- `develop` → Active development branch.
- `feature/<feature-name>` → Feature branches for new features.
- `doc/<doc-description>` → Branch to add documentation
- `bugfix/<bug-description>` → Fixes for existing issues.
- `hotfix/<critical-fix>` → Immediate fixes for production issues.

**Workflow:**

1. Create a new branch from `develop`:
   ```sh
   git checkout develop
   git pull origin develop
   git checkout -b feature/<feature-name>
   ```
2. Commit changes following [conventional commits](https://www.conventionalcommits.org/).
3. Push to remote:
   ```sh
   git push origin feature/<feature-name>
   ```
4. Open a **Pull Request (PR)** to `develop`.
5. Get a code review and merge if approved.
6. After all features are merged, `develop` is merged into `main` for a new release.

---

## 🧪 Test-Driven Development (TDD) in PriceByte

We follow **TDD** to ensure robust, reliable code. All contributions should include relevant tests.

### **Backend (Spring Boot + PostgreSQL)**

#### Running Tests

To run unit and integration tests:

```sh
./mvnw test
```

#### Writing Tests

- Use **JUnit 5** for unit tests.
- Use **Mockito** for mocking dependencies.
- Use **Testcontainers** for database integration testing.

Example Unit Test (JUnit + Mockito):

```java
@Test
void shouldReturnProductWhenFound() {
    Product mockProduct = new Product(1L, "Milk", 2.99);
    when(productService.getProductById(1L)).thenReturn(Optional.of(mockProduct));

    ResponseEntity<Product> response = productController.getProductById(1L);

    assertEquals(HttpStatus.OK, response.getStatusCode());
    assertEquals(mockProduct, response.getBody());
}
```

---

### **Frontend (React + TypeScript)**

#### Running Tests

To run unit tests:

```sh
npm test
```

#### Writing Tests

- Use **Jest** for unit tests.
- Use **React Testing Library** for component testing.
- Use **MSW (Mock Service Worker)** for API testing.

Example Unit Test (Jest + React Testing Library):

```tsx
test('renders product list', async () => {
  render(<ProductList />);
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  await waitFor(() => expect(screen.getByText(/Milk/i)).toBeInTheDocument());
});
```

---

## 🚀 Getting Started

### **Backend Setup (Spring Boot + PostgreSQL)**

1. Clone the repository:
   ```sh
   git clone https://github.com/yunz-dev/pricebyte.git
   cd pricebyte/backend
   ```
2. Create a `.env` file and configure database credentials.
3. Start PostgreSQL and run the backend:
   ```sh
   ./mvnw spring-boot:run
   ```
4. API will be available at `http://localhost:8080`.

### **Frontend Setup (React + TypeScript)**

1. Navigate to the frontend folder:
   ```sh
   cd pricebyte/frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```
4. App will be available at `http://localhost:3000`.

---

## 📝 Code Style Guidelines

- **Backend:** Follow Java's standard formatting (`google-java-format`).
- **Frontend:** Follow Prettier + ESLint (`npm run lint`).
- Keep functions small and modular.
- Use meaningful variable and function names.

---

## 🎯 How to Contribute

1. **Find an issue:** Check [Issues](https://github.com/your-repo/pricebyte/issues) and pick one.
2. **Discuss:** Comment on the issue to get assigned.
3. **Develop:** Follow the workflow and submit a PR to the **developement** branch.
4. **Code Review:** Respond to feedback and get your PR merged by a maintainer:
- [@Yunz](https://github.com/yunz-dev)
- [@VictorNguyen0702](https://github.com/VictorNguyen0702)
- [@MonkieeBoi](https://github.com/MonkieeBoi)

---

## 🎉 Thank You!

Your contributions make PriceByte better! Feel free to reach out with any questions. 🚀
