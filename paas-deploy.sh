# Set CF_HOME in a temp dir so that jobs do not share or overwrite each others' credentials.
export CF_HOME="$(mktemp -d)"
trap 'rm -r $CF_HOME' EXIT

APPNAME="ags-gateway-aws"

cf api https://api.cloud.service.gov.uk

# Note: the actual name of the environment variable is determined
# by what you enter into the Credentials Binding Plugin
cf auth "$CF_USER" "$CF_PASSWORD"

cf target -o csd-sso -s sandbox
cf push $APPNAME
cf set-env $APPNAME OIDC_CLIENT_ID "$OIDC_CLIENT_ID"
cf set-env $APPNAME OIDC_CLIENT_SECRET "$OIDC_CLIENT_SECRET"
cf set-env $APPNAME OIDC_CLIENT_ISSUER "$OIDC_CLIENT_ISSUER"
cf set-env $APPNAME SERVER_NAME "$SERVER_NAME"
cf restage $APPNAME

# Destroy token
cf logout