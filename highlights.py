import logging
import sys
import requests
from config import config
from bs4 import BeautifulSoup
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
import json

def fetch_live_match_ids():
    url = "https://m.cricbuzz.com/cricket-match/live-scores"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find( id='international-matches').find_all('a')
    match_ids = []
    for match_id in content:
        match_ids.append(match_id['href'].split('/')[-2])
    print(match_ids) 
    return match_ids
def get_summary(id:int):
    url = "https://m.cricbuzz.com/cricket-commentary/"+str(id)+"/god"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    #response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', class_='col-xs-9 col-lg-9 dis-inline')
    return (content.get_text())
def get_highlights(id:int):
    url = "https://m.cricbuzz.com/cricket-match-highlights/"+str(id)+"/god"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    #response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', class_='list-content')
    if not content== None:

        return (content.get_text())
    return 'no highlights'    




def main():
    logging.info('START')
    def acked(err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))
   
    matches= fetch_live_match_ids()
    schema_registry_client = SchemaRegistryClient(config["schema_registry"])
    match_highlights_value_schema = schema_registry_client.get_latest_version("match_highlights-value")
    kafka_config = config["kafka"] 
    additional_config ={
        "key.serializer": StringSerializer(),
        "value.serializer": AvroSerializer(
            schema_registry_client,
            match_highlights_value_schema.schema.schema_str,
        ),
    }
    kafka_config.update(additional_config)
    
    producer = SerializingProducer(kafka_config) 
    for match_id in matches:
        if matches.count(match_id) == 2:
            message =f"{get_highlights(match_id)} {get_summary(match_id)}"
            print(message)
            #(get_highlights(match_id)+"/n"+ get_summary(match_id))
            producer.produce(topic = 'match_highlights',key = match_id,  value={
                    "TITLE": match_id,
                    
                    "HIGHLIGHTS": message,
                },
                on_delivery=acked,)

    producer.flush()       
    producer.poll(1)
    #response = requests.get('https://m.cricbuzz.com/api/cricket-highlights/68077/1')
    #logging.info('%s',response.text)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())

