import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Minus, Calendar, DollarSign, Activity, AlertCircle, Sun } from 'lucide-react';

const BuongiornoDashboard = () => {
  // Dados mock para validação visual
  const [prediction] = useState({
    currentDate: '24/10/2025',
    targetDate: '25/10/2025',
    targetDay: 'Sábado',
    currentPrice: 2734.50,
    predictedPrice: 2748.30,
    change: 13.80,
    changePct: 0.50,
    trend: 'up', // 'up', 'down', 'stable'
    modelUsed: 'ARIMA',
    modelAccuracy: 99.53,
    confidence: 'high' // 'high', 'medium', 'low'
  });

  const getTrendIcon = () => {
    if (prediction.trend === 'up') return <TrendingUp className="w-8 h-8" />;
    if (prediction.trend === 'down') return <TrendingDown className="w-8 h-8" />;
    return <Minus className="w-8 h-8" />;
  };

  const getTrendColor = () => {
    if (prediction.trend === 'up') return 'text-green-600 bg-green-50 border-green-200';
    if (prediction.trend === 'down') return 'text-red-600 bg-red-50 border-red-200';
    return 'text-gray-600 bg-gray-50 border-gray-200';
  };

  const getTrendBadgeColor = () => {
    if (prediction.trend === 'up') return 'bg-green-100 text-green-800 border-green-200';
    if (prediction.trend === 'down') return 'bg-red-100 text-red-800 border-red-200';
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getTrendText = () => {
    if (prediction.trend === 'up') return 'Alta';
    if (prediction.trend === 'down') return 'Baixa';
    return 'Estável';
  };

  const getInterpretation = () => {
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
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Calendar className="w-4 h-4" />
              <span>{prediction.currentDate}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
          Powered by Buongiorno AI • Dados atualizados em tempo real via Yahoo Finance
        </div>
      </div>
    </div>
  );
};

export default BuongiornoDashboard;