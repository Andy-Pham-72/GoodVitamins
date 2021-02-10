# iHerb Webscraper Notebook

A notebook that has python script using Selenium to scrape 600 reivews per vitamin product in the [bestselling vitamin product](https://ca.iherb.com/c/Vitamins?sr=2&noi=48&p=1).

## Data Schema

|    Columns        |  Description                                        |
|-------------------|-----------------------------------------------------|
|item_image_link    | Product image link                                  |   
|item_brand         | Product brand name                                  |   
|item_name          | Product name                                        |
|item_description   | List of product features                            |
|total_rating       | Total rating of product                             |
|review_contents    | Product review contents                             |
|individual_rating  | Individual user rating                              |
|product_helpful    | Numbers of other users rated the review as helpful  |
|product_not_hepful | Numbers of other users rated the review as unhelpful|

## Future Work

This is the first web scraping script I've written so there are still some issues; for example, the script can catch non-vitamin products and run unstably sometimes. I'm trying to optimize the script so it can run smoothly everytimes. Therefore, any contributions are welcome.
