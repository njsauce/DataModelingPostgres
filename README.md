<h6>Purpose</h6>
The purpose of this database was to enable the analytics team at Sparkify to gain insight into what their customers were listening to. They needed a database that was designed to optimize queries on song play analysis. 

<h6>How to run</h6>
<ol>
  <li>Place the *create_tables.py* and the *etl.py* files in the same folder location</li>
  <li>Place the *Data folder* and the *sql_queries.py* file in the same location as step 2</li>
  <li>Run the *create_tables.py* file in the python console of your choice</li>
  <li>Run the *etl.py* file in the python console of your choice</li>
</ol>

<h6>File explanation</h6>
<ul>
  <li>*create_tables.py* - This python file carries out the action of creating the sparkify database tables. It relies on the sql_queries.py file we explain below.</li>
  <li>*etl.py* - This python file extracts the user data in the .json files, transforms it into the data formats we need and inserts/loads it into the database tables.</li>
  <li>*Data folder* - This folder contains all the user data in a raw format, as .json files.</li>
  <li>*sql_queries* - This python file contains your create, insert and drop statements. This file is used to design our tables and to manage inserting new data into the tables.</li>
</ul>

<h6>Design Justification</h6>
The objective given to us by Sparkify was to create a database that optimizes queries for their analytics team. With this in mind, we went with a Star schema approach with separate fact and dimension tables to avoid duplicating data in our tables. This design will allow for quick and easy queries from the analytics team where they can derive business insights. 

<ul>
  <li>*songplays table* - This table is our fact table. User session information is stored here to identify when a user signed in and what activity they did.</li>
  <li>*users table* - This table is a dimensions table. User identity information is stored here.</li>
  <li>*songs table* - This table is a dimension table. Song identity information is stored here.</li>
  <li>*artists table* - This table is a dimension table. Artist identity information is stored here.</li>
  <li>*time table* - This table is a dimension table.</li>
</ul>

