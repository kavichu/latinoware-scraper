# latinoware-scraper
[master](https://codeship.com/projects/186925/status?branch=master)
[develop](https://codeship.com/projects/186925/status?branch=develop)

# kubectl --namespace latinoware-io scale deployment latinoware-scraper --replicas=10
# kubectl rolling-update latinoware-scraper -f deployment.yaml
# kubectl set image deployment/latinoware-scraper lati=nginx:1.9.1