set -e -x

pip install coala-bears
pip install -r requirements.txt
pip install -r test-requirements.txt
sed -i.bak '/bears = GitCommitBear/d' .coafile
coala --ci -V
python -m pytest
codecov
