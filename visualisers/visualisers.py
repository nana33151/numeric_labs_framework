import matplotlib.pyplot as plt
from base.data_models import VisualiserConfiguration
import numpy as np


def approximation_visualise(task_config: VisualiserConfiguration, times = None):
    steps = np.log10(task_config.steps)
    errors = task_config.log_errors
    print(errors)
    fig, axs = plt.subplots(nrows = 3)
    axs[0].plot(steps, errors, label = 'Зависимость порядка ошибки от порядка шага')
    axs[0].set_xlabel('Логарифм шага', fontsize=12)
    axs[0].set_ylabel('Логарифм ошибки', fontsize=12)
    if times != None:
        axs[1].plot(steps, times, label = 'Зависимость времени выполнения от порядка шага')
    best = task_config.best_responce
    sort_idx = np.argsort(best.test_grid)
    x_sorted = best.test_grid[sort_idx]
    y_true_sorted = best.true_values[sort_idx]
    y_pred_sorted = best.interpolated[sort_idx]
    axs[1].plot(x_sorted, y_true_sorted, 'k-', linewidth=2, label='Истинная функция $f(x)$')
    axs[1].plot(x_sorted, y_pred_sorted, '--', color='royalblue', label=f'Интерполяция (лучший шаг $h={best.step}$)')
    axs[1].scatter(best.x_nodes, task_config.task_config.f(best.x_nodes), color='red', s=30, zorder=5, label='Узлы интерполяции')
    
    axs[1].set_title(f'Сравнение решений на отрезке [{task_config.task_config.bounds[0]}, {task_config.task_config.bounds[1]}]')
    axs[1].set_xlabel('$x$')
    axs[1].set_ylabel('$y$')
    axs[1].grid(True, linestyle='--', alpha=0.7)
    axs[1].legend()

    plt.tight_layout()
    plt.show()
    plt.show()

import matplotlib.pyplot as plt
import numpy as np
from base.data_models import VisualiserConfiguration


# сопоставление имени схемы -> (порядок производной, группа, подпись)
SCHEMA_META = {
    'first_der_right':   (1, 'first',   'правая $O(h)$'),
    'first_der_centr':   (1, 'first',   'центральная $O(h^2)$'),
    'second_der_right2': (2, 'second2', 'правая $O(h^2)$'),
    'second_der_centr2': (2, 'second2', 'центральная $O(h^2)$'),
    'second_der_right4': (2, 'second4', 'правая $O(h^4)$'),
    'second_der_centr4': (2, 'second4', 'центральная $O(h^4)$'),
}

TRUE_FN_LABEL = {1: "$f'(x)$", 2: "$f''(x)$"}


def derivative_visualise(task_config: VisualiserConfiguration, times=None):
    steps = np.asarray(task_config.steps, dtype=float)
    log_errors = task_config.log_errors       # dict {name: array}
    best = task_config.best_responce
    cfg = task_config.task_config

    order_steps = np.argsort(steps)
    steps_sorted = steps[order_steps]

    # --- фигура: 3 строки x 2 столбца ---
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(13, 11))

    # ---------- 1. Ошибка от шага (по схемам) ----------
    ax_err = axs[0, 0]
    if isinstance(log_errors, dict):
        for name, errs in log_errors.items():
            errs = np.asarray(errs, dtype=float)[order_steps]
            label = SCHEMA_META.get(name, (None, None, name))[2]
            ax_err.plot(np.log10(steps_sorted), np.log10(errs),
                        'o-', label=label)
    else:
        # совместимость: если кто-то передал массив (интерполяция)
        ax_err.plot(np.log10(steps_sorted),
                    np.log10(np.asarray(log_errors, dtype=float)[order_steps]),
                    'o-', label='error')
    ax_err.set_xlabel('$\\log_{10} h$', fontsize=11)
    ax_err.set_ylabel('$\\log_{10}(\\mathrm{error})$', fontsize=11)
    ax_err.set_title('Зависимость ошибки от шага')
    ax_err.grid(True, linestyle='--', alpha=0.7)
    ax_err.legend(fontsize=8)

    # ---------- 2. Время выполнения (опционально) ----------
    ax_time = axs[0, 1]
    if times is not None:
        ax_time.plot(np.log10(steps_sorted),
                     np.asarray(times, dtype=float)[order_steps],
                     's-', color='darkorange', label='время')
        ax_time.legend(fontsize=8)
    ax_time.set_xlabel('$\\log_{10} h$', fontsize=11)
    ax_time.set_ylabel('время, с', fontsize=11)
    ax_time.set_title('Время выполнения')
    ax_time.grid(True, linestyle='--', alpha=0.7)

    # ---------- 3. f(x) ----------
    ax_f = axs[1, 0]
    a, b = cfg.bounds
    x_full = np.linspace(a, b, 400)
    y_full = np.array([cfg.f(x) for x in x_full])
    ax_f.plot(x_full, y_full, 'k-', linewidth=2, label='$f(x)$')
    ax_f.set_title('Исходная функция')
    ax_f.set_xlabel('$x$')
    ax_f.set_ylabel('$y$')
    ax_f.grid(True, linestyle='--', alpha=0.7)
    ax_f.legend()

    # ---------- группируем кривые ----------
    groups = {'first': [], 'second2': [], 'second4': []}
    for c in best.curves:
        meta = SCHEMA_META.get(c.name)
        if meta is None:
            continue
        order, group, label = meta
        groups[group].append((label, order, c))

    # ---------- 4. f'(x) ----------
    ax_d1 = axs[1, 1]
    _plot_group(ax_d1, groups['first'], order=1, config=cfg,
                title="$f'(x)$: схемы")
    ax_d1.set_xlabel('$x$')
    ax_d1.set_ylabel('$y$')
    ax_d1.grid(True, linestyle='--', alpha=0.7)
    ax_d1.legend(fontsize=8)

    # ---------- 5. f''(x), O(h²) ----------
    ax_d2 = axs[2, 0]
    _plot_group(ax_d2, groups['second2'], order=2, config=cfg,
                title="$f''(x)$: схемы $O(h^2)$")
    ax_d2.set_xlabel('$x$')
    ax_d2.set_ylabel('$y$')
    ax_d2.grid(True, linestyle='--', alpha=0.7)
    ax_d2.legend(fontsize=8)

    # ---------- 6. f''(x), O(h⁴) ----------
    ax_d4 = axs[2, 1]
    _plot_group(ax_d4, groups['second4'], order=2, config=cfg,
                title="$f''(x)$: схемы $O(h^4)$")
    ax_d4.set_xlabel('$x$')
    ax_d4.set_ylabel('$y$')
    ax_d4.grid(True, linestyle='--', alpha=0.7)
    ax_d4.legend(fontsize=8)

    fig.suptitle(
        f'Производные на отрезке [{a}, {b}], лучший шаг $h={best.step}$',
        fontsize=13,
    )
    plt.tight_layout()
    plt.show()


def _plot_group(ax, curves, order, config, title):
    """Рисует эталонную производную + предсказания всех схем группы."""
    if not curves:
        ax.set_title(title)
        return

    # эталон — на самой широкой x-сетке из группы
    x_ref = max((c.x for _, _, c in curves), key=len)
    true_fn = (config.first_analitical_der if order == 1
               else config.second_analitical_der)
    y_ref = np.array([true_fn(xi) for xi in x_ref])
    ax.plot(x_ref, y_ref, 'k-', linewidth=2, label=TRUE_FN_LABEL[order])

    # предсказания схем
    for label, _, c in curves:
        ax.plot(c.x, c.y_pred, '--', label=label)

    ax.set_title(title)

def solving():
    pass

def cauchy():
    pass

def bvp():
    pass

def pde():
    pass