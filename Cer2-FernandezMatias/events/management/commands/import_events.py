import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from events.models import Event

class Command(BaseCommand):
    help = "Importa eventos desde un CSV con columnas: title,description,datetime,location,image,price,capacity"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Ruta al archivo CSV")
        parser.add_argument("--datetime-format", default="%Y-%m-%d %H:%M", help="Formato de fecha y hora (por defecto: %%Y-%%m-%%d %%H:%%M)")

    def handle(self, *args, **opts):
        path = opts["csv_path"]
        fmt = opts["datetime_format"]
        count = 0
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                required = {"title","datetime","location"}
                missing = required - set([c.strip() for c in reader.fieldnames or []])
                if missing:
                    raise CommandError(f"Faltan columnas requeridas en el CSV: {', '.join(sorted(missing))}")
                for row in reader:
                    dt = datetime.strptime(row["datetime"].strip(), fmt)
                    e = Event(
                        title=row["title"].strip(),
                        description=(row.get("description") or "").strip(),
                        datetime=dt,
                        location=row["location"].strip(),
                        price=float((row.get("price") or 0) or 0),
                        capacity=int((row.get("capacity") or 0) or 0),
                    )
                    # Nota: la imagen puede subirse luego por Admin; aquí no movemos archivos
                    e.save()
                    count += 1
        except FileNotFoundError:
            raise CommandError(f"No se encontró el archivo: {path}")
        self.stdout.write(self.style.SUCCESS(f"Importados {count} eventos."))
