export CHART_URL=oci://registry-1.docker.io/arizephoenix/phoenix-helm
export CHART_VERSION="4.0.14" 
helm upgrade --install phoenix $CHART_URL --version $CHART_VERSION