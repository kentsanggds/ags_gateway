# Set CF_HOME in a temp dir so that jobs do not share or overwrite each others' credentials.
export CF_HOME="$(mktemp -d)"
trap 'rm -r $CF_HOME' EXIT

cf api https://api.cloud.service.gov.uk

# Note: the actual name of the environment variable is determined
# by what you enter into the Credentials Binding Plugin
cf auth "$CF_USER" "$CF_PASSWORD"

cf target -o myorg -s myspace
cf push ags-gateway-aws

# Destroy token
cf logout