Apologies for the bad quality - I spent far too much time on setting up my local environment and then got lost in chatgpt.

- To run locally and test:
1) cd into rabbitmq and run docker compose up - navigate to localhost:<rabbitmq_port> to see the UI
2) cd into producer
3) Create & activate python virtual env: `python3 -m venv venv` then `source venv/bin/activate`
4) Install requirements: `pip install -r requirements.txt`
5) Run producer: `python producer.py` - you can see the queue has now two records
6) cd into consumer
7) Install requirements: `pip install -r requirements.txt`
8) Run consumer: `python consumer.py` - you can see the output.txt created

# Building docker images
In each of the consumer/producer run `docker build -t <app_name>:0.1.0`
Note: I think I've missed exposing ports on the containers correctly in the dockerfile.

# Running in local kubernetes cluster
To create all of the resources cd into kubernetes and `kubectl apply -f .`

To go to prometheus from local you need to port forward:
`kubectl port-forward svc/prometheus 9090:9090`

Notes
- I have not included tests - I have not done tdd so did not cheat more.
- Prometheus is not scraping correctly - probably due to my above note in the buulding docker images section.

