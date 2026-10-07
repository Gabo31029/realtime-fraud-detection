<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0014-despliegue-local-y-aws.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0014: Docker Compose en local y servicios gestionados en AWS

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

El sistema debe poder levantarse con un solo comando para desarrollo y evaluación, y desplegarse en AWS como
objetivo final.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Docker Compose en local y servicios gestionados en AWS (MSK, ECS Fargate, MemoryDB, RDS, MWAA) definidos con Terraform | El mismo código en ambos entornos, con equivalentes gestionados en la nube | Hay que mantener dos configuraciones |
| Todo en una instancia EC2 con Docker Compose | Idéntico al entorno local | Sin alta disponibilidad y sin aprovechar los servicios gestionados |
| Amazon EKS (Kubernetes) | Estándar para contenedores a gran escala | Complejidad y coste excesivos para el proyecto |

## Decisión

En local, Docker Compose levanta el sistema completo. En AWS, cada componente se ejecuta sobre su servicio gestionado
equivalente y la infraestructura se define como código con Terraform.

## Consecuencias

- La configuración de los servicios se inyecta mediante variables de entorno; en AWS se obtiene de Secrets Manager.
- El entorno de AWS se crea y se destruye bajo demanda para controlar el coste.
