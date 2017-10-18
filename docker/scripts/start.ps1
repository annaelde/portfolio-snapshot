# Start all project containers

$sd = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$pn = Import-CliXml $sd\pn.xml

docker container start $pn"_postgres"
docker container start $pn"_django"
docker container start $pn"_php"
docker container start $pn"_nginx"
