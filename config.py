from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
config = {
    
    "kafka": {
        'bootstrap.servers':'xxxxxx',
        'security.protocol':'SASL_SSL',
        'sasl.mechanisms':'PLAIN',
        'sasl.username':'xxxxxxxx',
        'sasl.password':'xxxxxxxxxxxx',
        
    },
    "schema_registry": {
        "url": "xxxxxxxxxx",
        "basic.auth.user.info": "xxxxxxxxx",
    }
}