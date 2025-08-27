import argparse

from shared.view import View
from data_processing.views import views
from data_ingestion.main import data_ingestion


def prompt_user(message: str, options: list[str]):
    opt = "|".join(options)

    i = None
    while i not in options:
        i = input(f"{message} [{opt}]: ")
        if i not in options:
            message = "Invalid value. Enter one of the options"

    return i


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Command-line utility to run specific tasks for the WeatherDE project."
    )

    parser.add_argument("--run-data-ingestion",
                        help="Run data ingestion pipeline",
                        action="store_true")

    parser.add_argument("--create-views",
                        help='Run "src/data_processing/views.py" script',
                        action="store_true")

    args = parser.parse_args()

    if args.run_data_ingestion:
        data_ingestion()

    if args.create_views:
        v = View()
        for (name, src) in views:
            replace = None
            if v.view_exists(name):
                replace = prompt_user(
                    "View already exists. Replace it?", ["y", "n"]) == "y"
            if replace is not None and not replace:
                continue
            v.create_view(name, src, views[(name, src)], replace)

        print("All views created.")

    if not any(vars(args).values()):
        parser.print_help()
