pip install gitpython
.ci/check_docker.py
if [[ $? == 1 ]]
then docker pull meetmangukiya/corobo-answers:latest && \
     docker build -t meetmangukiya/corobo-answers answers/
fi
