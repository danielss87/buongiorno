import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Minus, Calendar, DollarSign, Activity, AlertCircle, Sun, RefreshCw, History, BarChart3 } from 'lucide-react';

const BuongiornoDashboard = () => {
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('prediction'); // 'prediction' ou 'history'
  const [loadingHistory, setLoadingHistory] = useState(false);

  // URL da API (usa variável de ambiente ou localhost como fallback)
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

  // Função para buscar dados da API FastAPI
  const fetchPrediction = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Busca a última previsão da API
      const response = await fetch(`${API_URL}/predictions/latest`);
      
      if (!response.ok) {
        throw new Error('Não foi possível carregar os dados. Verifique se a API está rodando.');
      }
      
      const data = await response.json();
      
      // Formata os dados recebidos
      setPrediction({
        currentDate: new Date(data.prediction_date).toLocaleDateString('pt-BR'),
        targetDate: new Date(data.target_date).toLocaleDateString('pt-BR'),
        targetDay: data.target_day,
        currentPrice: data.current_price,
        predictedPrice: data.predicted_price,
        change: data.change,
        changePct: data.change_pct,
        trend: data.trend,
        modelUsed: data.model_used,
        modelAccuracy: data.model_accuracy,
        confidence: data.confidence
      });
      
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Função para buscar histórico com erros
  const fetchHistory = async () => {
    setLoadingHistory(true);

    try {
      const response = await fetch(`${API_URL}/predictions/history-errors`);

      if (!response.ok) {
        throw new Error('Não foi possível carregar o histórico.');
      }

      const data = await response.json();
      setHistory(data.predictions);
      setLoadingHistory(false);
    } catch (err) {
      console.error('Erro ao buscar histórico:', err);
      setLoadingHistory(false);
    }
  };

  // Carrega dados ao montar o componente
  useEffect(() => {
    fetchPrediction();
    fetchHistory();
  }, []);

  const getTrendIcon = () => {
    if (!prediction) return null;
    if (prediction.trend === 'up') return <TrendingUp className="w-8 h-8" />;
    if (prediction.trend === 'down') return <TrendingDown className="w-8 h-8" />;
    return <Minus className="w-8 h-8" />;
  };

  const getTrendColor = () => {
    if (!prediction) return 'text-gray-600 bg-gray-50 border-gray-200';
    if (prediction.trend === 'up') return 'text-green-600 bg-green-50 border-green-200';
    if (prediction.trend === 'down') return 'text-red-600 bg-red-50 border-red-200';
    return 'text-gray-600 bg-gray-50 border-gray-200';
  };

  const getTrendBadgeColor = () => {
    if (!prediction) return 'bg-gray-100 text-gray-800 border-gray-200';
    if (prediction.trend === 'up') return 'bg-green-100 text-green-800 border-green-200';
    if (prediction.trend === 'down') return 'bg-red-100 text-red-800 border-red-200';
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getTrendText = () => {
    if (!prediction) return 'Carregando...';
    if (prediction.trend === 'up') return 'Alta';
    if (prediction.trend === 'down') return 'Baixa';
    return 'Estável';
  };

  const getInterpretation = () => {
    if (!prediction) return '';
    if (prediction.trend === 'up') {
      if (prediction.changePct > 2) return 'Forte alta esperada! Momento favorável para considerar posições compradas.';
      return 'Alta moderada esperada. Tendência positiva no curto prazo.';
    }
    if (prediction.trend === 'down') {
      if (prediction.changePct < -2) return 'Forte baixa esperada! Cautela recomendada para posições compradas.';
      return 'Baixa moderada esperada. Tendência negativa no curto prazo.';
    }
    return 'O mercado deve permanecer estável, com pouca volatilidade esperada.';
  };

  // Tela de Loading
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-amber-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-600 text-lg">Carregando previsão...</p>
          <p className="text-slate-400 text-sm mt-2">Conectando à API em {API_URL}</p>
        </div>
      </div>
    );
  }

  // Tela de Erro
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg border border-red-200 p-8 max-w-2xl">
          <div className="flex items-center gap-4 mb-4">
            <AlertCircle className="w-12 h-12 text-red-600" />
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Erro ao Carregar Dados</h2>
              <p className="text-slate-600">Não foi possível conectar à API</p>
            </div>
          </div>
          
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800 text-sm">{error}</p>
          </div>

          <div className="space-y-3 mb-6">
            <h3 className="font-semibold text-slate-900">Passos para resolver:</h3>
            <ol className="list-decimal list-inside space-y-2 text-sm text-slate-700">
              <li>Certifique-se de que a API está rodando em: <code className="bg-slate-100 px-2 py-1 rounded">{API_URL}</code></li>
              <li>Abra o Anaconda Prompt e rode: <code className="bg-slate-100 px-2 py-1 rounded">conda activate buongiorno-api</code></li>
              <li>Navegue até: <code className="bg-slate-100 px-2 py-1 rounded">backend/api</code></li>
              <li>Execute: <code className="bg-slate-100 px-2 py-1 rounded">python main.py</code></li>
              <li>Certifique-se de que rodou o pipeline: <code className="bg-slate-100 px-2 py-1 rounded">python run_pipeline.py</code></li>
            </ol>
          </div>

          <button
            onClick={fetchPrediction}
            className="w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-5 h-5" />
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  // Dashboard Principal
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-amber-400 to-yellow-500 rounded-lg flex items-center justify-center shadow-md">
                <Sun className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">Buongiorno</h1>
                <p className="text-sm text-slate-500">Previsão de Preço do Ouro</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Calendar className="w-4 h-4" />
                <span>{prediction.currentDate}</span>
              </div>
              <button
                onClick={() => {
                  fetchPrediction();
                  fetchHistory();
                }}
                className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                title="Atualizar dados"
              >
                <RefreshCw className="w-5 h-5 text-slate-600" />
              </button>
              <div className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full border border-green-200">
                API Conectada
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-1 border-b border-slate-200">
            <button
              onClick={() => setActiveTab('prediction')}
              className={`px-6 py-3 font-medium text-sm border-b-2 transition-colors flex items-center gap-2 ${
                activeTab === 'prediction'
                  ? 'border-amber-500 text-amber-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              Previsão Atual
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-6 py-3 font-medium text-sm border-b-2 transition-colors flex items-center gap-2 ${
                activeTab === 'history'
                  ? 'border-amber-500 text-amber-600'
                  : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
              }`}
            >
              <History className="w-4 h-4" />
              Histórico de Previsões
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Content: Previsão */}
        {activeTab === 'prediction' && (
          <>
            {/* Hero Card - Previsão Principal */}
            <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden mb-6">
              <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-6 text-white">
                <div className="flex items-center gap-3 mb-2">
                  <Calendar className="w-5 h-5 text-amber-400" />
                  <span className="text-sm font-medium text-slate-300">Previsão para</span>
                </div>
                <h2 className="text-3xl font-bold mb-1">
                  {prediction.targetDate} ({prediction.targetDay})
                </h2>
              </div>

              <div className="p-8">
                {/* Preço Previsto - Destaque Principal */}
                <div className="flex items-center justify-between mb-8 pb-8 border-b border-slate-200">
                  <div>
                    <p className="text-sm font-medium text-slate-500 mb-2">Preço Previsto</p>
                    <div className="flex items-baseline gap-3">
                      <span className="text-5xl font-bold text-slate-900">
                        ${prediction.predictedPrice.toFixed(2)}
                      </span>
                      <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border ${getTrendBadgeColor()}`}>
                        {getTrendIcon()}
                        <span className="font-semibold">{getTrendText()}</span>
                      </div>
                    </div>
                  </div>

                  {/* Variação */}
                  <div className={`flex flex-col items-end p-6 rounded-xl border-2 ${getTrendColor()}`}>
                    <p className="text-sm font-medium mb-2">Variação Esperada</p>
                    <div className="text-3xl font-bold">
                      {prediction.change > 0 ? '+' : ''}{prediction.change.toFixed(2)}
                    </div>
                    <div className="text-2xl font-semibold">
                      {prediction.changePct > 0 ? '+' : ''}{prediction.changePct.toFixed(2)}%
                    </div>
                  </div>
                </div>

                {/* Grid de Informações */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  {/* Preço Atual */}
                  <div className="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <div className="flex items-center gap-2 mb-3">
                      <DollarSign className="w-5 h-5 text-slate-600" />
                      <span className="text-sm font-medium text-slate-600">Preço Atual</span>
                    </div>
                    <div className="text-2xl font-bold text-slate-900">
                      ${prediction.currentPrice.toFixed(2)}
                    </div>
                    <p className="text-xs text-slate-500 mt-1">Última atualização: hoje</p>
                  </div>

                  {/* Modelo Usado */}
                  <div className="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <div className="flex items-center gap-2 mb-3">
                      <Activity className="w-5 h-5 text-slate-600" />
                      <span className="text-sm font-medium text-slate-600">Modelo</span>
                    </div>
                    <div className="text-2xl font-bold text-slate-900">
                      {prediction.modelUsed}
                    </div>
                    <p className="text-xs text-slate-500 mt-1">Acurácia: {prediction.modelAccuracy}%</p>
                  </div>

                  {/* Confiança */}
                  <div className="bg-slate-50 rounded-xl p-5 border border-slate-200">
                    <div className="flex items-center gap-2 mb-3">
                      <AlertCircle className="w-5 h-5 text-slate-600" />
                      <span className="text-sm font-medium text-slate-600">Confiança</span>
                    </div>
                    <div className="text-2xl font-bold text-slate-900 capitalize">
                      {prediction.confidence === 'high' ? 'Alta' : prediction.confidence === 'medium' ? 'Média' : 'Baixa'}
                    </div>
                    <div className="flex gap-1 mt-2">
                      <div className={`h-2 w-full rounded ${prediction.confidence === 'high' || prediction.confidence === 'medium' || prediction.confidence === 'low' ? 'bg-green-500' : 'bg-slate-200'}`}></div>
                      <div className={`h-2 w-full rounded ${prediction.confidence === 'high' || prediction.confidence === 'medium' ? 'bg-green-500' : 'bg-slate-200'}`}></div>
                      <div className={`h-2 w-full rounded ${prediction.confidence === 'high' ? 'bg-green-500' : 'bg-slate-200'}`}></div>
                    </div>
                  </div>
                </div>

                {/* Interpretação */}
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
                  <h3 className="text-sm font-semibold text-blue-900 mb-2 flex items-center gap-2">
                    <Activity className="w-4 h-4" />
                    Interpretação da Análise
                  </h3>
                  <p className="text-blue-800 leading-relaxed">
                    {getInterpretation()}
                  </p>
                </div>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
              <div className="flex gap-3">
                <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-amber-900 mb-1">Aviso Importante</h4>
                  <p className="text-sm text-amber-800 leading-relaxed">
                    Esta previsão é baseada em modelos estatísticos e dados históricos. Não constitui recomendação de investimento.
                    O mercado de commodities é volátil e está sujeito a diversos fatores externos não previsíveis por modelos matemáticos.
                  </p>
                </div>
              </div>
            </div>

            {/* Footer Info */}
            <div className="text-center mt-8 text-sm text-slate-500">
              Powered by Buongiorno AI • API REST FastAPI • Dados via Yahoo Finance
            </div>
          </>
        )}

        {/* Tab Content: Histórico */}
        {activeTab === 'history' && (
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
            <div className="bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-6 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <History className="w-5 h-5 text-amber-400" />
                    <span className="text-sm font-medium text-slate-300">Histórico de Previsões</span>
                  </div>
                  <h2 className="text-3xl font-bold mb-1">
                    Previsões vs Resultados Reais
                  </h2>
                  <p className="text-slate-400 text-sm mt-2">
                    Compare as previsões do modelo com os valores reais observados
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-sm text-slate-400">Total de previsões</div>
                  <div className="text-3xl font-bold text-amber-400">{history.length}</div>
                </div>
              </div>
            </div>

            <div className="p-8">
              {loadingHistory ? (
                <div className="text-center py-12">
                  <div className="w-12 h-12 border-4 border-amber-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-slate-600">Carregando histórico...</p>
                </div>
              ) : history.length === 0 ? (
                <div className="text-center py-12">
                  <History className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                  <p className="text-slate-600">Nenhuma previsão no histórico ainda.</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b-2 border-slate-200">
                        <th className="text-left py-4 px-4 text-sm font-semibold text-slate-700">Data Alvo</th>
                        <th className="text-right py-4 px-4 text-sm font-semibold text-slate-700">Previsto</th>
                        <th className="text-right py-4 px-4 text-sm font-semibold text-slate-700">Real</th>
                        <th className="text-right py-4 px-4 text-sm font-semibold text-slate-700">Erro ($)</th>
                        <th className="text-right py-4 px-4 text-sm font-semibold text-slate-700">Erro (%)</th>
                        <th className="text-center py-4 px-4 text-sm font-semibold text-slate-700">Modelo</th>
                        <th className="text-center py-4 px-4 text-sm font-semibold text-slate-700">MAPE</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.slice().reverse().map((item, index) => (
                        <tr
                          key={index}
                          className="border-b border-slate-100 hover:bg-slate-50 transition-colors"
                        >
                          <td className="py-4 px-4">
                            <div className="font-medium text-slate-900">
                              {new Date(item.target_date).toLocaleDateString('pt-BR')}
                            </div>
                            <div className="text-xs text-slate-500">
                              {item.prediction_date ? new Date(item.prediction_date).toLocaleDateString('pt-BR') : '-'}
                            </div>
                          </td>
                          <td className="text-right py-4 px-4 font-medium text-slate-700">
                            ${item.predicted_price?.toFixed(2)}
                          </td>
                          <td className="text-right py-4 px-4 font-medium text-slate-900">
                            {item.real_price !== null ? `$${item.real_price?.toFixed(2)}` : (
                              <span className="text-slate-400 text-sm">Pendente</span>
                            )}
                          </td>
                          <td className={`text-right py-4 px-4 font-semibold ${
                            item.error_abs === null ? 'text-slate-400' :
                            Math.abs(item.error_abs) < 20 ? 'text-green-600' :
                            Math.abs(item.error_abs) < 50 ? 'text-yellow-600' :
                            'text-red-600'
                          }`}>
                            {item.error_abs !== null ? (
                              `${item.error_abs > 0 ? '+' : ''}${item.error_abs.toFixed(2)}`
                            ) : '-'}
                          </td>
                          <td className={`text-right py-4 px-4 font-semibold ${
                            item.error_pct === null ? 'text-slate-400' :
                            Math.abs(item.error_pct) < 1 ? 'text-green-600' :
                            Math.abs(item.error_pct) < 2 ? 'text-yellow-600' :
                            'text-red-600'
                          }`}>
                            {item.error_pct !== null ? (
                              `${item.error_pct > 0 ? '+' : ''}${item.error_pct.toFixed(2)}%`
                            ) : '-'}
                          </td>
                          <td className="text-center py-4 px-4">
                            <span className="inline-block bg-slate-100 text-slate-700 text-xs font-medium px-2 py-1 rounded uppercase">
                              {item.model_used}
                            </span>
                          </td>
                          <td className="text-center py-4 px-4">
                            <span className={`inline-block text-xs font-medium px-2 py-1 rounded ${
                              item.model_mape < 1 ? 'bg-green-100 text-green-800' :
                              item.model_mape < 2 ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {item.model_mape?.toFixed(2)}%
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Estatísticas Resumidas */}
              {history.length > 0 && history.filter(h => h.error_abs !== null).length > 0 && (
                <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="bg-blue-50 rounded-xl p-4 border border-blue-200">
                    <div className="text-sm font-medium text-blue-900 mb-1">Erro Médio Absoluto</div>
                    <div className="text-2xl font-bold text-blue-600">
                      ${(history.filter(h => h.error_abs !== null).reduce((sum, h) => sum + Math.abs(h.error_abs), 0) / history.filter(h => h.error_abs !== null).length).toFixed(2)}
                    </div>
                  </div>
                  <div className="bg-green-50 rounded-xl p-4 border border-green-200">
                    <div className="text-sm font-medium text-green-900 mb-1">Previsões Precisas</div>
                    <div className="text-2xl font-bold text-green-600">
                      {history.filter(h => h.error_abs !== null && Math.abs(h.error_pct) < 1).length}/{history.filter(h => h.error_abs !== null).length}
                    </div>
                    <div className="text-xs text-green-700 mt-1">
                      {((history.filter(h => h.error_abs !== null && Math.abs(h.error_pct) < 1).length / history.filter(h => h.error_abs !== null).length) * 100).toFixed(1)}% com erro {'<'} 1%
                    </div>
                  </div>
                  <div className="bg-purple-50 rounded-xl p-4 border border-purple-200">
                    <div className="text-sm font-medium text-purple-900 mb-1">Erro Médio %</div>
                    <div className="text-2xl font-bold text-purple-600">
                      {(history.filter(h => h.error_pct !== null).reduce((sum, h) => sum + Math.abs(h.error_pct), 0) / history.filter(h => h.error_pct !== null).length).toFixed(2)}%
                    </div>
                  </div>
                  <div className="bg-amber-50 rounded-xl p-4 border border-amber-200">
                    <div className="text-sm font-medium text-amber-900 mb-1">Maior Erro</div>
                    <div className="text-2xl font-bold text-amber-600">
                      ${Math.max(...history.filter(h => h.error_abs !== null).map(h => Math.abs(h.error_abs))).toFixed(2)}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BuongiornoDashboard;