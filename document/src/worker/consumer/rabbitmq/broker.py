from src.worker.depends.rabbitmq_depend import broker_client_depend

client = broker_client_depend()

subscriber = client.broker.subscriber(
    queue=client.queue,
    exchange=client.exchange,
)