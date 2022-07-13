"""
Entry point for the application


"""
from logger import console
from extract import main
from load.main import Loader


from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress,track

# --------------------------------------------

# Create a welcome banner with a welcome message
banner_message = "Extract Crash Data from NYC Open Data\n\nETL Script"
console.print(Panel(banner_message), style="bold green")

# --------------------------------------------

chosen_datasets = set()
choices = [
        "crashes",
        "vehicles",
        "people"
]

while choices:
    dataset = Prompt.ask(
        'Choose a dataset which to extract:\n',
        choices = choices,
        default=choices[0]
    )

    chosen_datasets.add(dataset)
    choices.remove(dataset)

    console.log(
        f"You've chosen to extract the following datasets:"
        f"[bold magenta]'{list(chosen_datasets)}'[/bold magenta]."
    )

    if choices:
        again = Confirm.ask(
            "Would you like to select an additional dataset?",
            default=False
        )
        if not again:
            break


# One last time
console.log(
    f"You've chosen to extract the following datasets:"
    f"[bold magenta]'{list(chosen_datasets)}'[/bold magenta]."
)


if __name__ =='__main__':

    # Eventually, will allow all sources
    for key in chosen_datasets:

        proceed_extract = Confirm.ask(
            f"Would you like to [red]EXTRACT[/red] data for dataset={key}?",
            default=False
        )

        if proceed_extract:
            
            # Extract
            records = main.extract_data(key)

            # Save locally, a bit extra IO, but helps if
            # you want to break into discrete steps
            console.log('Proceeding to save data (locally)')
            main.save_data(key, records)


        console.log('Proceeding to load data into the DB')
        # Load the data into the DB
        loader = Loader()
        loader.load_data(key)

        console.log(f'Done loading data into the DB for dataset={key}', style="bold green")
