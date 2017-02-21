# -*- coding: utf-8 -*-
import codecs
from datetime import datetime

class Log(object):
    RECORD_DIR = 'records/'
    INPUT_FILE = '_input.txt'
    OUTPUT_FILE = '_output.txt'
    
    @classmethod
    def log_parsed_bible_word(cls, input_text, bible_word_list):
        curr_time = str(datetime.now())
        Log.write_file(cls.RECORD_DIR + curr_time + cls.INPUT_FILE, input_text)

        output_content = u''
        for bible_word in bible_word_list:
            if len(output_content) <= 0:
                output_content = bible_word
            else:
                output_content += u'\n' + bible_word

        Log.write_file(cls.RECORD_DIR + curr_time + cls.OUTPUT_FILE, output_content)
        
    @staticmethod
    def write_file(path, content):
        file = codecs.open(path, 'w', encoding='utf8')
        file.write(content)
        file.close()