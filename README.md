# Análise Estocástica e Espectral de Sinais de Voz: Humano vs. IA (TTS)

Repositório desenvolvido para a disciplina de **Processos Estocásticos para Engenharia** (Engenharia de Telecomunicações - UFSJ / Campus Alto Paraopeba). O objetivo principal é investigar o comportamento estatístico e espectral de sinais de voz, comparando uma gravação humana real com uma locução gerada artificialmente por inteligência artificial (Text-to-Speech - TTS).

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas
O script foi desenvolvido em **Python**, fazendo uso de bibliotecas robustas de processamento de sinais e computação científica:
* `numpy` — Manipulação de arrays e cálculos estatísticos (média e variância).
* `scipy.signal` — Estimação da Densidade Espectral de Potência (PSD) via método de Welch e correlação.
* `librosa` — Carregamento, reamostragem (16 kHz) e conversão de áudio para mono.
* `matplotlib` — Geração de gráficos analíticos em alta resolução (300 DPI).

---

## 📋 Metodologia e Etapas da Análise

1. **Pré-processamento:** Normalização de amplitude no intervalo [-1, 1] e reamostragem padronizada para $f_s = 16\text{ kHz}$ de ambos os áudios.
2. **Estudo da Estacionariedade (WSS):** Divisão dos sinais em janelas curtas de 32 ms ($N = 512$ amostras com 50% de sobreposição) para avaliar a variância e a média local ao longo do tempo.
3. **Função de Autocorrelação:** Avaliação da dependência temporal e identificação do período fundamental (pitch, $T_0 \approx 7\text{ ms}$) na voz humana em contraste com o amortecimento na voz sintética.
4. **Densidade Espectral de Potência (PSD):** Aplicação do periodograma de Welch (`nperseg=1024`) para mapear a distribuição de energia no domínio da frequência, evidenciando artefatos de vocoders neurais na faixa de 1,2 kHz a 4,2 kHz.

---

## 📂 Estrutura de Arquivos
* `analise_estocastica.py` : Script principal contendo toda a pipeline de processamento e plotagem.
* `Trabalho_Processos_Estocasticos_Diego_Rodrigues_2.pdf` : Relatório técnico acadêmico completo com a fundamentação teórica, gráficos gerados e discussão dos resultados.

---

## 📊 Resultados e Análise Gráfica

### 1. Sinais no Domínio do Tempo
<p align="center">
  <img src="01_sinais_tempo.png" width="85%" alt="Sinais no Tempo">
</p>
<p align="center">
  <em><b>Análise:</b> Compara a amplitude normalizada e o comportamento temporal bruto de uma gravação de voz humana real com a locução gerada por Inteligência Artificial (TTS).</em>
</p>

---

### 2. Estudo da Estacionariedade (WSS)
<p align="center">
  <img src="02_estacionariedade_wss.png" width="85%" alt="Estacionariedade WSS">
</p>
<p align="center">
  <em><b>Análise:</b> Avaliação da variação da média e da variância local utilizando janelas curtas de 32 ms (50% de sobreposição), permitindo verificar o perfil de estacionariedade dos sinais.</em>
</p>

---

### 3. Função de Autocorrelação
<p align="center">
  <img src="03_autocorrelacao.png" width="85%" alt="Autocorrelação">
</p>
<p align="center">
  <em><b>Análise:</b> Destaca a periodicidade e identifica o período fundamental (pitch, aproximadamente 7 ms) na voz humana em contraste direto com o comportamento do sinal sintético.</em>
</p>

---

### 4. Densidade Espectral de Potência (PSD - Método de Welch)
<p align="center">
  <img src="04_psd_welch.png" width="85%" alt="PSD Welch">
</p>
<p align="center">
  <em><b>Análise:</b> Mapeia a distribuição de energia no domínio da frequência utilizando o periodograma de Welch, evidenciando claramente os artefatos característicos de vocoders neurais.</em>
</p>

---

## 🚀 Como Executar o Código

1. Certifique-se de ter o Python instalado junto com as dependências necessárias:
   ```bash
   pip install numpy scipy librosa matplotlib imageio-ffmpeg
