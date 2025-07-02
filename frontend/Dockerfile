FROM node:20-alpine

WORKDIR /app

# Copy package files first
COPY package.json ./

# Install dependencies (will create yarn.lock if missing)
RUN yarn install

# Copy configuration files
COPY tailwind.config.js postcss.config.js vite.config.ts tsconfig.json tsconfig.node.json ./

# Copy source files
COPY src/ ./src/
COPY index.html ./

# Copy the entrypoint script
COPY frontend-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/frontend-entrypoint.sh

EXPOSE 5173

ENTRYPOINT ["frontend-entrypoint.sh"]
CMD ["yarn", "dev"]
