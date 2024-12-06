FROM mcr.microsoft.com/mssql/server:2022-latest

USER root
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

USER mssql
