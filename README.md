# Mission to Mars

## Overview

This project demonstrates a responsive website using bootstrap, python, flask, and mongodb.

The data for this project, was obtained by scraping the following sites for images, technical data and news articles:

- Mars news site: https://data-class-mars.s3.amazonaws.com/Mars/index.html
- Mars featured image site: featured image: https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html
- Mars facts site: https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html
- Mars hemispheres site:
  https://marshemispheres.com/

## Usage

1: Open a Terminal window and start the MongoDB server:

    brew services start mongodb-community@5.0

2: Check that the mars_app DB exists. If not, create it a new one. Start the mongo DB in the terminal by entering the command `mongo`. From the Mongo DB CLI enter `show databases`.

2: Run the app:

    python app.py

3: The previous command will start the app on port 127.0.0.1:5000. Go to this port in your web browser to open the Mission to Mars site:

  <img src="./images/landing_page.jpeg" alt="Mars Landing Page" width="500"/>

4: When the 'Latest News' button is clicked, the '/scrape' route will be used to get the latest news and display it in the appropriate section on the webpage:

  <img src="./images/latest_news.jpeg" alt="Mars News" width="500"/>

5: Shut down the Mongo DB server using the following commands from the Mongo CLI:

    > use admin
    > db.shutdownServer()

## Folders/Files

- templates: This folder contains the index.html template required to render the data from app.py.

- index.hml: This file is the template that calls app.py to scrape the sites used to retrieve the data shown on this site.

- app.py: python program to connect to the mongo datbase 'mars_app' using PyMongo and creates the following flask routes:

  - /: retrieves the one and only collection in the local mars_db containing all the data for the site to render the index.html template

  - /scrape: calls the 'scrape_all()' function in scraping.py to retrieve all the data to be displayed on the site.

  After scraping the data, it stores it in the mars_app mongo db as a collection.

  If the collection already exists, it will be upserted.

- scraping.py: python program defining the following functions to scrape sites for data and it to the template for rendering:

  - scrape_all(): performs the following tasks:

    - set up splinter to use a chrome browser
    - calls mars_news() function to retrieve the most recent news article and title to be displayed under the jumbotron
    - calls featured_image(browser) function to retrieve the featured image to be displayed on the left
    - calls mars_facts() function to retrieve the mars facts to be displayed on the right
    - calls mars_hemispheres(browser) function to retrieve the list of hemispheres consisting of a url to an image and its title to be displayed in the bottom 1/2 of the main page
    - populates the data dictionary object with the data retrieved from the browser and returns a it to be used by the index.html template to render the images and other data

  - mars_news(browser): given a browser this function will visit the mars news site to find the news article teaser and title which will be returned as 2 strings, news_title and news_p

  - featured_image(browser): given a browser this function will visit the JPL space site to retrieve the currently featured image

  - mars_facts(): uses pandas to scrape the mars facts site for the latest facts storing it in a dataframe. This dataframe is converted to html to be returned as an pre-formatted table to be displayed neatly on the site

  - mars_hemispheres(browser): given a browser this function will visit the mars hemispheres site to retrieve the high resolution images and titles for each of mars 4 hemispheres. The hemispheres will be stored as a dictionary object with the attributes 'image_url' and 'title' returned as a list of dictionaries.

  ## Troubleshooting Tips

  ### Port in Use

  To stop the app, use the terminal to run the following commands:

  - `ps -fA | grep python`

    Shows a list of python processess with their process ids.

  - `kill -9 pid`

    Where pid is the process id of app.py

  ### To Check Data in Mongo DB

  From the terminal enter `mongo` and enter the following commands from the mongo CLI:

  ```
  > use mars_app
  > show collections
  > db.<collection_name>.find()
  ```

  ### Mongo DB Process Documentation

  https://www.mongodb.com/docs/manual/tutorial/manage-mongodb-processes/
