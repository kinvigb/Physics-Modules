import numpy as np

def find_ensemble_resonances_optimized(structure_ensemble, A, B, w_range, looped=False, loss=0, threshold=1e-7):
    # Store only the previous metric for each structure, initialized to None.
    prev_metrics = {struct: None for struct in structure_ensemble}
    all_resonance_frequencies = []

    for i, w in enumerate(w_range):
        c = np.cos(w + loss * 1j)
        s = np.sin(w + loss * 1j)
        Ta = np.array([[c, 1j * (1/A) * s], [1j * (A) * s, c]], dtype=complex)
        Tb = np.array([[c, 1j *(1/B) * s], [1j * (B) * s, c]], dtype=complex)

        for struct in structure_ensemble:
            T_total = np.eye(2, dtype=complex)
            for cable_type in struct[::-1]:
                if cable_type == 'A':
                    T_total = Ta @ T_total
                elif cable_type == 'B':
                    T_total = Tb @ T_total

            if not looped:
                current_metric = T_total[1, 0].imag
            else:
                identity_matrix = np.eye(2, dtype=complex)
                determinant = np.linalg.det(T_total - identity_matrix)
                current_metric = determinant
            
            prev_metric = prev_metrics[struct]
            
            if prev_metric is not None:
                if prev_metric * current_metric < 0 and \
                   (abs(prev_metric) > threshold or abs(current_metric) > threshold):
                    
                    # Use linear interpolation for a more accurate peak location
                    if current_metric != prev_metric:
                        w_prev = w_range[i-1]
                        w_curr = w_range[i]
                        resonance_freq = w_prev - prev_metric * (w_curr - w_prev) / (current_metric - prev_metric)
                        all_resonance_frequencies.append(np.cos(resonance_freq))
                    else:
                        all_resonance_frequencies.append(np.cos(w_range[i]))

            prev_metrics[struct] = current_metric

    return sorted(list(all_resonance_frequencies))