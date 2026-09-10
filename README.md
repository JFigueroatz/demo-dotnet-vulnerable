# Analisis de vulnerabilidades .NET con Jenkins y Dependency-Track

## Descripcion

Este proyecto demuestra un analisis de vulnerabilidades de dependencias NuGet utilizando un pipeline de Jenkins, un SBOM CycloneDX, Dependency-Track y Pandoc.

Las dependencias antiguas se utilizan exclusivamente con fines educativos para demostrar la deteccion de vulnerabilidades. No deben utilizarse en produccion.

## Objetivo

Automatizar el siguiente proceso:

```text
Codigo fuente .NET
    -> compilacion
    -> SBOM CycloneDX
    -> Dependency-Track
    -> resultados de vulnerabilidades
    -> informe Markdown/HTML con Pandoc
```

## Tecnologias utilizadas

- .NET SDK 10
- Jenkins 2.568.3
- Dependency-Track 5.1.0
- PostgreSQL 18
- Docker Desktop y Docker Compose
- CycloneDX .NET 6.2.0
- Pandoc 3.1.11.1
- Git y GitHub

## Dependencias analizadas

El proyecto `src/VulnerableApp/VulnerableApp.csproj` contiene versiones antiguas de paquetes NuGet:

| Componente | Version |
|---|---:|
| log4net | 2.0.5 |
| Newtonsoft.Json | 6.0.8 |
| SharpZipLib | 0.86.0 |
| System.Text.Encodings.Web | 4.7.0 |

Estas dependencias tienen vulnerabilidades conocidas y fueron seleccionadas para fines de laboratorio.

## SBOM

SBOM significa Software Bill of Materials. Es el inventario de componentes que forman parte de una aplicacion.

CycloneDX genera el archivo `bom.json`, que contiene los nombres, versiones e identificadores de las dependencias. Dependency-Track utiliza este archivo para relacionar los componentes con vulnerabilidades conocidas.

## Arquitectura

Docker Compose levanta los siguientes servicios:

| Servicio | Acceso |
|---|---|
| Jenkins | http://localhost:8082 |
| Dependency-Track | http://localhost:8081 |
| API de Dependency-Track | http://localhost:8080 |
| PostgreSQL | Red interna de Docker |

Jenkins utiliza una imagen personalizada definida en `Dockerfile.jenkins`. Esta imagen incluye .NET, Git, Python, CycloneDX y Pandoc.

## Ejecucion del entorno

Requisitos:

- Docker Desktop iniciado.
- Docker Compose disponible.

Iniciar los servicios:

```bash
docker compose up -d
```

Ver el estado:

```bash
docker compose ps
```

Detener los servicios:

```bash
docker compose down
```

## Configuracion de Dependency-Track

1. Crear el proyecto `Demo-DotNet-Vulnerable`.
2. Usar la version `1.0.0`.
3. Crear un equipo para Jenkins.
4. Generar una API Key con permisos de carga y lectura.
5. Guardar la API Key como credencial secreta en Jenkins con el ID `dtrack-api-key`.
6. Habilitar la fuente OSV/ETC para obtener avisos de paquetes NuGet.

Las credenciales no deben incluirse en este repositorio.

## Pipeline de Jenkins

El archivo `Jenkinsfile` define estas etapas:

1. Clonar el repositorio remoto de GitHub.
2. Restaurar las dependencias .NET.
3. Compilar el proyecto.
4. Generar el SBOM `artifacts/bom.json` con CycloneDX.
5. Publicar el SBOM en Dependency-Track.
6. Consultar los hallazgos mediante la API.
7. Generar `results.json`.
8. Convertir los resultados a `report.md`.
9. Convertir Markdown a HTML con Pandoc.
10. Archivar los resultados como artefactos del build.

## Configuracion del trabajo Jenkins

Crear un trabajo de tipo Pipeline con estos valores:

```text
Repository URL: https://github.com/JFigueroatz/demo-dotnet-vulnerable.git
Branch: */master
Script Path: Jenkinsfile
```

Ejecutar el trabajo con **Build Now** y revisar la consola. Una ejecucion correcta termina con:

```text
Finished: SUCCESS
```

## Resultados obtenidos

El analisis detecto seis vulnerabilidades:

| Severidad | Cantidad |
|---|---:|
| Critica | 2 |
| Alta | 2 |
| Media | 2 |
| Baja | 0 |

Componentes analizados: 4.

La puntuacion de riesgo mostrada por Dependency-Track fue 36.

## Artefactos generados

Cada build exitoso conserva:

- `bom.json`: SBOM CycloneDX.
- `results.json`: resultados consultados desde Dependency-Track.
- `report.md`: informe fuente en Markdown.
- `report.html`: informe final generado con Pandoc.

## Recomendaciones

- Actualizar las dependencias a versiones soportadas y corregidas.
- Revisar cada identificador de vulnerabilidad en su fuente correspondiente.
- Ejecutar nuevamente el pipeline despues de actualizar una dependencia.
- No utilizar las versiones vulnerables en entornos productivos.

## Limitaciones

El analisis se enfoca en las dependencias declaradas en el SBOM. No sustituye una prueba de penetracion, un analisis estatico del codigo ni una auditoria completa de seguridad.

Las dependencias vulnerables de este repositorio forman parte de un laboratorio controlado.

## Enlaces

- Repositorio: https://github.com/JFigueroatz/demo-dotnet-vulnerable
- Jenkins local: http://localhost:8082/job/Pipeline-DotNet-DependencyTrack/
- Dependency-Track local: http://localhost:8081
