"""
For each file in corpus described in corpus_description_file_path, create in output_folder_path a file with one sentence per line.
Each line first contains an integer refering to the id of its style then the content of the sentence.
"""

import codecs
import sys
import os
import getopt
import nltk.data

class Dataset(object):
	absolute_path = ""
	format = ""
	style = ""
	language = ""

	def __init__(self, absolute_path, format, style, language):
		self.absolute_path = absolute_path
		self.format = format
		self.style = style
		self.language = language

def read_args(argv):
   corpus_description_file_path = './corpus_description'
   output_folder_path = './output'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <corpus_description_file_path> -o <output_folder_path>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <corpus_description_file_path> -o <output_folder_path>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         corpus_description_file_path = arg
      elif opt in ("-o", "--ofile"):
         output_folder_path = arg
   print('Corpus description file: ', corpus_description_file_path)
   print('Output folder: ', output_folder_path)
   return corpus_description_file_path, output_folder_path

def read_corpus_description_file(corpus_description_file_path):
	datasets = []
	with open(corpus_description_file_path) as corpus_description_file:
		dir_path = os.path.dirname(os.path.realpath(corpus_description_file_path))
		print(dir_path)
		lines = corpus_description_file.readlines()
		for line in lines:
			if len(line) > 0 and not line.startswith("#"):
				line_elements = line.split("\t")
				dataset_absolute_path = os.path.join(dir_path, line_elements[0])
				dataset = Dataset(dataset_absolute_path, line_elements[1], line_elements[2], line_elements[3])
				datasets.append(dataset)
	return datasets

def generate_sentences_file(input_file_path, output_file_path):
	print("generate_sentences_file from " + input_file_path + " to " + output_file_path)
	with codecs.open(input_file_path, 'r', encoding='utf8') as input_file:
		input_file_content = input_file.read()
		sentences = tokenizer.tokenize(input_file_content)
		with codecs.open(output_file_path, 'w', encoding='utf8') as output_sentences_file:
			for sentence in sentences:
				output_sentences_file.write(sentence.replace("\n", " ") + os.linesep)

def generate_files_for_dataset(dataset, output_folder_path):
	if not os.path.exists(output_folder_path):
		os.makedirs(output_folder_path)
	dataset_parent_dir_path = os.path.dirname(dataset.absolute_path)
	tokenizer = nltk.data.load("tokenizers/punkt/french.pickle")
	for dirname, dirnames, filenames in os.walk(dataset.absolute_path):
		for filename in filenames:
			absolute_file_path = os.path.join(dirname, filename)
			relative_file_path = absolute_file_path.replace(dataset_parent_dir_path + "/", "")
			output_filename = relative_file_path.replace("/", "_").replace(" ", "_")
			output_file_path = os.path.join(output_folder_path, output_filename)
			print("generate_sentences_file from " + absolute_file_path + " to " + output_file_path)
			with codecs.open(absolute_file_path, 'r', encoding='utf8') as input_file:
				input_file_content = input_file.read()
				sentences = tokenizer.tokenize(input_file_content)
				with codecs.open(output_file_path, 'w', encoding='utf8') as output_sentences_file:
					for sentence in sentences:
						output_sentences_file.write(sentence.replace("\n", " ") + os.linesep + os.linesep)

def main(argv):
	corpus_description_file_path, output_folder_path = read_args(argv)
	datasets = read_corpus_description_file(corpus_description_file_path)
	for dataset in datasets:
		generate_files_for_dataset(dataset, output_folder_path)

if __name__ == "__main__":
	main(sys.argv[1:])
