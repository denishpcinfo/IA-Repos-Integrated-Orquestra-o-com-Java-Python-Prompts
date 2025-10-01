FROM eclipse-temurin:17-jre
WORKDIR /app
COPY target/semantic-kernel-java-bank-0.0.2.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
