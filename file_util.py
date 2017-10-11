import shutil, errno
import codecs

def copy_directory(src_dir, dest_dir):
    try:
        shutil.copytree(src_dir, dest_dir)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src_dir, dest_dir)
        else: 
            raise
        
def zip_directory(src_dir, dest_file):
    shutil.make_archive(dest_file, 'zip', src_dir)
    
def remove_directory(target_dir):
    shutil.rmtree(target_dir)
    
def rename_file(src_file, dest_file):
    shutil.move(src_file, dest_file)
    
def copy_file(src_file, dest_file):
    shutil.copyfile(src_file, dest_file)
    
def read_file_content(filename):
    with codecs.open(filename, 'r', encoding='utf8') as f:
        return f.read()
        
    return None
    
def read_binary_file(filename):
    with open(filename, 'rb') as f:
        return f.read()
        
    return None
    
def write_file_content(filename, text):
    with codecs.open(filename, 'w', encoding='utf8') as f:
        f.write(text)

if __name__ == '__main__':
    src_dir = './pptx/base'
    dest_dir = './pptx/temp'
    dest_file = './pptx/temp'
    dest_pptx = './pptx/temp.pptx'
    
    copy_directory(src_dir, dest_dir)
    zip_directory(dest_dir, dest_file)
    rename_file(dest_file + '.zip', dest_pptx)
