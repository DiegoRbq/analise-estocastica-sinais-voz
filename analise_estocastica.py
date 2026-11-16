import subprocess
import imageio_ffmpeg
import numpy as np
import librosa
import scipy.signal as signal
import matplotlib.pyplot as plt

# ==============================================================================
# 0. CONVERSÃO AUTOMÁTICA PARA WAV E CARREGAMENTO DOS SINAIS
# ==============================================================================
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run(
    [ffmpeg_exe, "-y", "-i", "audio_real.aac", "audio_real.wav"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    check=True
)

fs = 16000  # Taxa de amostragem de 16 kHz sugerida no roteiro

x_real, _ = librosa.load("audio_real.wav", sr=fs, mono=True)
x_fake, _ = librosa.load("audio_fake.wav", sr=fs, mono=True)

# Normalização de amplitude (-1 a 1) para comparação justa de variância e potência
x_real = x_real / np.max(np.abs(x_real))
x_fake = x_fake / np.max(np.abs(x_fake))

t_real = np.arange(len(x_real)) / fs
t_fake = np.arange(len(x_fake)) / fs

print(f"Áudio Real: {len(x_real)} amostras | Duração: {t_real[-1]:.2f} s")
print(f"Áudio Fake: {len(x_fake)} amostras | Duração: {t_fake[-1]:.2f} s")

# ==============================================================================
# GRÁFICO 1: SINAIS ORIGINAIS NO DOMÍNIO DO TEMPO (Item 2.1)
# ==============================================================================
fig, axs = plt.subplots(2, 1, figsize=(10, 6))

axs[0].plot(t_real, x_real, color="steelblue", linewidth=0.6)
axs[0].set_title("Sinal de Voz Real - Domínio do Tempo")
axs[0].set_xlabel("Tempo (s)")
axs[0].set_ylabel("Amplitude Normalizada")
axs[0].grid(True, alpha=0.3)

axs[1].plot(t_fake, x_fake, color="darkorange", linewidth=0.6)
axs[1].set_title("Sinal de Voz Sintético (Fake) - Domínio do Tempo")
axs[1].set_xlabel("Tempo (s)")
axs[1].set_ylabel("Amplitude Normalizada")
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("01_sinais_tempo.png", dpi=300)
plt.close()

# ==============================================================================
# GRÁFICO 2: ESTUDO DA ESTACIONARIEDADE WSS EM JANELAS CURTAS (Item 1)
# N = 512 amostras (32 ms a 16 kHz) com sobreposição de 50% (passo = 256)
# ==============================================================================
frame_len = 512
hop_len = 256  # Sobreposição de 50% (256 amostras)

var_real = [np.var(x_real[i:i+frame_len]) for i in range(0, len(x_real) - frame_len, hop_len)]
var_fake = [np.var(x_fake[i:i+frame_len]) for i in range(0, len(x_fake) - frame_len, hop_len)]

mean_real = [np.mean(x_real[i:i+frame_len]) for i in range(0, len(x_real) - frame_len, hop_len)]
mean_fake = [np.mean(x_fake[i:i+frame_len]) for i in range(0, len(x_fake) - frame_len, hop_len)]

t_win_real = np.arange(len(var_real)) * (hop_len / fs)
t_win_fake = np.arange(len(var_fake)) * (hop_len / fs)

fig, axs = plt.subplots(2, 2, figsize=(12, 7))

# Variância por janela
axs[0, 0].plot(t_win_real, var_real, color="steelblue", linewidth=1.2)
axs[0, 0].set_title("Variância por Janela (32 ms) - Voz Real")
axs[0, 0].set_xlabel("Tempo (s)")
axs[0, 0].set_ylabel("Variância")
axs[0, 0].grid(True, alpha=0.3)

axs[0, 1].plot(t_win_fake, var_fake, color="darkorange", linewidth=1.2)
axs[0, 1].set_title("Variância por Janela (32 ms) - Voz Sintética (Fake)")
axs[0, 1].set_xlabel("Tempo (s)")
axs[0, 1].set_ylabel("Variância")
axs[0, 1].grid(True, alpha=0.3)

# Média por janela
axs[1, 0].plot(t_win_real, mean_real, color="steelblue", linewidth=1.0)
axs[1, 0].set_title("Média por Janela (32 ms) - Voz Real")
axs[1, 0].set_xlabel("Tempo (s)")
axs[1, 0].set_ylabel("Média Amostral")
axs[1, 0].set_ylim(-0.05, 0.05)
axs[1, 0].grid(True, alpha=0.3)

axs[1, 1].plot(t_win_fake, mean_fake, color="darkorange", linewidth=1.0)
axs[1, 1].set_title("Média por Janela (32 ms) - Voz Sintética (Fake)")
axs[1, 1].set_xlabel("Tempo (s)")
axs[1, 1].set_ylabel("Média Amostral")
axs[1, 1].set_ylim(-0.05, 0.05)
axs[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("02_estacionariedade_wss.png", dpi=300)
plt.close()

# ==============================================================================
# GRÁFICO 3: FUNÇÃO DE AUTOCORRELAÇÃO Rx(tau) (Item 2)
# ==============================================================================
def autocorr_normalizada(x):
    x_centrado = x - np.mean(x)
    r = np.correlate(x_centrado, x_centrado, mode="full")
    r = r / np.max(np.abs(r))  # Normaliza Rx(0) = 1
    lags = np.arange(-len(x) + 1, len(x)) / fs * 1000  # Atraso tau em ms
    return lags, r

lags_real, r_real = autocorr_normalizada(x_real)
lags_fake, r_fake = autocorr_normalizada(x_fake)

# Zoom na janela de atrasos de -30 ms a +30 ms para visualizar periodicidade (pitch)
mask_real = (lags_real >= -30) & (lags_real <= 30)
mask_fake = (lags_fake >= -30) & (lags_fake <= 30)

fig, axs = plt.subplots(2, 1, figsize=(10, 6))

axs[0].plot(lags_real[mask_real], r_real[mask_real], color="steelblue", linewidth=1.1)
axs[0].set_title("Função de Autocorrelação Normalizada $R_X(\\tau)$ - Voz Real (Zoom ±30 ms)")
axs[0].set_xlabel("Atraso $\\tau$ (ms)")
axs[0].set_ylabel("$R_X(\\tau)$ Normalizada")
axs[0].grid(True, alpha=0.3)

axs[1].plot(lags_fake[mask_fake], r_fake[mask_fake], color="darkorange", linewidth=1.1)
axs[1].set_title("Função de Autocorrelação Normalizada $R_X(\\tau)$ - Voz Sintética (Zoom ±30 ms)")
axs[1].set_xlabel("Atraso $\\tau$ (ms)")
axs[1].set_ylabel("$R_X(\\tau)$ Normalizada")
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("03_autocorrelacao.png", dpi=300)
plt.close()

# ==============================================================================
# GRÁFICO 4: DENSIDADE ESPECTRAL DE POTÊNCIA - PSD VIA WELCH (Item 3)
# ==============================================================================
f_real, psd_real = signal.welch(x_real, fs=fs, nperseg=1024)
f_fake, psd_fake = signal.welch(x_fake, fs=fs, nperseg=1024)

fig, axs = plt.subplots(2, 1, figsize=(10, 7))

# Comparação sobreposta em escala logarítmica (dB/Hz)
axs[0].semilogy(f_real, psd_real, label="Voz Real", color="steelblue", linewidth=1.2)
axs[0].semilogy(f_fake, psd_fake, label="Voz Sintética (Fake)", color="darkorange", linewidth=1.2, alpha=0.85)
axs[0].set_title("Densidade Espectral de Potência (PSD - Método de Welch) - Comparação")
axs[0].set_xlabel("Frequência (Hz)")
axs[0].set_ylabel("PSD ($V^2$/Hz) [Escala Log]")
axs[0].legend()
axs[0].grid(True, which="both", alpha=0.3)

# Diferença espectral em dB/Hz
psd_real_db = 10 * np.log10(psd_real + 1e-12)
psd_fake_db = 10 * np.log10(psd_fake + 1e-12)

axs[1].plot(f_real, psd_real_db, label="Voz Real (dB/Hz)", color="steelblue", linewidth=1.2)
axs[1].plot(f_fake, psd_fake_db, label="Voz Sintética (dB/Hz)", color="darkorange", linewidth=1.2, alpha=0.85)
axs[1].set_title("Densidade Espectral de Potência (PSD) em dB/Hz")
axs[1].set_xlabel("Frequência (Hz)")
axs[1].set_ylabel("Densidade Espectral (dB/Hz)")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("04_psd_welch.png", dpi=300)
plt.close()

print("Análise concluída com sucesso! Os 4 gráficos PNG foram salvos na pasta.")