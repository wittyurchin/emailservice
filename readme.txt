Step1:-Install RabbitMq
    sudo apt-get install rabbitmq-server

Start RabbitMq
For ubuntu 14.04
    sudo service rabbitmq-server start
    sudo service rabbitmq-server stop
    sudo service rabbitmq-server status
For systems with systemctl
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server
    sudo systemctl stop rabbitmq-server


Step2:-Start celery(from project directory)
    celery -A artivatic worker -B -l info