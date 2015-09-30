if [ ! -d "mcom-tests" ]
then
    git clone https://github.com/mozilla/mcom-tests/;
fi;

if [ ! -d "venv" ];
then
    virtualenv venv;
fi;

. venv/bin/activate

cd mcom-tests/

git fetch origin
git reset --hard origin/master

pip install -r requirements.txt
pip install pytest-xdist

SAUCE_CREDENTIALS_PATH=`mktemp`
cat << EOF > $SAUCE_CREDENTIALS_PATH
username: $SAUCELABS_USERNAME
password: $SAUCELABS_PASSWORD
api-key: $SAUCELABS_API_KEY
EOF

py.test -r=fsxXR --verbose -n 15 \
        --baseurl=${BASE_URL} \
        --browsername="${BROWSER_NAME}" \
        --browserver=${BROWSER_VERSION} \
        --platform="${PLATFORM}" \
        --junitxml=results.xml \
        --saucelabs=${SAUCE_CREDENTIALS_PATH} \
        --capability="selenium-version:${SELENIUM_VERSION}" \
        --build=${BUILD_TAG} \
        tests
