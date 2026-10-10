# Transfer Matrix Method (TMM)

This repository contains a Python implementation of TMM. It's intended for completing tasks at these university courses:
1. **Modeling of Complex Systems** 
2. **Geometric Modeling**

## Project Structure

1. `pytmm.core` – TMM implementation [1].
2. `pytmm.electrical` – TMM presets for solving electrical circuits [1] (used for testing `pytmm.core`).
3. `pytmm.splines` – Implementation of beam splines [2].

## Getting Started

Install required dependencies:

```
pip install .
```

## Documentation

1. `docs/core/transfer_matrix_method.md` – Transfer matrix method description [1, lecture 1].
2. `docs/core/krylov_method.md` – Krylov method for constructing a transfer matrix for TMM [1, lecture 2].
3. `docs/splines/beam_spline.md` – Beam splines description [2].
4. `docs/splines/beam_spline_smoothing.md` – How to use beam splines for smoothing [2].

## Literature

1. І.В. Ориняк. РОЗРАХУНКИ СКЛАДНИХ СИСТЕМ МЕТОДОМ ПОЧАТКОВИХ ПАРАМЕТРІВ. Рекомендовано Методичною радою КПІ ім. Ігоря Сікорського як навчальний посібник для студентів, які навчаються за спеціальністю 113 «Прикладна математика» Київ, КПІ ім. Ігоря Сікорського, 2022, 252 с. Режим доступу <https://ela.kpi.ua/bitstream/123456789/48744/1/Rozrakhunky_skladnykh_system>
2. І.В. Ориняк. ДИФЕРЕНЦІЙНА ГЕОМЕТРІЯ І СПЛАЙНИ
