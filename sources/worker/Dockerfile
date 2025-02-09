
FROM mcr.microsoft.com/dotnet/sdk:7.0-alpine@sha256:1478c99b4bed8d297ccd000e0fdaf060cdfb281779f8c8aa47f031a09503c0d4 AS restore
WORKDIR /tmp/build

# Copy project file separately to take advantage of Docker layer caching
COPY Worker.csproj ./
# Restore dependencies without copying the entire project
RUN dotnet restore

FROM restore AS build
WORKDIR /tmp/build

COPY . .

# Compile and publish the application in Release mode
RUN dotnet publish -c Release -o /app/out --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:7.0-alpine@sha256:4328f4d60da5d18ca8d3ba816f58a3a4e521e614728c7b6e36f96cfc09a68004 AS runtime
WORKDIR /app

# Install dumb-init for proper signal handling and process management
RUN apk add --no-cache dumb-init

# Create a non-root user for security
RUN addgroup -S appgroup && adduser --disabled-password -S appuser -G appgroup
USER appuser

# Copy only the published application from the build stage
COPY --from=build /app/out .

ENTRYPOINT [ "dumb-init", "dotnet", "Worker.dll" ]