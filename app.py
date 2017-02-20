# -*- coding: utf-8 -*-
import os
import codecs
from flask import Flask, request, render_template, jsonify
from reader import Abbreviation, Book, Verse
from bible import Bible
from db_connector import Query, DBBook
from datetime import datetime

app = Flask(__name__)

KOR_BIBLE   = 'db/kor_bible.db'
ENG_BIBLE   = 'db/eng_bible.db'

def generate_bible_verse_list_from_text(text):
    bible_verse_list = Abbreviation.identify_bible_verse(text)
    if not bible_verse_list:
        return []
        
    results = []
    for curr in bible_verse_list:
        book = Abbreviation.identify_book(curr)
        verse = Abbreviation.identify_verse(curr)
        
        book_fullname = Book.get_kor_bible_from_abbr(book)
        if book_fullname is not None and Verse.get_chapter(verse) > 0 \
            and len(Verse.get_verses(verse)) > 0:
            results.append(book_fullname + u' ' + verse)

    return results

def encode_bible_verse_form(book_fullname, verse):
    return book_fullname + u' ' + verse
    
def decode_bible_verse_form(bible_verse_form):
    content = bible_verse_form.split(u' ')
    if not content or len(content) != 2:
        return None
        
    return content
    
def log_parsed_bible_verse(input_text, verse_list):
    base_dir = 'records/'
    curr_time = str(datetime.now())
    write_file(base_dir + curr_time + '_input.txt', input_text)
    
    output_content = u''
    for verse in verse_list:
        if len(output_content) <= 0:
            output_content = verse
        else:
            output_content += u'\n' + verse
            
    write_file(base_dir + curr_time + '_output.txt', output_content)
    
def write_file(path, content):
    file = codecs.open(path, 'w', encoding='utf8')
    file.write(content)
    file.close()

@app.route('/')
def get_main_page():
    bible_books = DBBook.bible_kor_to_db.keys()
    bible_books.sort()
    return render_template('index.html', bible_books=bible_books)
            
@app.route('/_parse_bible_verse')
def parse_bible_verse():
    bible_text = request.args.get('text')
    bible_verse_list = generate_bible_verse_list_from_text(bible_text)
    log_parsed_bible_verse(bible_text, bible_verse_list)
    return jsonify(result=bible_verse_list)
    
@app.route('/_show_bible_word')
def show_bible_word():
    version_list = [KOR_BIBLE, ENG_BIBLE]
    query_with_version = {}
    query_with_version[KOR_BIBLE] = Query(KOR_BIBLE)
    query_with_version[ENG_BIBLE] = Query(ENG_BIBLE)
    
    bible_verse = request.args.get('verse')
    decoded_bible_verse = decode_bible_verse_form(bible_verse)
    if decoded_bible_verse is None:
        return jsonify(result='Error')
        
    book_fullname = decoded_bible_verse[0]
    verse = decoded_bible_verse[1]
    chapter = Verse.get_chapter(verse)
    verse_list = Verse.get_verses(verse)
    bible = Bible(book_fullname, chapter, verse_list, verse)
    
    for version in version_list:
        results = query_with_version[version].get_result(bible)
        bible.add_result(version, results)
    content = bible.get_print_str(version_list, False)
    
    for version in version_list:
        query_with_version[version].close_connection()
    
    return jsonify(result=content)

if __name__ == '__main__':
    app.run(debug=True)
