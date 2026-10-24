# Guía de ciclos TDD y commits (rojo -> verde -> refactor)

**Importante:** la rúbrica pide evidencia en el historial de Git. Para que sea real, cada
integrante debe escribir los commits de sus historias, siguiendo este orden. El código final
de este proyecto sirve de referencia; no copien todo de una vez: construyan cada paso.

## Reparto sugerido (3 integrantes, 2 historias cada uno)
| Integrante | Historias | Revisa las pruebas de |
|---|---|---|
| A | HU-01 y HU-06 | B |
| B | HU-02 y HU-03 | C |
| C | HU-04 y HU-05 | A |
(Con 4 integrantes: una historia con pareja o repartan HU-02/HU-05 en dos.)

## Preparación
```bash
git init && git checkout -b main
git commit --allow-empty -m "chore: estructura inicial del proyecto"
```
Agregar a la docente como colaboradora en GitHub (Settings > Collaborators).

## Ciclo por criterio de aceptación
1. 🔴 Escribir UNA prueba que falle -> `pytest` en rojo -> commit `test:`
2. 🟢 Escribir el mínimo código que la pasa -> `pytest` en verde -> commit `feat:`
3. 🔵 Limpiar sin cambiar comportamiento -> `pytest` sigue verde -> commit `refactor:`

## Secuencia de commits sugerida
**HU-01 (carrito)**
- `test: agregar cantidad válida deja el producto en el carrito (HU-01 CA1)`
- `feat: clase Carrito con agregar y cantidad_de`
- `test: rechazar cantidades 0 y 51 (HU-01 CA2)` -> `feat: validar rango 1..50`
- `test: stock insuficiente con mock de inventario (HU-01 CA3)` -> `feat: consultar inventario y lanzar StockInsuficienteError`
- `test: agregar producto repetido suma cantidades (HU-01 CA4)` -> `feat: acumular cantidades`
- `refactor: constantes CANTIDAD_MINIMA/MAXIMA y errores propios`

**HU-03 (descuento volumen)**
- `test: parametrizada 199.999/200.000/499.999/500.000 (HU-03)` -> `feat: porcentaje_descuento_volumen` -> `refactor: constantes de umbral`

**HU-02 (IVA)**
- `test: IVA según tarifa 0/5/19 (CA1)` -> `feat: liquidar calcula IVA`
- `test: IVA sobre valor con descuento (CA2)` -> `feat: aplicar descuento antes del IVA`
- `test: redondeo 52,5 -> 53` -> `feat: dividir_redondeado` -> `refactor: aritmética entera`

**HU-04 (cupones)**, **HU-05 (envío y total)**, **HU-06 (puntos)**: mismo patrón. Dejen el
ejemplo del enunciado (licuadora, cafés, arroces) como última prueba de integración.

## Revisión entre pares
Cada revisor deja comentarios en un Pull Request (o en el commit) revisando: patrón AAA,
valores límite, nombres que describan comportamiento. Guarden capturas para el informe.

## Ensayo para la sustentación (ciclo en vivo)
Práctica: "CA nuevo: el cupón BIENVENIDA da 15 % solo en la primera compra".
1) escribir test rojo, 2) código mínimo, 3) refactor. Hablen mientras lo hacen.
