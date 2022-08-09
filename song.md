## 所依赖包
pip3 install jenkins
pip3 install pymysql
pip3 install flask
pip3 install Flask-BasicAuth
pip3 install functools
pip3 install Flask-Cors
pip3 install Flask-HTTPAuth
pip3 install Flask-Migrate
pip3 install Flask-Script
pip3 install Flask-SQLAlchemy

## 启动服务
进入docker容器 
docker exec  -itu root 容器id /bin/sh

进入目录 /var/jenkins_home/workspace/项目名称

停止服务 
sh app.sh stop

启动服务 
sh app.sh start

查看启动端口
sh app.sh status



