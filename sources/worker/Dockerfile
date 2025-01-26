FROM mcr.microsoft.com/dotnet/sdk:7.0-alpine@sha256:1478c99b4bed8d297ccd000e0fdaf060cdfb281779f8c8aa47f031a09503c0d4 AS restore
WORKDIR /tmp/build
COPY . .
RUN dotnet restore

FROM restore AS build
WORKDIR /tmp/build
COPY . .
RUN dotnet publish -o output Worker.csproj

FROM mcr.microsoft.com/dotnet/aspnet:7.0-alpine@sha256:4328f4d60da5d18ca8d3ba816f58a3a4e521e614728c7b6e36f96cfc09a68004 AS runtime
WORKDIR /app
COPY --from=build /tmp/build/output .
ENTRYPOINT [ "dotnet", "Worker.dll"]