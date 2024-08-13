Modern Tibetan POS-tagger using Google's Gemini Pro API
The script is designed to produce Universal Dependency (UD) part-of-speech (POS) tagged files in conLLu-format.
## Description
The script takes all files from a folder, tokenises the contained text with modern-botok and sends it line by line to Google Gemini using the Google Cloud API. Gemini returns the tokens with POS-tags and writes it in conLLu-format. In a post-processing step, the generated conLLu-files are cleaned up and tags are normalised.
### POS-tag set
The script was developed to produce training data to train a Tibetan language model for SpaCy, which is best done using Universal Dependency (UD) tags. Currently, a limited set of UD tags is used: 
## Setting up and running the script
Detailed instructions on how to set up Google Cloud and Vertex AI and how to run the script are in How-to-run.txt 
### Note
There should be more files in the conllu, output and text folders. The files uploaded here are only samples.

The script was developed for the Divergent Discourses project by Yuki Gyokogu (Leipzig University) and Franz Xaver Erhard (Leipzig University)
