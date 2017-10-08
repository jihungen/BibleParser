# -*- coding: utf-8 -*-
import re

from ppt import ppt_content

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

    def get_print_str_in_version(self, version, b_remove_annotation):
        '''Print the string by verse and version'''
        content = u''
        for verse in self.verse_list:
            verse_str = str(verse)
            if verse_str in self.text[version]:
                if len(content) > 0:
                    content += u'\n'
                
                if b_remove_annotation:
                    curr_text = refine_text(self.text[version][verse_str])
                else: 
                    curr_text = self.text[version][verse_str]
                content += verse_str + '. ' + curr_text

        return content

    def get_print_str_in_verse(self, verse, version_list, b_remove_annotation):
        '''Print the string by version and verse'''
        content_list = self.get_print_list_in_verse(verse, version_list, b_remove_annotation)
        return u'\n'.join(content_list)
        
    def get_print_list_in_verse(self, verse, version_list, b_remove_annotation):
        '''Print the string by version and verse'''
        content_list = []
        for version in version_list:
            verse_str = str(verse)
            if verse_str in self.text[version]:
                if b_remove_annotation:
                    curr_text = refine_text(self.text[version][verse_str])
                else: 
                    curr_text = self.text[version][verse_str]
                    
                content_list.append(verse_str + '. ' + curr_text)

        return content_list

    def get_print_str(self, version_list, b_version_first, b_remove_annotation):
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
                    content += self.get_print_str_in_version(version, b_remove_annotation) + u'\n'
        else:
            content_list = []
            for verse in self.verse_list:
                curr_content = self.get_print_str_in_verse(verse, version_list, b_remove_annotation)
                if len(curr_content) > 0:
                    content_list.append(curr_content)
                    
            content += u'\n'.join(content_list)

        return content
        
    def get_ppt_content(self, version_list, b_remove_annotation):
        '''Print the string of chapter, verse and text'''
        if not version_list or len(version_list) <= 0:
            return dict()

        for version in version_list:
            if not self.text[version]:
                return dict()
                
        content_list = []
        for verse in self.verse_list:
            curr_text = self.get_print_list_in_verse(verse, version_list, b_remove_annotation)
            curr_ppt_content = ppt_content(
                book_chapter_verse=self.get_book_chapter_verse(),
                version_list=version_list,
                text=curr_text
            )
            content_list.append(curr_ppt_content)
            
        return str(content_list)

def refine_text(text):
    if not re.search(u'[가-힣]+', text):
        '''Refine the only Korean text.'''
        return text

    refined = u''
    cnt_bracket = 0
    for ch in text:
        if ch == u'(':
            cnt_bracket += 1
            
        if cnt_bracket > 0:
            if ch == u')':
                cnt_bracket -= 1
                
            continue
        
        if not is_alpha_unicode(ch):
            refined += ch

    return refined

def is_alpha_unicode(ch):
    ord_val = ord(ch)
    if ord_val >= ord('a') and ord_val <= ord('z') or ord_val >= ord('A') and ord_val <= ord('Z'):
        return True
    else:
        return False
