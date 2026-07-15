## What have I landed on? 🐦🐦‍⬛

This is a personal project revolving around the popular bird-themed board game Wingspan. I enjoy the game very much, and had the idea that it would be fun to do some data analysis with it, which could also help me to get a better grip on SQL and the way that it combines with general programming languages.

## Contents

I have constructed my relational database in MySQL. It includes data about all 261 bird cards from the base game, the swift start pack and the European expansion. 

The file ``wingspan.sql`` can be used to reconstruct my database, which contains two tables. The first is the **bird** table:

| Field                   | Type                                     | Null | Key | Default | Extra |
|-------------------------|------------------------------------------|------|-----|---------|-------|
| scientific_name         | varchar(50)                              | NO   | PRI | NULL    |       |
| nl_name                 | varchar(50)                              | YES  | UNI | NULL    |       |
| victory_points          | smallint unsigned                        | NO   |     | NULL    |       |
| lives_in_forest         | tinyint(1)                               | YES  |     | 0       |       |
| lives_in_grasslands     | tinyint(1)                               | YES  |     | 0       |       |
| lives_in_wetlands       | tinyint(1)                               | YES  |     | 0       |       |
| nest_type               | enum('BOWL','PLTF','CVTY','GRND','STAR') | YES  |     | NULL    |       |
| nest_capacity           | smallint unsigned                        | NO   |     | NULL    |       |
| wingspan                | smallint unsigned                        | NO   |     | NULL    |       |
| expansion               | enum('SW','EE','OE','A','AM')            | YES  |     | NULL    |       |
| power_id                | smallint unsigned                        | YES  | MUL | NULL    |       |
| food_is_multiple_choice | tinyint(1)                               | NO   |     | 0       |       |
| worms                   | smallint unsigned                        | NO   |     | 0       |       |
| grains                  | smallint unsigned                        | NO   |     | 0       |       |
| berries                 | smallint unsigned                        | NO   |     | 0       |       |
| fish                    | smallint unsigned                        | NO   |     | 0       |       |
| rats                    | smallint unsigned                        | NO   |     | 0       |       |
| wild                    | smallint unsigned                        | NO   |     | 0       |       |

For the bird powers, I have included a separate table called **power**:

| Field       | Type                                                   | Null | Key | Default | Extra          |
|-------------|--------------------------------------------------------|------|-----|---------|----------------|
| power_id    | smallint unsigned                                      | NO   | PRI | NULL    | auto_increment |
| color       | enum('WH','BR','PK','TL')                              | YES  |     | NULL    |                |
| type        | enum('DICE','FOOD','CARD','CACH','EGGS','SWRM','HUNT') | YES  |     | NULL    |                |
| description | varchar(250)                                           | YES  |     | NULL    |           

## Goals

The purpose of this project is mostly to be a space for me to get more used to SQL databases and querying. I'd like to use this data to try out other databases as well, such as PostgreSQL. 

Beyond just constructing the database, I've also played around with investigating a few research questions surrounding correlations between the different bird properties. For this I've used Python (via Jupyter Notebook) with Matplotlib, Numpy and Pandas, as these are tools which I'm familiar with. I hope to eventually make a blog post out of this data analysis on my GitHub Pages blog, although my LangLearner project is currently my first priority. 

--------------------

Wingspan © Stonemaier Games
