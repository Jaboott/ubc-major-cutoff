## UBC Major Cutoff Poller

A poller to monitor updates to the [UBC Major Cutoff Spreadsheet](https://docs.google.com/spreadsheets/d/1WkMPGKerBEms560QiMY4v8BmapBitMqwq9lTmzoSJPo/edit), parse its contents, and update the database whenever changes are detected.

## Running Locally
You can test this poller locally using a Python entry point. For example, run: 

`python -c "import src.polling.poller; src.polling.poller.poll()"`