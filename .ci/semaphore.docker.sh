set -e -x

docker build -t meetmangukiya/corobo .
.ci/semaphore.answers.sh

docker images

docker run --user root meetmangukiya/corobo /bin/sh -c "
    set -e -x
    pip install -r test-requirements.txt
    find -name \"**.pyc\" -delete
    python -m pytest
"

if [[ $BRANCH_NAME == "master" && $SEMAPHORE_REPO_SLUG == "coala/corobo"  ]]
then echo "pushing..." && docker push meetmangukiya/corobo && docker push meetmangukiya/corobo-answers
fi
