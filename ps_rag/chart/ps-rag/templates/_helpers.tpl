{{- define "ps-rag.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ps-rag.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "ps-rag.labels" -}}
helm.sh/chart: {{ include "ps-rag.name" . }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
{{- end -}}

{{- define "ps-rag.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ps-rag.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "ps-rag.api.name" -}}
{{- printf "%s-api" (include "ps-rag.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ps-rag.chroma.name" -}}
{{- printf "%s-chroma" (include "ps-rag.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ps-rag.chroma.serviceName" -}}
{{- if .Values.chroma.service.name -}}
{{- .Values.chroma.service.name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- include "ps-rag.chroma.name" . -}}
{{- end -}}
{{- end -}}

{{- define "ps-rag.chroma.pvcName" -}}
{{- printf "%s-chroma-pvc" (include "ps-rag.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ps-rag.builderJob.name" -}}
{{- printf "%s-build-vector-db" (include "ps-rag.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "ps-rag.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- if .Values.serviceAccount.name -}}
{{- .Values.serviceAccount.name -}}
{{- else -}}
{{- printf "%s-sa" (include "ps-rag.api.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}
