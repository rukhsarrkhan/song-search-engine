import bs4
import re
import os
import glob

html_files_path = r"./html_files"

def fetch_html_files(link: str):
    # This function will fetch html files from html_files folder and return the text in it.
    with open(os.path.join(html_files_path, link), 'r', encoding='utf-8') as html_file:
        return html_file.read()

def data_parse(text: str):
    # This function breaks the text in the files into list of words
    words = re.findall(r"\b\w+\b", text.lower())
    # Opens the file with all the restricted words
    with open("stopWords.txt", "r") as file:
        stop_words = file.read().splitlines()
    return [word for word in words if word not in stop_words]

def define_ranking(words):
    # creates ranking of list of words in key value format 
    rank = {}
    for word in words:
        rank[word] = rank.get(word, 0) + 1
    return rank

# Node object in a trie
class Node(object):
    def __init__(self, char: str):
        self.char = char
        self.parent = None
        self.children = {}
        self.is_a_prefix = False
        self.is_index = False
        self.counter = 1
        self.occurrences = None
        self.rank = None

    def __str__(self):
        return """Node:\tchar: "%s",
            \tchildren: %s
            \tis_a_prefix: %s
            \tis_index: %s
            \tcounter: %s
            \toccureneceList: %s
            \trank: %s""" % (self.char, self.children, self.is_a_prefix, self.is_index, self.counter, self.occurrences, self.rank)

# Trie object consisting of nodes
class Trie(object):
    def __init__(self, root=None):
        if root is None:
            self.root = Node(" ")

    def add_word(self, word: str, link: str, rank: int):
        node = self.root
        # we iterate over all the characters in the words
        for char in word:
            try:
                # if the character is already present in the tree, traverse tree to that node 
                child = node.children[char]
                child.counter += 1
                node = child
            except:
                # if the character is not present in the tree, create a new node with proper links
                new_node = Node(char)
                new_node.parent = node
                node.children[char] = new_node
                node = new_node
        # set the node as index as it is the last node in that route
        node.is_index = True
        if node.children:
            # set prefix if the node has children
            node.is_a_prefix = True
        if node.rank:
            try:
                previous_rank = node.rank[link]
                if previous_rank != rank:
                    if node.occurrences:
                        try:
                            list_of_links = node.occurrences[previous_rank]
                            if link in list_of_links:
                                list_of_links.remove(link)
                                list_of_links = node.occurrences[rank]
                                if link not in list_of_links:
                                    list_of_links.append(link)
                        except:
                            node.occurrences[rank] = [link]
                    else:
                        node.occurrences = {rank: [link]}
            except:
                node.rank[link] = rank
                if node.occurrences:
                    try:
                        list_of_links = node.occurrences[rank]
                        if link not in list_of_links:
                            list_of_links.append(link)
                    except:
                        node.occurrences[rank] = [link]
        else:
            node.rank = {link: rank}
            if node.occurrences:
                try:
                    list_of_links = node.occurrences[rank]
                    if link not in list_of_links:
                        list_of_links.append(link)
                except:
                    node.occurrences[rank] = [link]
            else:
                node.occurrences = {rank: [link]}


class Song_Search_Engine(object):
    def __init__(self):
        self.trie = Trie()
        self.compressedTrie = Trie()

    def parse_html(self, link):
        html_page = fetch_html_files(link)
        soup = bs4.BeautifulSoup(html_page, 'html.parser')
        text_from_page = soup.get_text()
        words_from_page = data_parse(text_from_page)
        return words_from_page

    def crawl_pages(self, trie: Trie, link: str):
        words_from_page = self.parse_html(link)
        rank_of_page = define_ranking(words_from_page)
        for word, rank in rank_of_page.items():
            trie.add_word(word, link, rank)


    def compress_node(self, node):
        children = list(node.children.values())
        if len(children) == 1 and node.is_a_prefix == 0:
            child = children[0]
            child.parent = None
            del node.parent.children[node.char]
            node.char += child.char
            node.parent.children[node.char] = node
            node.children = child.children
            node.is_a_prefix = child.is_a_prefix
            node.is_index = child.is_index
            node.occurrences = child.occurrences
            node.rank = child.rank
            self.compress_node(node)
        elif len(children) > 1:
            for child in children:
                self.compress_node(child)

    def compressing_trie(self):
        node = self.compressedTrie.root
        for child in list(node.children.values()):
            self.compress_node(child)

    # methods searches for a given string in a trie data structure
    def search_word_helper(self, node: Node, string: str):
        children = list(node.children.items())
        for child in children:
            if child[0] == string and child[1].is_index == 1:
                return child[1].occurrences
            elif string.find(child[0]) == 0:
                return self.search_word_helper(child[1], string.replace(child[0], "", 1))
        return None
    # wrapper around search_word_helper()
    def word_search(self, word: str):
        root = self.compressedTrie.root
        return self.search_word_helper(root, word)

    # method processes the search results and prints them in a formatted way.
    def process_search_results(self, search_results):
        final_results = sorted(list(search_results.items()), key=lambda tup: tup[0], reverse=True)
        for tup in final_results:
            for res in tup[1]:
                print("Word that you searched is present in: ",res)
        print("\n")


def main():
    links = []
    for file in os.listdir(html_files_path):
        if os.path.isfile(os.path.join(html_files_path, file)):
            links.append(file)

    # initating search engine
    song_search_engine = Song_Search_Engine()

    for link in links:
        song_search_engine.crawl_pages(song_search_engine.compressedTrie, link)
    song_search_engine.compressing_trie()

    print("\nSearching for music made easy! Try search for a word related to music:\n")
    def get_input():
        return re.sub("[^\w]", "", input("Type your word to search or type quit/exit/q to exit the Search engine: ").lower())

    searched_keyword = get_input()
    while searched_keyword not in ["quit", "exit", "q"]:
        search_results = song_search_engine.word_search(searched_keyword)
        if search_results:
            song_search_engine.process_search_results(search_results)
        else:
            print("Does not exist in any html files\n")
        searched_keyword = get_input()

if __name__ == "__main__":
    main()
