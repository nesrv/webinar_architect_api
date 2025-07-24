#!/bin/bash
echo "[*] Запуск всех компонентов системы Kafka..."

# Запуск в фоновом режиме с новыми терминалами
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal --title="Kafka Monitor" -- bash -c "./start_monitor.sh; read -p 'Press Enter to close...'"
    sleep 1
    gnome-terminal --title="Kafka Consumer" -- bash -c "./start_consumer.sh; read -p 'Press Enter to close...'"
    sleep 1
    gnome-terminal --title="Kafka Producer" -- bash -c "./start_producer.sh; read -p 'Press Enter to close...'"
elif command -v xterm &> /dev/null; then
    xterm -title "Kafka Monitor" -e "./start_monitor.sh" &
    sleep 1
    xterm -title "Kafka Consumer" -e "./start_consumer.sh" &
    sleep 1
    xterm -title "Kafka Producer" -e "./start_producer.sh" &
else
    echo "Запустите компоненты вручную в отдельных терминалах:"
    echo "./start_monitor.sh"
    echo "./start_consumer.sh"
    echo "./start_producer.sh"
fi

echo "[*] Все компоненты запущены!"