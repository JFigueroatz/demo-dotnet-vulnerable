pipeline {
    agent any

    environment {
        DT_URL = 'http://host.docker.internal:8080'
        DT_PROJECT_NAME = 'Demo-DotNet-Vulnerable'
        DT_PROJECT_VERSION = '1.0.0'
    }

    stages {
        stage('Obtener código fuente') {
            steps {
                deleteDir()
                sh 'git clone file:///workspace .'
            }
        }

        stage('Compilar proyecto .NET') {
            steps {
                sh 'dotnet restore src/VulnerableApp/VulnerableApp.csproj'
                sh 'dotnet build src/VulnerableApp/VulnerableApp.csproj --no-restore --configuration Release'
            }
        }

        stage('Generar SBOM') {
            steps {
                sh 'rm -rf artifacts && mkdir -p artifacts'
                sh 'dotnet-CycloneDX src/VulnerableApp/VulnerableApp.csproj --output artifacts --output-format json --configuration Release'
                sh 'test -f artifacts/bom.json'
            }
        }

        stage('Publicar SBOM en Dependency-Track') {
            steps {
                withCredentials([string(credentialsId: 'dtrack-api-key', variable: 'DT_API_KEY')]) {
                    dependencyTrackPublisher(
                        artifact: 'artifacts/bom.json',
                        projectName: env.DT_PROJECT_NAME,
                        projectVersion: env.DT_PROJECT_VERSION,
                        dependencyTrackUrl: env.DT_URL,
                        dependencyTrackApiKey: DT_API_KEY,
                        synchronous: true
                    )
                }
            }
        }

        stage('Generar informe') {
            steps {
                withCredentials([string(credentialsId: 'dtrack-api-key', variable: 'DT_API_KEY')]) {
                    sh 'DT_URL="$DT_URL" DT_PROJECT_NAME="$DT_PROJECT_NAME" DT_API_KEY="$DT_API_KEY" python3 scripts/fetch_results.py'
                }
                sh 'python3 scripts/build_report.py'
                sh 'pandoc report.md -o report.html'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/bom.json,results.json,report.md,report.html', fingerprint: true
        }
    }
}
