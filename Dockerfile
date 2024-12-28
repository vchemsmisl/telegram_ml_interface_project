FROM python:3.12
WORKDIR /telegram_ml_interface_project_image

COPY requirements.txt requirements.txt
COPY main.py main.py

COPY messages.py messages.py
COPY constants.py constants.py

COPY src/database.py src/database.py
COPY src/facade.py src/facade.py
COPY src/model.py src/model.py
COPY src/tgbot.py src/tgbot.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]