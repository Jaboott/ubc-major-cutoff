## UBC Major Cutoff Poller

A poller to monitor updates to the [UBC Major Cutoff Spreadsheet](https://docs.google.com/spreadsheets/d/1WkMPGKerBEms560QiMY4v8BmapBitMqwq9lTmzoSJPo/edit), parse its contents, and update the database whenever changes are detected.

## Configuration
Create a file named .env at the root of the project with the following variables:

```
DOCUMENT_URL="https://docs.google.com/spreadsheets/d/1WkMPGKerBEms560QiMY4v8BmapBitMqwq9lTmzoSJPo/export?gid=0&format=csv"
DB_USER="your_database_user"
DB_PASSWORD="your_database_password"
DB_HOST="your_database_host"
DB_PORT="your_database_port"
DB_NAME="your_database_name"
```

## Running Locally
You can test this poller locally using a Python entry point. For example, run: 

`python -c "import src.polling.poller; src.polling.poller.poll()"`