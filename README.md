# This project includes:
1. html_files directory which includes 12 html files of music related wikipedia links
2. songSearchEngine.py which includes serach engine logic for word search
3. stopWords.txt includes array of stop words such as articles, prepositions, and pronouns to exclude them as mentioned in problem statement
4. output.txt which includes sample runs 

# Approach of the project:
1. Reading the html files in html_files directory to parse all the words present in them 
2. Create a trie data structure of all the words present in the input html files. The trie will have node data structure to store the characters of the words
3. Using trie because it allows for fast prefix searching, where you can quickly find all the words in a dataset that start with a certain prefix
4. Initially, the search engine parses all the files to create a trie of all the words present in the html links
5. Later when the user inputs the word he/she wants to search, a search operation is performed on the trie 
6. If the word is present in the trie, list of all the links in which the word exists is printed on the terminal. Else its propmts that the word doesnt exist in any html file
7. The program remains active until the use types quit, exit or q or manually ends the execution
8. Also parsing a stopWords.txt file to exclude stop words such as articles, prepositions, and pronouns

# To run the search engine:
1. Please execute the songSearchEngine.py file in the song-search-engine directory 
2. Python3 is required as we have used bs4 library, which is used for web scarping
3. Example: rkhan@Rukhsars-Air song-search-engine % python3 songSearchEngine.py
