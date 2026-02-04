import PyPDF2
from typing import List, Dict, Any
import os
from pathlib import Path

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file"""
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        chunk_id = 0
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            if not chunk_words:
                continue
                
            chunk_text = ' '.join(chunk_words)
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                'chunk_id': chunk_id,
                'start_word': i,
                'end_word': min(i + self.chunk_size, len(words))
            })
            
            chunks.append({
                'text': chunk_text,
                'metadata': chunk_metadata
            })
            chunk_id += 1
        
        return chunks
    
    def process_directory(self, directory_path: str) -> List[Dict]:
        """Process all documents in a directory"""
        all_chunks = []
        directory = Path(directory_path)
        
        for file_path in directory.rglob('*'):
            if file_path.suffix.lower() in ['.pdf', '.txt']:
                print(f"Processing: {file_path.name}")
                
                # Extract text
                if file_path.suffix.lower() == '.pdf':
                    text = self.extract_text_from_pdf(str(file_path))
                else:
                    text = self.extract_text_from_txt(str(file_path))
                
                # Create metadata
                metadata = {
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'file_type': file_path.suffix.lower()[1:],
                    'file_size': file_path.stat().st_size
                }
                
                # Chunk text
                chunks = self.chunk_text(text, metadata)
                all_chunks.extend(chunks)
        
        return all_chunks