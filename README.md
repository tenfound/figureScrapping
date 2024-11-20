Figure Scrapping:

Objective:
1. Scrap listings from Pre-Owned Section of AmiAmi
2. Compile listings into an excel sheet

Bonus Objectives:
1. Take listings and put them into a database
2. Display entries of the database on a webpage
3. Search features

Problems to tackle / Tasks to do:
1. How to handle figures with discounted prices?
- eg. https://www.amiami.com/eng/detail/?gcode=FIGURE-156533-R & https://www.amiami.com/eng/detail/?gcode=FIGURE-144891-R
- can use "item-detail__price_selling-price" class instead of "item-detail__price" class, the actual selling price of the item.
- list price & discount price (the one that's cancelled) is the same. Use one or the other.
2. Standardise Size Specifications column.
  - Currently some entries use temp_list to "find" the size specification.
  - temp_list does not split the text in original scrapping process.
  - Results in some entires containing extra information when only "Size:" is needed.
3. Figures can have a "Product Line" entry in the original page while others don't.
  - Causes some entries in excel to be misaligned by 1.
4. Proceed with learning how to do database i guess.



find() vs findAll():
find() searches for the first result (automatically sets limit=1)
findAll() searches the entire document

findAll() is of type list, and returns an empty list if nothing is found.
find() returns a string if something is found and None if nothing is found.

Why used used lists instead of growing the dataframe:
https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
& also, df.append() is deprecated. 

Open Price: Figure is likely a prize figure.
