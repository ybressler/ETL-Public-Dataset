# NYC Open Data – Vehicle Collisions
> _This project About allows you to ETL NYC Vehicle Collision data into a local postgres database._

# Running this program
_Here's what you need to do to get this to work._
1. Clone this repository to your local machine.
2. Navigate to the directory of this project and create a new virtual environment
```bash
python3 -m venv venv
```
3. Activate the virtual environment and install required dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```
4. Create an APP token (similar to API token) which will be used to
get data from the NYC Open Data API:

  a. Create a [NYC Open Data Account](https://data.cityofnewyork.us/login)

  b. Click `edit Your Profile`

  c. Navigate to `Developer Settings`

  d. Create a new App Token

  e. Choose arbitrary values for each of the parameters they ask,
    this is for your bookeeping.

  f. Note the `App Token` and `Secret Token`, you will need these
  in step 6.

5. Create a local postgres database for the ETL program.

  a. Can be any configuration you'd like. I will recommend
  creating a new DB under the port `5430`.

  b. (Optional) Once instantiated, create a new `database`
    object named `db`. The application is smart enough to
    create a new db object if `db` doesn't exist, but you
    may choose to err on the side of caution here.

  c. No need to worry about schema, the application
    is smart enough to figure out how to proceed without it.


6. Create required secrets:

    a. Create a file `secrets/local.ini`
    b. Add the following to that file:
    ```
    [nyc_open_data]
    APP_TOKEN=******
    APP_SECRET_TOKEN=******

    [database]
    DB_URI=postgresql://postgres:@localhost:5430/db
    ```

7. There is a quirk when running migrations, you will need to help the
migrations manager find your program. Export the current working directory
to an environment variable `PROJECT_PATH`:
```bash
export PROJECT_PATH="$PWD"
```

8. Run migration manager (this will create all tables defined in
[`database.models`](database/models)):
```bash
bash database/migrations_manager/run_alembic.sh -m "first migration" -u -r
```
> For more details on how this works: [database/migrations_manager](database/migrations_manager/readMe.md)

9. You are now ready to run the extract service! Execute the main executable
and follow the prompts. (The program is kind of smart enough not to do the
same work twice, but it's not 100%, so more work needed to be done there.)
```bash
python3 main.py
```
> Note: Currently, only `crashes` dataset is supported for loading into the
database. Future work will be done to include other datasets. You can, however,
download this data (into properly transformed json records) locally. Perfect
for a NoSql DB. But not yet ready for a RDBMS.

10. You can now query your database from your database! Hoorah!

---
# About the Data
Relevant resources:
  * [Pydantic Models](models/)
  * [ORM Models](database/models/)

### Motor Vehicle Collisions - Crashes
The Motor Vehicle Collisions crash table contains details on the crash event.
Each row represents a crash event. The Motor Vehicle Collisions data tables
contain information from all police reported motor vehicle collisions in NYC.
The police report ([MV104-AN](https://www.nhtsa.gov/sites/nhtsa.dot.gov/files/documents/ny_overlay_mv-104an_rev05_2004.pdf))
is required to be filled out for collisions where someone is injured or
killed, or where there is at least $1000 worth of damage.


### Motor Vehicle Collisions - Vehicles
The Motor Vehicle Collisions vehicle table contains details on each vehicle
involved in the crash. Each row represents a motor vehicle involved in
a crash. The data in this table goes back to April 2016 when crash reporting
switched to an electronic system.

### Motor Vehicle Collisions - Person
The Motor Vehicle Collisions person table contains details for people
involved in the crash. Each row represents a person (driver, occupant,
pedestrian, bicyclist,..) involved in a crash. The data in this table
goes back to April 2016 when crash reporting switched to an electronic system.


### Additional Info:
Check out other cool open datasets available on
[NYC Open Data](https://data.cityofnewyork.us/browse?limitTo=datasets&q=).
----
