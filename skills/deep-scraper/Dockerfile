FROM node:20-slim

WORKDIR /usr/src/app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers
RUN npm install -g playwright && \
    playwright install chromium --with-deps

# Copy skill files
COPY package.json .
COPY assets ./assets

RUN npm install crawlee playwright

ENV NODE_ENV=production

CMD ["node", "assets/main_handler.js"]
