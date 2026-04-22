# Build stage
FROM node:22-alpine3.21 AS builder

WORKDIR /app

COPY package.json .
RUN npm install --production

# Production stage
FROM node:22-alpine3.21

WORKDIR /app

RUN apk upgrade --no-cache

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/node_modules ./node_modules
COPY app.js .
COPY views ./views

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "app.js"]