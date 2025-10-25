"""
Buongiorno - Script de teste de dependências
Verifica se todas as bibliotecas necessárias estão instaladas
"""

def test_import(module_name, package_name=None):
    """
    Testa importação de um módulo
    
    Args:
        module_name (str): Nome do módulo para importar
        package_name (str): Nome do pacote para pip (se diferente do módulo)
    """
    if package_name is None:
        package_name = module_name
    
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name:20s} - versão {version}")
        return True
    except ImportError:
        print(f"❌ {package_name:20s} - NÃO INSTALADO")
        print(f"   Instale com: pip install {package_name}")
        return False

def main():
    """Testa todas as dependências"""
    print("\n" + "="*70)
    print("🔍 VERIFICAÇÃO DE DEPENDÊNCIAS - PROJETO BUONGIORNO")
    print("="*70 + "\n")
    
    dependencies = [
        ('pandas', None),
        ('numpy', None),
        ('yfinance', None),
        ('sklearn', 'scikit-learn'),
        ('statsmodels', None),
    ]
    
    results = []
    
    print("📦 Bibliotecas Essenciais:")
    print("-"*70)
    
    for module_name, package_name in dependencies:
        result = test_import(module_name, package_name)
        results.append(result)
    
    print("\n" + "="*70)
    
    # Resumo
    total = len(results)
    installed = sum(results)
    missing = total - installed
    
    if missing == 0:
        print("✅ TODAS AS DEPENDÊNCIAS ESTÃO INSTALADAS!")
        print(f"   {installed}/{total} bibliotecas prontas para uso")
    else:
        print(f"⚠️  FALTAM {missing} DEPENDÊNCIAS!")
        print(f"   {installed}/{total} bibliotecas instaladas")
        print("\n💡 Para instalar tudo de uma vez:")
        print("   pip install pandas numpy yfinance scikit-learn statsmodels")
    
    print("="*70 + "\n")
    
    # Testes adicionais
    if all(results):
        print("🧪 Testando funcionalidades básicas...")
        print("-"*70)
        
        try:
            import pandas as pd
            import numpy as np
            
            # Teste pandas
            df = pd.DataFrame({'A': [1, 2, 3]})
            print(f"✅ Pandas funcionando - DataFrame criado com {len(df)} linhas")
            
            # Teste numpy
            arr = np.array([1, 2, 3])
            print(f"✅ NumPy funcionando - Array criado com {len(arr)} elementos")
            
            # Teste yfinance
            import yfinance as yf
            print(f"✅ yfinance importado - Pronto para buscar dados")
            
            # Teste scikit-learn
            from sklearn.metrics import mean_absolute_error
            print(f"✅ scikit-learn funcionando - Métricas disponíveis")
            
            # Teste statsmodels
            from statsmodels.tsa.arima.model import ARIMA
            print(f"✅ statsmodels funcionando - ARIMA disponível")
            
            print("-"*70)
            print("\n🎉 TUDO PRONTO! Você pode rodar o pipeline agora!")
            print("   Execute: python run_pipeline.py")
            
        except Exception as e:
            print(f"\n⚠️  Erro ao testar funcionalidades: {e}")
    
    print("\n")

if __name__ == "__main__":
    main()
