# Build stage
FROM node:18-alpine3.20 AS builder

WORKDIR /app

COPY package.json .
RUN npm install --production

# Production stage
FROM node:18-alpine3.20

WORKDIR /app

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