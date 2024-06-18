import numpy as np
from scipy.fftpack import dct, idct
import time
import queue

def dct2_manual(matrix):
    N = matrix.shape[0]
    result = np.zeros_like(matrix, dtype=np.float32)
    for u in range(N):
        for v in range(N):
            sum_val = 0
            for x in range(N):
                for y in range(N):
                    sum_val += matrix[x, y] * np.cos(np.pi * u * (2 * x + 1) / (2 * N)) * np.cos(np.pi * v * (2 * y + 1) / (2 * N))
            alpha_u = np.sqrt(1/N) if u == 0 else np.sqrt(2/N)
            alpha_v = np.sqrt(1/N) if v == 0 else np.sqrt(2/N)
            result[u, v] = alpha_u * alpha_v * sum_val
    return result

def idct2_manual(matrix):
    N = matrix.shape[0]
    result = np.zeros_like(matrix, dtype=np.float32)
    for x in range(N):
        for y in range(N):
            sum_val = 0
            for u in range(N):
                for v in range(N):
                    alpha_u = np.sqrt(1/N) if u == 0 else np.sqrt(2/N)
                    alpha_v = np.sqrt(1/N) if v == 0 else np.sqrt(2/N)
                    sum_val += alpha_u * alpha_v * matrix[u, v] * np.cos(np.pi * u * (2 * x + 1) / (2 * N)) * np.cos(np.pi * v * (2 * y + 1) / (2 * N))
            result[x, y] = sum_val
    return result

def dct2(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def idct2(matrix):
    return idct(idct(matrix.T, norm='ortho').T, norm='ortho')

def compare_dct2_algorithms(progress_queue, plot_queue):
    sizes = [8, 16, 32]
    manual_times = []
    library_times = []
    iterations = 10  # Numero di iterazioni per mediare i tempi

    total_steps = len(sizes) * 2
    step = 0
    
    for size in sizes:
        print("size: ", size)
        matrix = np.random.rand(size, size).astype(np.float32)
        
        # Misurazione dei tempi per l'algoritmo manuale
        start_time = time.time()
        for _ in range(iterations):
            dct2_manual(matrix)
        manual_times.append((time.time() - start_time) / iterations)
        step += 1
        progress_queue.put((step / total_steps) * 100)
        
        # Misurazione dei tempi per l'algoritmo della libreria
        start_time = time.time()
        for _ in range(iterations):
            dct2(matrix)
        library_times.append((time.time() - start_time) / iterations)
        step += 1
        progress_queue.put((step / total_steps) * 100)
    print("Sizes: ", sizes)
    print("Manual times: ", manual_times)
    print("Library times: ", library_times)

    progress_queue.put("done")
    plot_queue.put((sizes, manual_times, library_times))