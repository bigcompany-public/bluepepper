$ErrorActionPreference = "Stop"

# Get url and token
if (-Not $env:BLUEPEPPER_GIT_URL) {
    throw "Please set the BLUEPEPPER_GIT_URL environment variable to you repository's url"
}
if (-Not $env:BLUEPEPPER_GIT_PAT) {
    throw "Please set the BLUEPEPPER_GIT_PAT environment variable to the Personal Access Token to connect with"
}

# Compose git connection url
$protocol, $_, $website, $user, $repo = $env:BLUEPEPPER_GIT_URL.split("/")

git clone "$protocol//$env:BLUEPEPPER_GIT_PAT@$website/$user/$repo"