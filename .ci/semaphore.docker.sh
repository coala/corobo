set -e -x

docker build -t meetmangukiya/corobo .

docker images

docker run --user root meetmangukiya/corobo /bin/sh -c "
    set -e -x
    pip install -r test-requirements.txt
    find -name \"**.pyc\" -delete
    python -m pytest
"

if [[ $BRANCH_NAME == "master" ]]
then echo "pushing..." && docker push meetmangukiya/corobo
fi
