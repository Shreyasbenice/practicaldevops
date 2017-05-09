import requests, json
import atexit
from . import app

from kafka import KafkaProducer
from kafka.errors import KafkaError
import ssl

sasl_mechanism = 'PLAIN'
security_protocol = 'SASL_SSL'

# Create a new context using system defaults, disable all but TLS1.2
context = ssl.create_default_context()
context.options &= ssl.OP_NO_TLSv1
context.options &= ssl.OP_NO_TLSv1_1

producer = KafkaProducer(bootstrap_servers = app.config['KAFKA_BROKERS_SASL'],
                         sasl_plain_username = app.config['KAFKA_USERNAME'],
                         sasl_plain_password = app.config['KAFKA_PASSWORD'],
                         security_protocol = security_protocol,
                         ssl_context = context,
                         sasl_mechanism = sasl_mechanism,
                         api_version = (0,10))

def create_topic():
    import requests
    import json
    
    data = { 'name' : app.config['KAFKA_TOPIC'] }
    headers = {
        'content-type': 'application/json',
        'X-Auth-Token' : app.config['KAFKA_API_KEY'] 
    }
    url = app.config['KAFKA_ADMIN_URL'] + '/admin/topics'

    # TODO check for topic before creating - only create if required

    # create the topic (http POST)
    response = requests.post(url, headers = headers, data = json.dumps(data))

    # verify the topic was created (http GET)
    response = requests.get(url, headers = headers, data = json.dumps(data))
    print (response.text)


def send_message(message):

    producer.send(app.config['KAFKA_TOPIC'], message.encode('utf-8'))
    # producer.flush()


create_topic()

@atexit.register
def python_shutting_down():
    print('Disconnecting MessageHub client')
    # TODO



