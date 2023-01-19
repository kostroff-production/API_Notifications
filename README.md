# TZ_Notifications
### Сервис уведомлений
Сервис осуществляет рассылку писем клиентам по заданным критериям.
Рассылка начнется автоматически как только подойдет ее время, так же присылается отчет на почту администратора о отработанных рассылках.
Сервис рассылки связан внешним API со службой отправки смс оповещений клиентам.
<br>
# Install 
Установите приложение на ваш Linux сервер, предварительно установив на него пакеты:
<br>
```
sudo apt update
sudo apt install libpq-dev
sudo apt-get install python3-psycopg2
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
sudo apt install docker-ce
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Не забываем, что нужно вносить свои данные в `config.yaml` и данные по БД так же должны совпадать с данными в `Docker`.
<br>
Устанавливаем `git` и вытягиваем проект.
<br>
```
apt install git
git init .
git remote add origin git@github.com:kostroff-production/TZ_Notifications.git
git clone https://github.com/kostroff-production/TZ_Notifications.git
```
Делаем сборку с `Docker`.
<br>
```
chmod +x ./entrypoint.sh
docker build .
docker-compose up -d --build
```
