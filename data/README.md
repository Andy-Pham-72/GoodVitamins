# GoodVitamins Datasets

This is the datasets that I scraped from [iHerb Bestselling Vitamin Products](https://ca.iherb.com/c/Vitamins?sr=2&noi=48&p=1)


### Data Schema for `iherb_best_selling_products_raw_dataset` :

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

### Data Schema for `iherb_best_selling_products_clean_dataset` :

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
|product_id         | The product's unique ID                             |
|brand_id           | The brand's unique ID                               |

