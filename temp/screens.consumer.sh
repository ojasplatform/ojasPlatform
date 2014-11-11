#!/bin/sh
bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic mytopic --from-beginning
