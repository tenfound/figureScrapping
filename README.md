Figure Scrapping:

Objective:
1. Scrap listings from Pre-Owned Section of AmiAmi
2. Compile listings into an excel sheet

Bonus Objectives:
1. Take listings and put them into a database
2. Display entries of the database on a webpage
3. Search features

Problems to tackle:
1. How to handle figures with discounted prices?
- eg. https://www.amiami.com/eng/detail/?gcode=FIGURE-156533-R & https://www.amiami.com/eng/detail/?gcode=FIGURE-144891-R
- can use "item-detail__price_selling-price" class instead of "item-detail__price" class, the actual selling price of the item.
- list price & discount price (the one that's cancelled) is the same. Use one or the other.

Some classes to add:
Figure name: item-detail__section-title
Brand: item-detail__brand
Price: item-detail__price

Get Size specification from class “item-about__data-text more active”



find() vs findAll():
find() searches for the first result (automatically sets limit=1)
findAll() searches the entire document

findAll() is of type list, and returns an empty list if nothing is found.
find() returns a string if something is found and None if nothing is found. 
