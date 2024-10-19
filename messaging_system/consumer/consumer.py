import pika
import os
import threading
from flask import Flask, jsonify
from prometheus_client import start_http_server, Summary, Gauge

# Function to consume messages from RabbitMQ
def consume_from_queue(connection, output_file, queue_name='corti'):
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        with open(output_file, 'a') as file:
            file.write(message + '\n')
            print(f"Written to file: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print('Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()
    

# Flask application for the health check endpoint
app = Flask(__name__)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
health_gauge = Gauge('producer_health', 'Health of the producer', ['status'])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="Consumer is running"), 200

@app.route('/metrics')
def metrics():
    # Expose Prometheus metrics
    return generate_latest()

# Function to start Flask health check server
def start_health_check_server():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    output_file = os.getenv('OUTPUT_FILE', 'output.txt')

    # RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))

    # Start the health check server in a separate thread
    health_check_thread = threading.Thread(target=start_health_check_server)
    health_check_thread.daemon = True  # Ensure it terminates when the main thread does
    health_check_thread.start()

    # Start consuming messages from the queue
    print("Starting consumer...")
    consume_from_queue(connection, output_file)
