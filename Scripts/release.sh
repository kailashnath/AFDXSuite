MAJOR_VERSION=$1
version=$(date +$1.%m.%d)

git diff
git archive -o Interoperability_Linux_$version.zip HEAD

