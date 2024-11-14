import os
import shutil
from typing import List, Optional
from streamlit.runtime.uploaded_file_manager import UploadedFile
from pathlib import Path
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from src.core.logger import Logger

class DocumentProcessor:
    """Clase para procesar diferentes tipos de documentos"""
    
    def __init__(self, raw_dir="data/raw", processed_dir="data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self._create_directories()
        self.logger = Logger()
        self.supported_extensions = {
            '.pdf': self._load_pdf,
            '.txt': self._load_text
        }

    def _create_directories(self):
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def save_uploaded_files(self, files: List[UploadedFile]) -> bool:
        try:
            # Limpiar directorio raw
            shutil.rmtree(self.raw_dir)
            os.makedirs(self.raw_dir)

            # Guardar nuevos archivos
            for file in files:
                file_path = os.path.join(self.raw_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            return True
        except Exception as e:
            print(f"Error al guardar archivos: {e}")
            return False 

    def process_file(self, file_path: str) -> List[Document]:
        """
        Procesa un archivo y retorna una lista de documentos.
        
        Args:
            file_path (str): Ruta al archivo a procesar
            
        Returns:
            List[Document]: Lista de documentos procesados
            
        Raises:
            ValueError: Si el formato de archivo no está soportado
            Exception: Si hay un error al procesar el archivo
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
            
            extension = path.suffix.lower()
            if extension not in self.supported_extensions:
                raise ValueError(f"Formato de archivo no soportado: {extension}")
            
            # Llamar al método de carga correspondiente
            documents = self.supported_extensions[extension](path)
            
            self.logger.info(f"Archivo procesado exitosamente: {path.name}")
            return documents
            
        except Exception as e:
            self.logger.error(f"Error procesando archivo {file_path}: {str(e)}")
            raise

    def _load_pdf(self, file_path: Path) -> List[Document]:
        """
        Carga un archivo PDF.
        
        Args:
            file_path (Path): Ruta al archivo PDF
            
        Returns:
            List[Document]: Lista de documentos del PDF
        """
        loader = PyPDFLoader(str(file_path))
        return loader.load()

    def _load_text(self, file_path: Path) -> List[Document]:
        """
        Carga un archivo de texto.
        
        Args:
            file_path (Path): Ruta al archivo de texto
            
        Returns:
            List[Document]: Lista de documentos del archivo de texto
        """
        loader = TextLoader(str(file_path))
        return loader.load()

    def process_directory(self, directory_path: str) -> List[Document]:
        """
        Procesa todos los archivos soportados en un directorio.
        
        Args:
            directory_path (str): Ruta al directorio
            
        Returns:
            List[Document]: Lista de todos los documentos procesados
        """
        try:
            path = Path(directory_path)
            if not path.is_dir():
                raise NotADirectoryError(f"No es un directorio válido: {directory_path}")
            
            documents = []
            for ext in self.supported_extensions:
                for file_path in path.glob(f"**/*{ext}"):
                    try:
                        docs = self.process_file(str(file_path))
                        documents.extend(docs)
                    except Exception as e:
                        self.logger.error(f"Error procesando {file_path}: {str(e)}")
                        continue
            
            return documents
            
        except Exception as e:
            self.logger.error(f"Error procesando directorio {directory_path}: {str(e)}")
            raise