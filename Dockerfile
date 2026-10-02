FROM python:3.12-slim
RUN useradd --create-home --uid 10001 jarvis
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
RUN mkdir -p /app/data /app/.jarvis && chown -R jarvis:jarvis /app
USER 10001
ENV JARVIS_HOST=0.0.0.0
EXPOSE 8080
CMD ["python","-m","jarvis"]
