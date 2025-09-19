import numpy as np

def find_ensemble_resonances_optimized(structure_ensemble, A, B, w_range, looped=False, loss=0):
    live_metrics = {struct: [None, None] for struct in structure_ensemble}
    all_resonance_frequencies = []

    for i, w in enumerate(w_range):
        c = np.cos(w + loss * 1j)
        s = np.sin(w + loss * 1j)
        Ta = np.array([[c, 1j * A * s], [1j * (1/A) * s, c]], dtype=complex)
        Tb = np.array([[c, 1j * B * s], [1j * (1/B) * s, c]], dtype=complex)
        for struct in structure_ensemble:
            T_total = np.eye(2, dtype=complex)
            for cable_type in struct:
                if cable_type == 'A':
                    T_total = Ta @ T_total
                elif cable_type == 'B':
                    T_total = Tb @ T_total

            if not looped:
                metric = T_total[1, 0].real
            else:
                identity_matrix = np.eye(2, dtype=complex)
                determinant = np.linalg.det(T_total - identity_matrix)
                metric = determinant.real
            
            live_metrics[struct][0] = live_metrics[struct][1]
            live_metrics[struct][1] = metric

            if i > 0:
                prev_metric, current_metric = live_metrics[struct]

                if prev_metric * current_metric < 0:
                    resonance_freq = (w_range[i-1] + w_range[i]) / 2.0
                    all_resonance_frequencies.append(resonance_freq)
                elif np.isclose(current_metric, 0):
                    all_resonance_frequencies.append(w)

    return sorted(list(set(all_resonance_frequencies)))