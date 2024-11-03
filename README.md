# HighlightHawk

This project is a work in progress that aims to monitor live cricket matches for new highlights and deliver real-time notifications via Telegram. I used web scraping to gather data from Cricbuzz and Apache Kafka for data streaming and KSQL for stream processing.

## Inspiration and Adaptation
The project takes inspiration from a YouTube tutorial https://youtu.be/jItIQ-UvFI4?si=RPRWuIg9b5N93brB that demonstrates building a data pipeline to monitor YouTube comments and send alerts through Telegram. This project adapts that concept by:

* **Focusing on cricket highlights**: Instead of monitoring YouTube comments, this project targets Cricbuzz as a data source to capture real-time updates on cricket match highlights.
* **Utilizing web scraping**: Unlike the YouTube tutorial's reliance on an API, this project employs web scraping techniques using Python and BeautifulSoup to extract data from Cricbuzz web pages.

## Project Components

1. **Web Scraping (highlights/highlights.py)**:
    * **Fetching Live Match IDs**: The `fetch_live_match_ids()` function scrapes the Cricbuzz website to identify currently active matches and extracts their unique IDs .
    * **Extracting Highlights and Summaries**: The `get_highlights()` and `get_summary()` functions retrieve the latest highlights and match summaries for each identified match ID .

2. **Data Streaming with Kafka**:
    * **Kafka Producer**: The Python script utilizes a Kafka producer to send the extracted match data (ID, highlights, summary) to a Kafka topic named 'match_highlights' .

3. **Stream Processing with KSQL**:
    * **KSQL Statements**: Used confluent cloud for kafka cluster and ksql.The KSQL code defines streams and tables to manage the incoming cricket data . It creates:
        * `match_highlights_stream`: A stream to monitor the raw data from the 'match_highlights' topic.
        * `latest_highlights`: A table to store the most recent highlights for each match, using `LATEST_BY_OFFSET` to track changes .
        * `highlights_changes_stream`: A stream that captures any changes in the `latest_highlights` table, effectively providing a stream of updates on new highlights .

4. **Alerting System (Partially Implemented)**:
    * **Telegram Outbox**: Defined a stream named `telegram_outbox` intended to hold messages ready for delivery to Telegram .
    * **Message Formatting**: prepared messages for Telegram, including the match title and the latest highlight .
    * **Missing Connector**: Currently, this project lacks the Kafka connector needed to bridge the `telegram_outbox` stream with the Telegram API. This connector would be responsible for sending the formatted messages from Kafka to Telegram, completing the notification delivery process.

 

