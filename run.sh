#!/bin/zsh

python ./microservices/middleware/initialize_db.py &
python ./microservices/Users_service/initialize_db.py &
python ./microservices/Visitors_validation/initialize_db.py &