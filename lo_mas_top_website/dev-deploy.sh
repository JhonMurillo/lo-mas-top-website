echo "Installing virtual env Lo Mas Top..."
python3 -m venv lo_mas_top_website
echo "Activate Virtual Env for: " $OSTYPE "..."

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    source lo_mas_top_website/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
    source lo_mas_top_website/bin/activate
elif [[ "$OSTYPE" == "cygwin" ]]; then
    /lo_mas_top_website/Scripts/activate
elif [[ "$OSTYPE" == "msys" ]]; then
    /lo_mas_top_website/Scripts/activate
elif [[ "$OSTYPE" == "win32" ]]; then
    /lo_mas_top_website/Scripts/activate
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    /lo_mas_top_website/Scripts/activate
else
    /lo_mas_top_website/Scripts/activate
fi

echo "Installing requirements..."
pip install -r requirements.txt

echo "Making migrations..."
python manage.py makemigrations

echo "Migrating..."
python manage.py migrate

echo "Deploy server..."
python manage.py runserver