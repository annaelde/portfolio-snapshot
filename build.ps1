function findReplace([String] $Path, [String] $Find, [String] $Replace)
{
    $content = Get-Content $Path
    $content = $content.replace($Find, $Replace)
    Set-Content -Path $Path -Value $content
}

# Compile all the source
npm run prod

# Create/overwrite build folder
New-Item -ItemType "directory" -Path "." -Name "build" -Force 

# Populate with directories
New-Item -ItemType "directory" -Path "./build" -Name "project" -Force 
New-Item -ItemType "directory" -Path "./build" -Name "assets" -Force 
New-Item -ItemType "directory" -Path "./build" -Name "config" -Force 

# Copy site to project folder
Copy-Item "./site/*" -Destination "./build/project" -Recurse

# Clean up project folder
if (Test-Path "./build/project/temp/cache"){ Remove-Item "./build/project/temp/cache" -Recurse }
if (Test-Path "./build/project/temp/email"){ Remove-Item "./build/project/temp/email" -Recurse }

# Remove unused settings
Remove-Item "./build/project/settings/development.json"
Remove-Item "./build/project/settings/development.py"

# Set the correct settings state
findReplace -Path "./build/project/manage.py" -Find "settings.development" -Replace "settings.production"
findReplace -Path "./build/project/aec/wsgi.py" -Find "settings.development" -Replace "settings.production"

# Move and cleanup static folder
Move-Item -Path "./build/project/static" -Destination "./build/assets/"
Move-Item -Path "./build/assets/static/maintenance.html" -Destination "./build/assets/"
Move-Item -Path "./build/assets/static/favicon.ico" -Destination "./build/assets/"

# Dump the DB
docker exec -d aec_postgres bash -c "pg_dump --username=anna --format=c --file=/db/build.bak aec" | Out-Null

# Add projects to assets
git clone https://github.com/annaelde/rain-city.git ./build/assets/rain-city
git clone https://github.com/annaelde/desert-time.git ./build/assets/desert-time
git clone https://github.com/annaelde/hazel-glen.git ./build/assets/hazel-glen

# Clean up projects
Remove-Item "./build/assets/hazel-glen/.git" -Recurse -Force
Remove-Item "./build/assets/desert-time/.git" -Recurse -Force
Remove-Item "./build/assets/rain-city/.git" -Recurse -Force

# Move media folder
Move-Item -Path "./build/project/media" -Destination "./build/assets/"

# Optimize images
$staticImages = Get-ChildItem -Path "./build/assets/static/images" -Include *.gif, *.jpg, *.jpeg, *.png -Recurse
foreach ($image in $staticImages)
{
    $path = (Split-Path -Path $image.FullName)
    $cmd = "imagemin $($image.FullName) --out-dir=$path"
    Invoke-Expression $cmd
}

$mediaImages = Get-ChildItem -Path "./build/assets/media/images" -Include *.gif, *.jpg, *.jpeg, *.png -Recurse
foreach ($image in $mediaImages)
{   
    $path = (Split-Path -Path $image.FullName)
    $cmd = "imagemin $($image.FullName) --out-dir=$path"
    Invoke-Expression $cmd
}

# Copy config files
Copy-Item "./docker/requirements.pip" -Destination "./build/config"
Copy-Item "./config/prod/anna.elde.codes" -Destination "./build/config"
Copy-Item "./config/prod/gunicorn.service" -Destination "./build/config"

# Copy DB to config
Move-Item -Path "./docker/db/build.bak" -Destination "./build/config"

# Housekeeping: delete all empty folders
do {
  $dirs = Get-ChildItem "./build/" -Directory -Recurse | Where { (Get-ChildItem $_.fullName).count -eq 0 } | Select -ExpandProperty FullName
  $dirs | Foreach-Object { Remove-Item $_ }
} while ($dirs.count -gt 0)

# Compress to .zip
Compress-Archive -Path "./build/*" -CompressionLevel Optimal -DestinationPath "./build.zip" -Force

# Remove build folder
Remove-Item "./build" -Recurse -Force

# Upload build and build script to the server
scp ./build.zip elde.codes:/web/aec/
scp ./config/prod/build.py elde.codes:/web/aec/