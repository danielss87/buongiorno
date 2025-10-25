"""
Buongiorno - Verificação de estrutura do projeto
Checa se todos os arquivos e pastas estão nos lugares corretos
"""

import os
from pathlib import Path

def check_exists(path, item_type="file"):
    """Verifica se arquivo ou pasta existe"""
    exists = os.path.exists(path)
    icon = "✅" if exists else "❌"
    type_label = "📁" if item_type == "folder" else "📄"
    status = "OK" if exists else "FALTANDO"
    print(f"{icon} {type_label} {path:50s} [{status}]")
    return exists

def main():
    print("\n" + "="*80)
    print("🔍 VERIFICAÇÃO DE ESTRUTURA - PROJETO BUONGIORNO")
    print("="*80 + "\n")
    
    # Lista de verificação
    checks = {
        'folders': [
            'data',
            'data/raw',
            'data/processed',
            'src',
            'src/data',
            'src/features',
            'src/models',
        ],
        'files': [
            'run_pipeline.py',
            'src/__init__.py',
            'src/data/__init__.py',
            'src/data/fetch_data.py',
            'src/data/preprocess.py',
            'src/features/__init__.py',
            'src/features/build_features.py',
            'src/models/__init__.py',
            'src/models/models.py',
        ]
    }
    
    results = {'folders': [], 'files': []}
    
    # Verifica pastas
    print("📁 PASTAS:")
    print("-"*80)
    for folder in checks['folders']:
        result = check_exists(folder, "folder")
        results['folders'].append(result)
    
    print("\n📄 ARQUIVOS:")
    print("-"*80)
    for file in checks['files']:
        result = check_exists(file, "file")
        results['files'].append(result)
    
    # Resumo
    print("\n" + "="*80)
    total_folders = len(results['folders'])
    ok_folders = sum(results['folders'])
    total_files = len(results['files'])
    ok_files = sum(results['files'])
    
    print(f"📊 RESUMO:")
    print(f"   Pastas:   {ok_folders}/{total_folders} OK")
    print(f"   Arquivos: {ok_files}/{total_files} OK")
    
    if ok_folders == total_folders and ok_files == total_files:
        print("\n🎉 ESTRUTURA PERFEITA! Você pode rodar o pipeline!")
        print("   Execute: python run_pipeline.py")
    else:
        print("\n⚠️  Alguns itens estão faltando!")
        print("\n💡 AÇÕES NECESSÁRIAS:")
        
        if ok_folders < total_folders:
            print("\n   Criar pastas faltantes:")
            for i, folder in enumerate(checks['folders']):
                if not results['folders'][i]:
                    print(f"      mkdir {folder}")
        
        if ok_files < total_files:
            print("\n   Criar/mover arquivos faltantes:")
            for i, file in enumerate(checks['files']):
                if not results['files'][i]:
                    if '__init__.py' in file:
                        print(f"      type nul > {file}  # Windows")
                    else:
                        print(f"      Copie o código para: {file}")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
