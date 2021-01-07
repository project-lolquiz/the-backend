############################################################
######### Run this script with . ./run.sh command ##########
############################################################

# Running docker-compose
sudo docker-compose down
sudo docker-compose up -d --remove-orphans

# Setting environment variables
export REDIS_PASSWORD=Acesso01!
export ENV=dev
export DATABASE_URL=postgresql://postgres@localhost:5432/lolquiz

echo 'Waiting containers to be up running...'
sleep 10s

# Running scripts into database
echo 'Running migrations'
cat ./migrations/*.sql | docker exec -i the-backend_thedb_1 psql -U postgres -d lolquiz

echo 'Infrastructure OK'

source venv/bin/activate
pip install -r requirements.txt
python main.py