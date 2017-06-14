# -*- coding: utf-8 -*-
import re

class Bible(object):
    '''Represent Bible class that shows book, chapter, verses and bible text'''
    def __init__(self, book, chapter, verse_list, chapter_verse_form):
        '''Initialize the object by book, chapter, verses and chapter-verse abbreviation form'''
        self.book = book
        self.chapter = chapter
        self.verse_list = verse_list
        self.chapter_verse_form = chapter_verse_form
        self.text = {}

    def add_text(self, version, new_text):
        '''Add bible text'''
        if version in self.text:
            del self.text[version]

        self.text[version] = new_text

    def get_book_chapter_verse(self):
        '''Get book and chapter-verse form'''
        return self.book + u' ' + self.chapter_verse_form

    def get_print_str_in_version(self, version):
        '''Print the string by verse and version'''
        content = u''
        for verse in self.verse_list:
            verse_str = str(verse)
            if verse_str in self.text[version]:
                if len(content) > 0:
                    content += u'\n'
                content += verse_str + '. ' + self.refine_text(self.text[version][verse_str])

        return content

    def get_print_str_in_verse(self, verse, version_list):
        '''Print the string by version and verse'''
        content = u''
        for version in version_list:
            verse_str = str(verse)
            if verse_str in self.text[version]:
                if len(content) > 0:
                    content += u'\n'
                content += verse_str + '. ' + self.refine_text(self.text[version][verse_str])

        return content

    def get_print_str(self, version_list, b_version_first):
        '''Print the string of chapter, verse and text'''
        if not version_list or len(version_list) <= 0:
            return u''

        for version in version_list:
            if not self.text[version]:
                return u'말씀을 찾을 수 없습니다.'

        content = self.get_book_chapter_verse() + u'\n'
        if b_version_first:
            for version in version_list:
                if version in self.text:
                    content += self.get_print_str_in_version(version) + u'\n'
        else:
            for verse in self.verse_list:
                content += self.get_print_str_in_verse(verse, version_list) + u'\n'

        return content
    
    @staticmethod
    def refine_text(text):
        if not re.search(u'[가-힣]+', text):
            return text
            
        refined = u''
        for ch in text:
            if not is_alpha_unicode(ch):
                refined += ch
                
        return refined
    
    @staticmethod
    def is_alpha_unicode(ch):
        ord_val = ord(ch)
        if ord_val >= ord('a') and ord_val <= ord('z') or ord_val >= ord('A') and ord_val <= ord('Z'):
            return True
        else:
            return False
