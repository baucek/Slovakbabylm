# Slovakbabylm

In folders you can find specific .py or .ipynb files which were used for SlovakBabyLM. 
Whole slovakbabylm dataset can be found on https://huggingface.co/datasets/ubokri/SlovakBabyLM

# Repository Structure
## Experiments 
This folder contain .ipynb files which was used for application metrics and get results from them.
Python version: 3.8.10

Files:
- `Creating_text.ipynb`-  Create text based on certain requirements, specific order or randomly also counter to compute how many data are inside of files
- `Order_text.ipynb`-     Train tokenizer for specific text, evaluate specific text and create order (by subdataset or as a whole json) results are json files and order of files
- `Comp_masking.ipynb`-   Put created ordered json into text file and for 3 experiment create text with masks based on condition.
- `Creating_model.ipynb`- Create models based on created text with or without specific masking also compute how many masks create DataCollatorForLanguageModeling class
- `sa.ipynb` & `qa.ipynb`-  Sentiment analysis and question anwering
- `Visualization.ipynb`-  Code for tables which are in diploma thesis. 


In each notebook you need to set name of folder or list of folders in specific order depence on what do you want.
Requirements are in folder
You run gradually each cell.

Empty folders for results:
- `data`: in data folder you have 6 empty folders where you need to download sub-datasets from https://huggingface.co/datasets/ubokri/SlovakBabyLM
- `tok_bpe`: Tokenizer for each text
- `saved_models`: All files for running a model
- `results_evaluation`: Results of QA and SA


## Data mining and Preprocessing
If file for crawling is not folder you can find it in `Crawling-scrapy\spiders-scr\spiders`
Python version: 3.11.7 
In folder subtitles are two text files which are code in AWS lambdas, which you need to create and also create AWS S3 instance where you save code and python enviroment with libraries
neccessery to run code (.zip)
For save result you need to change path for each file


### Crawling spider  
This folder contain enviroment neccessery to run scrapy. 
All spiders are in Crawling-scrapy\spiders-scr\spiders
You run spider from CMD: `cd Crawling-scrapy\spiders-scr` 
`scrapy crawl {name of spider} -o outfile.json`



