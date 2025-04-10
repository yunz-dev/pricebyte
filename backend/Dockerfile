FROM openjdk:17-slim

WORKDIR /app

COPY build.gradle settings.gradle ./
COPY gradle gradle
RUN ./gradlew build --no-daemon || true

COPY src src
RUN ./gradlew build --no-daemon -x test

EXPOSE 8080

CMD ["./gradlew", "bootRun", "--no-daemon"]