# NYC Open Data – Vehicle Collisions
> _This project About allows you to ETL a public dataset to a postgres DB._

# Motor Vehicle Collisions - Crashes
he Motor Vehicle Collisions crash table contains details on the crash event.
Each row represents a crash event. The Motor Vehicle Collisions data tables
contain information from all police reported motor vehicle collisions in NYC.
The police report ([MV104-AN](https://www.nhtsa.gov/sites/nhtsa.dot.gov/files/documents/ny_overlay_mv-104an_rev05_2004.pdf))
is required to be filled out for collisions where someone is injured or
killed, or where there is at least $1000 worth of damage.

## Motor Vehicle Collisions - Vehicles
The Motor Vehicle Collisions vehicle table contains details on each vehicle
involved in the crash. Each row represents a motor vehicle involved in
a crash. The data in this table goes back to April 2016 when crash reporting
switched to an electronic system.


----

## Assignment:
* Choose a public dataset that is of interest to you.
* Write ETL code in Python to load this data into a DB of your choice on
your local machine.  MySQL, SQLite, or Postgres are suitable for this task.
* Write a few interesting SQL queries to present some analysis of the data.

### The ETL code should:
* Perform some validation, cleaning, filtering and transformations based upon
some realistic rules that you define.
* A short write-up about these rules would be appreciated and illustrate your
understanding of the process.
* Use a performant methodology, e.g. COPY vs INSERT for loading the
raw data into the database.
* Make it possible to re-run the process without duplicating data and with
minimal impact to hypothetical live queries running on the already loaded data.
* Provide clear feedback in the case of an error without negatively impacting
the hypothetical live queries against the previously loaded version of the data.

### Extra credit for:
* Use of visualizations to present the data with charts
* Collection of metrics about the performance of the ETL itself
