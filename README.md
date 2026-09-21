[![Django CI](https://github.com/MargotHTeunisse/Wingspan-Data-Project/actions/workflows/django.yml/badge.svg)](https://github.com/MargotHTeunisse/Wingspan-Data-Project/actions/workflows/django.yml)

## What have I landed on? 🐦🐦‍⬛

This is a personal project revolving around the popular bird-themed board game Wingspan. I enjoy the game very much, and had the idea that it would be fun to use its bird data for a little data project.

## Visualization 

I have chosen to build my visualization tool in Python, using the Django framework. 

The idea of my visualization is to include:

- A search tool with filters for bird properties
- A charting area, in which one can either plot the distribution of a single bird property, or compare two properties.

The user interface uses Django templating and views in combination with basic CSS styling and JavaScript, including Chart.js for the charting area.

At this time the search tool can look up birds by their scientific name, but the filter function is not implemented yet. The charting area currently allows for different charts to be loaded based on a selection menu, though the chart itself is currently a placeholder, since this function is not integrated with the database yet.

## Data

To save the bird data, I have constructed a relational database in MySQL. It includes data about all 261 bird cards from Wingspan's base game, the swift start pack and the European expansion. 

The file ``wingspan.sql`` can be used to reconstruct my database, which contains two tables. The first is the **bird** table, which keeps track of the properties of the individual bird cards, as the name suggests. Note that for the bird power, I just save a foreign key.

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

For the bird powers, I have included a separate table called **power**. I use a separate table for this, since some birds have no power, and the same power may be shared among multiple birds.

| Field       | Type                                                   | Null | Key | Default | Extra          |
|-------------|--------------------------------------------------------|------|-----|---------|----------------|
| power_id    | smallint unsigned                                      | NO   | PRI | NULL    | auto_increment |
| color       | enum('WH','BR','PK','TL')                              | YES  |     | NULL    |                |
| type        | enum('DICE','FOOD','CARD','CACH','EGGS','SWRM','HUNT') | YES  |     | NULL    |                |
| description | varchar(250)                                           | YES  |     | NULL    |                |

## Acknowledgements

I am certainly not alone in taking an interest in the data behind Wingspan, and there are several community projects which I was inspired by. First, I would be amiss not to mention [Wingsearch](https://navarog.github.io/wingsearch/), created by [navarog on GitHub](https://github.com/navarog/wingsearch) and other contributors. I consider this the definitive Wingspan search tool, which the search tool in my own visualization is openly inspired by.

Also worth mentioning is the [Wingspan spreadsheet](https://boardgamegeek.com/filepage/193164/wingspan-spreadsheet-bird-cards-bonus-cards-end-of) by TawnyFrogMouth on BoardGameGeek. While I preferred to construct my own database for this project, TawnyFrogMouth's data is at the basis of many Wingspan data analysis project, including Wingsearch.

Finally, want to mention the series (The Maths Behind Wingspan)[https://youtube.com/playlist?list=PLMmCK_-bDs_mvwsFrDiDeWqy_8oG-mOBz&si=A6sC7QOFLrep4Ye6] by Wingin' it on Youtube. The series uses mathematical analysis of Wingspan to give strategy advice, and while analysis was not my focus here, this series was what pushed me to try and look at Wingspan through a research lens.

--------------------

Wingspan © Stonemaier Games
