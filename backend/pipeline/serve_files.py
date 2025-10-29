"""
Buongiorno - Servidor de Arquivos
Serve os arquivos gerados pelo pipeline para o frontend React
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    """Handler com CORS habilitado para permitir requisições do React"""
    
    def end_headers(self):
        # Habilita CORS para permitir requisições do localhost:5173
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()
    
    def do_OPTIONS(self):
        """Responde requisições OPTIONS para CORS"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Customiza o log para ser mais legível"""
        print(f"📡 {self.address_string()} - {format % args}")

def main():
    # Muda para a pasta data para servir os arquivos
    if not os.path.exists('data'):
        print("❌ Pasta 'data' não encontrada!")
        print("   Certifique-se de rodar este script na raiz do projeto Buongiorno")
        print(f"   Diretório atual: {os.getcwd()}")
        sys.exit(1)
    
    os.chdir('data')
    
    # Configurações do servidor
    HOST = 'localhost'
    PORT = 8000
    
    # Inicia o servidor
    httpd = HTTPServer((HOST, PORT), CORSRequestHandler)
    
    print("\n" + "="*70)
    print("🌅 BUONGIORNO - SERVIDOR DE ARQUIVOS")
    print("="*70)
    print(f"✅ Servidor iniciado com sucesso!")
    print(f"📡 Servindo em: http://{HOST}:{PORT}")
    print(f"📁 Pasta base: {os.getcwd()}")
    print("\n💡 Arquivos disponíveis:")
    print(f"   - http://{HOST}:{PORT}/predictions/predictions_history.csv")
    print(f"   - http://{HOST}:{PORT}/predictions/prediction_YYYY-MM-DD.txt")
    print(f"   - http://{HOST}:{PORT}/processed/gold_features.csv")
    print("\n⚠️  Mantenha este terminal aberto enquanto usa o frontend")
    print("🛑 Para parar: Ctrl+C")
    print("="*70 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado!")
        httpd.shutdown()

if __name__ == "__main__":
    main()