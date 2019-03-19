set -e -x

pip install git+https://github.com/coala/coala.git@master
pip install git+https://github.com/coala/coala-bears.git@master
pip install -r requirements.txt
pip install -r test-requirements.txt
sed -i.bak '/bears = GitCommitBear/d' .coafile
coala --ci -V
python -m pytest
codecov
