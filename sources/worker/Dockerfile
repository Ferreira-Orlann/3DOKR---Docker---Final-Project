
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build

WORKDIR /worker

COPY ./worker/*.csproj ./worker/

RUN dotnet restore ./worker

COPY ./worker ./worker


WORKDIR /app/worker
RUN dotnet publish -c Release --self-contained=false --no-restore -o /app/publish

FROM mcr.microsoft.com/dotnet/runtime:7.0

WORKDIR /app

COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "Worker.dll"]
