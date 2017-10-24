# -*- coding: utf-8 -*-
import time
import os
from file_util import copy_directory, zip_directory, rename_file, read_file_content, write_file_content, copy_file, remove_directory, remove_file

PPTX_DIR = './pptx/'
PPTX_BASE = PPTX_DIR + 'base'
PPTX_TEMPLATES = PPTX_DIR + 'templates/'

PPTX_FILES = PPTX_DIR + 'files/'
PPTX_ERROR_FILE = 'error.pptx'

REPLACEMENT_POS = 'replacement_position'

def pptx_content(book, chapter_verse_form, book_chapter_verse, text):
    return {
        'book': book,
        'chapter_verse_form': chapter_verse_form,
        'book_chapter_verse': book_chapter_verse,
        'text': text
    }

def build_pptx(pptx_content):
    if pptx_content is None or len(pptx_content) <= 0:
        return PPTX_ERROR_FILE
    
    output_filename = str(time.time())
    working_dir = PPTX_DIR + output_filename
    
    copy_directory(PPTX_BASE, working_dir)
    
    no_slides = len(pptx_content)
    
    content_types = build_content_types(no_slides)
    write_file_content(working_dir + '/[Content_Types].xml', content_types)
    
    presentation = build_presentation(no_slides)
    write_file_content(working_dir + '/ppt/presentation.xml', presentation)
    
    presentation_rels = build_presentation_rels(no_slides)
    write_file_content(working_dir + '/ppt/_rels/presentation.xml.rels', presentation_rels)
    
    for idx, val in enumerate(pptx_content):
        slide = build_slide(val)
        slide_filename = working_dir + '/ppt/slides/slide%d.xml' % (idx + 1)
        write_file_content(slide_filename, slide)
        
        copy_file(PPTX_TEMPLATES + '/ppt/slides/_rels/slide.xml.rels', working_dir + '/ppt/slides/_rels/slide%d.xml.rels' % (idx + 1))
        
    remove_file(working_dir + '/ppt/_rels/.keep')
    remove_file(working_dir + '/ppt/slides/_rels/.keep')
    
    zip_directory(working_dir, output_filename)
    remove_directory(working_dir)
    
    from db_connector import DBBook
    book_kor = pptx_content[0]['book']
    book_eng = DBBook.get_db_book(book_kor)
    chapter_verse_form = pptx_content[0]['chapter_verse_form']
    pptx_filename = book_eng + ' ' + chapter_verse_form + '.pptx'
    
    rename_file(output_filename + '.zip', PPTX_FILES + pptx_filename)
    
    return pptx_filename
    
def remove_old_pptx():
    curr_time = time.time()
    
    for filename in os.listdir(PPTX_FILES):
        if filename != PPTX_ERROR_FILE:
            fullpath = PPTX_FILES + filename
            file_created = os.path.getmtime(fullpath)
            
            if curr_time - file_created > (60 * 60 * 24):
                print('Remove ' + filename)
                remove_file(fullpath)
    
def build_content_types(no_slides):
    content = u''
    for index in range(0, no_slides):
        content += u'<Override ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" PartName="/ppt/slides/slide%d.xml"/>' % (index + 1)

    content_types_filename = PPTX_TEMPLATES + '[Content_Types].xml'
    content_types_content = read_file_content(content_types_filename)
    
    return content_types_content.replace(REPLACEMENT_POS, content)
    
def build_presentation(no_slides):
    content = u'<p:sldIdLst>'
    for index in range(0, no_slides):
        content += u'<p:sldId r:id="rId%d" id="%d"/>' % (index + 11, index + 256)
    content += u'</p:sldIdLst>'

    presentation_filename = PPTX_TEMPLATES + 'ppt/presentation.xml'
    presentation_content = read_file_content(presentation_filename)
    
    return presentation_content.replace(REPLACEMENT_POS, content)
    
def build_presentation_rels(no_slides):
    content = u''
    for index in range(0, no_slides):
        content += u'<Relationship Target="slides/slide%d.xml" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Id="rId%d"/>' % (index + 1, index + 11)

    presentation_rels_filename = PPTX_TEMPLATES + 'ppt/_rels/presentation.xml.rels'
    presentation_rels_content = read_file_content(presentation_rels_filename)
    
    return presentation_rels_content.replace(REPLACEMENT_POS, content)
    
def build_slide(pptx_content):
    book_chapter_verse = pptx_content['book_chapter_verse']
    text_content = u''
    for idx, val in enumerate(pptx_content['text']):
        if idx == 0:
            curr_content = u'<a:p><a:pPr algn="l"><a:buFontTx/><a:buNone/><a:defRPr/></a:pPr><a:r><a:rPr lang="ko-KR" altLang="en-US" sz="3600" b="1" dirty="0"><a:latin typeface="맑은 고딕" pitchFamily="50" charset="-127"/></a:rPr><a:t>'
            curr_content += val
            curr_content += u'</a:t></a:r><a:endParaRPr lang="en-US" altLang="ko-KR" sz="3600" b="1" dirty="0"><a:latin typeface="맑은 고딕" pitchFamily="50" charset="-127"/></a:endParaRPr></a:p>'
        else:
            curr_content = u'<a:p><a:pPr algn="l"><a:buFontTx/><a:buNone/><a:defRPr/></a:pPr><a:endParaRPr lang="en-US" altLang="ko-KR" b="1" dirty="0"><a:latin typeface="맑은 고딕" pitchFamily="50" charset="-127"/></a:endParaRPr></a:p><a:p><a:pPr algn="l"><a:buFontTx/><a:buNone/><a:defRPr/></a:pPr><a:r><a:rPr lang="ko-KR" altLang="en-US" sz="2800" dirty="0"><a:latin typeface="맑은 고딕" pitchFamily="50" charset="-127"/></a:rPr><a:t>'
            curr_content += val
            curr_content += u'</a:t></a:r><a:endParaRPr lang="en-US" altLang="ko-KR" sz="2800" dirty="0"><a:latin typeface="맑은 고딕" pitchFamily="50" charset="-127"/></a:endParaRPr></a:p>'
        
        text_content += curr_content
        
    slide_filename = PPTX_TEMPLATES + 'ppt/slides/slide.xml'
    slide_content = read_file_content(slide_filename)
    
    slide_content_with_book_chapter_verse = slide_content.replace('book_chapter_verse', book_chapter_verse)
    return slide_content_with_book_chapter_verse.replace('bible_text', text_content)

if __name__ == '__main__':
    pptx_content = {
        'book_chapter_verse': u'시편 27:1-5',
        'version_list': [1, 2],
        'text': {
            1: u'1. 여호와는 나의 빛이요 나의 구원이시니 내가 누구를 두려워하리요 여호와는 내 생명의 능력이시니 내가 누구를 무서워하리요',
            2: u'1. The LORD is my light and my salvation- whom shall I fear? The LORD is the stronghold of my life-of whom shall I be afraid?'
        }
    }
    
    slide = build_slide(pptx_content)
    write_file_content('./temp_slide1.xml', slide)
