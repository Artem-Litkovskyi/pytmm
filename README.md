# Transfer Matrix Method (TMM)

This repository contains a Python implementation of TMM. It's intended for completing tasks at these university courses:
1. **Modeling of Complex Systems** 
2. **Geometric Modeling**

## 🧱 Project Structure

1. `tmm_kit.tmm` – TMM implementation [1].
2. `tmm_kit.electrical` – TMM presets for solving electrical circuits [1] (used for testing `tmm`).
3. `tmm_kit.beam_splines` – Implementation of beam splines [2].

## 🚀 Getting Started

1. Install from GitHub:

```
pip install https://github.com/Artem-Litkovskyi/tmm-kit.git
```

2. Import:

```python
import tmm_kit.tmm
```

## 💡 Documentation

1. `docs/tmm` – Transfer matrix method description [1, lecture 1].
2. `docs/tmm` – Krylov method for constructing a transfer matrix for TMM [1, lecture 2].
3. `docs/beam_splines/beam_spline.md` – Beam splines description [2].
4. `docs/beam_splines/beam_spline_smoothing.md` – How to use beam splines for smoothing [2].

## 📚 Literature

1. І.В. Ориняк. РОЗРАХУНКИ СКЛАДНИХ СИСТЕМ МЕТОДОМ ПОЧАТКОВИХ ПАРАМЕТРІВ. Рекомендовано Методичною радою КПІ ім. Ігоря Сікорського як навчальний посібник для студентів, які навчаються за спеціальністю 113 «Прикладна математика» Київ, КПІ ім. Ігоря Сікорського, 2022, 252 с. Режим доступу <https://ela.kpi.ua/bitstream/123456789/48744/1/Rozrakhunky_skladnykh_system>
2. І.В. Ориняк. ДИФЕРЕНЦІЙНА ГЕОМЕТРІЯ І СПЛАЙНИ
