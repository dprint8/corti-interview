import pika
import os
from flask import Flask, jsonify
import threading


def send_to_queue(connection, file_path, queue_name='corti'):
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                message = line.strip()
                channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=message,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Make message persistent
                    )
                )
                print(f"Sent to queue: {message}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()


# Flask application for the health check endpoint
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="Consumer is running"), 200

# Function to start Flask health check server
def start_health_check_server():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    input_file = os.getenv('INPUT_FILE', 'input.txt')
    
    # RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    
    # Start the health check server in a separate thread
    health_check_thread = threading.Thread(target=start_health_check_server)
    health_check_thread.daemon = True  # Ensure it terminates when the main thread does
    health_check_thread.start()

    print("Starting producer...")
    send_to_queue(connection, input_file)
    print("All lines sent to queue.")
