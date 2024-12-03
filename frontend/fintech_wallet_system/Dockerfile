# Step 1: Build the React app
FROM node:18
# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build:prod

# Serve the app using serve
RUN npm install -g serve

# Command to run the app
CMD ["serve", "-s", "build"]

# Expose the port the app runs on
EXPOSE 3000
