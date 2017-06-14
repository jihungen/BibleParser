# -*- coding: utf-8 -*-
import codecs
from datetime import datetime

class Log(object):
    RECORD_DIR = 'records/'
    INPUT_FILE = '_input.txt'
    OUTPUT_FILE = '_output.txt'
    
    @classmethod
    def log_parsed_bible_word(cls, input_text, bible_word_list):
        pass
        
    @staticmethod
    def write_file(path, content):
        file = codecs.open(path, 'w', encoding='utf8')
        file.write(content)
        file.close()
