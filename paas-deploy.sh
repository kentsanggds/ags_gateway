# Set CF_HOME in a temp dir so that jobs do not share or overwrite each others' credentials.
export CF_HOME="$(mktemp -d)"
trap 'rm -r $CF_HOME' EXIT

APPNAME="ags-gateway-aws"

cf api https://api.cloud.service.gov.uk

# Note: the actual name of the environment variable is determined
# by what you enter into the Credentials Binding Plugin
cf auth "$CF_USER" "$CF_PASSWORD"

cf target -o csd-sso -s sandbox

echo '  env:' >> manifest.yml
echo '      OIDC_CLIENT_ID: '$OIDC_CLIENT_ID >> manifest.yml
echo '      OIDC_CLIENT_SECRET: '$OIDC_CLIENT_SECRET >> manifest.yml
echo '      OIDC_CLIENT_ISSUER: '$OIDC_CLIENT_ISSUER >> manifest.yml
echo '      SERVER_NAME: '$SERVER_NAME >> manifest.yml

cf push $CF_APPNAME

# remove the env block in case it gets pushed again using this script 
# without destroying the app
head -n 4 manifest.yml > temp.yml ; mv temp.yml manifest.yml

# Destroy token
cf logout