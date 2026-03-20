{{- define "ml-service.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "ml-service.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "ml-service.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
