FROM rabbitmq:3-management

COPY configure-rabbitmq.sh /configure-rabbitmq.sh
RUN chmod +x /configure-rabbitmq.sh

CMD ["sh", "-c", "rabbitmq-server & /configure-rabbitmq.sh"]

