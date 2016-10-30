# garage_sales
# Welcome to HackLB/garage_sales

This repository is intended to mirror and archive records from the City of Long Beach [Garage Sale Permit](https://wwwbitprod1.longbeach.gov/GarageSalePermit/SearchByDate.aspx) database. We opted for JSON as a more convenient format for consuming and analyzing garage sale records, and git in order to maintain a historical record including changes over time. This repo groups records by address, so you can easily see the history of garage sales for each address.

This project is an activity of [HackLB](https://github.com/HackLB).


### Contributing to this repo

Pull requests are welcome - if you have an idea for an improvement (for instance, porting `update.py` to another language) you're welcome to make it and open a PR, or open an issue first for discussion.

### Sample record

A typical record is shown below for reference:

```
{'dates': ['10/29/2016 - 10/30/2016'], 'location': '6320 LONG BEACH BLVD'}
```