---
layout: default
title: API Reference
---

<div id="swagger-ui"></div>
<link href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.28.0/swagger-ui.css" rel="stylesheet">
<link href="/assets/css/api-reference.css" rel="stylesheet">
<script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
<script>
  SwaggerUIBundle({
    url: "https://raw.githubusercontent.com/bob-cd/bob/queue/apiserver/src/main/resources/bob/api.yaml",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIBundle.SwaggerUIStandalonePreset
    ],
    layout: "BaseLayout"
  })
</script>