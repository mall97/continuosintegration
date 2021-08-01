
#!/bin/sh
echo "teste"
find ../Libraries -type f -exec chmod 744 {} \;
find ../Tests -type f -exec chmod 744 {} \;
python3 ./../Libraries/Serial/serial_server.py
robot ./../Tests/features
echo "teste2"