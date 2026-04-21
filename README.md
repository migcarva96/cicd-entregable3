# cicd_entregable3

ALB URL Staging: http://calculadora-staging-alb-820526134.us-east-1.elb.amazonaws.com/
ALB URL Production: http://calculadora-production-alb-1937976631.us-east-1.elb.amazonaws.com/

1. Explica brevemente el flujo de trabajo nuevo completo que implementaste con Terraform (commit -> CI -> Build/Push Imagen -> Deploy TF Staging -> Update Service Staging -> Test Staging -> Deploy TF Prod -> Update Service Prod -> Smoke Test Prod). Sé específico sobre qué artefacto se mueve, qué hace cada job principal, y qué valida cada tipo de prueba.

Cada vez que hago un git push a main, el pipeline arranca solo. Primero corre todo el CI: los linters, las pruebas unitarias y el análisis de SonarCloud. Si todo eso pasa, construye la imagen Docker y la sube a Docker Hub.
Después Terraform toma ese SHA y crea o actualiza toda la infraestructura de staging en AWS: el cluster ECS, el ALB, los security groups, la task definition apuntando exactamente a esa imagen. Luego fuerza un nuevo despliegue en ECS y espera a que el contenedor esté corriendo y el health check de /health responda 200.
Con staging estable, corren las pruebas de aceptación contra la URL real del ALB, validando que todo funcione correctamente con operaciones reales. Si esas pruebas pasan, recién ahí el pipeline procede a hacer lo mismo en producción con la misma imagen que ya fue validada. Al final corren las pruebas de humo en producción, que solo verifican que la app cargó y está respondiendo.
                                                                        
2. ¿Qué ventajas y desventajas encontraste al usar Terraform o infraestructura como código en vez de desplegar manualmente? ¿Qué te pareció definir la infraestructura en HCL?
Ventajas: La infraestructura es reproducible, versionada e inmutable — si el cluster se daña, un terraform apply lo recrea idéntico. El mismo main.tf sirve para staging y producción solo cambiando environment_name evitando errores manuales. La destrucción de toda la infra también se puede automatizar para optimizar recursos.                             
Desventajas: Las credenciales temporales de AWS Academy expiran y deben rotarse antes de cada ejecucción.  

3. ¿Qué ventajas y desventajas tiene introducir un entorno de Staging en el pipeline de despliegue a AWS? ¿Cómo impacta esto la velocidad vs. la seguridad del despliegue?
Ventajas: Los bugs de infra o negocio se detectan en staging antes de pasar el deploy a producción ya que los tests de aceptación corren contra infraestructura real en AWS (ALB real, Fargate real, red real) antes de tocar producción. Se puede hacer QA en un entorno de testing seguro y controlado.
Desventajas: El pipeline se demora más ya que todos los checks de terraform se duplican. También implica el doble de costos en AWS y el doble de recursos a mantener.


4. ¿Qué diferencia hay entre las pruebas ejecutadas contra Staging (test-staging) y las ejecutadas contra Producción (smoke-test-production) en tu pipeline? ¿Por qué esta diferencia?
En la etapa de test-staging corren pruebas de aceptación para validar el funcionamiento correcto de la lógica de negocio mientras que en la etapa de smoke-test-production corre solamente test_smoke_test para validar que el servicio esta up y listo para recibir tráfico. Esta diferencia se hace porque se supone que si llega a prod ya las pruebas de aceptación debieron haber pasado.  

5. Considerando un ciclo completo de DevOps, ¿qué partes importantes (fases, herramientas, prácticas) crees que aún le faltan a este pipeline de CI/CD que has construido? (Menciona 2, explica por qué son importantes y cómo podrían implementarse brevemente).
Dos partes importantes a incorporar son la observabilidad y el rollback automático. 
El rollback automatico es por si el smoke test falla, automaticamente se vuelva a desplegar la utlima version estable en produccion. Se podria implementar guardando el tag de la ultima imagen y correr terraform con ese tag.
Y en cuanto a observabilidad se puede integrar cloudwatch para monitorear los errores y latencias de la app y si algo falla que se notifique al correo o a slack

6. ¿Cómo te pareció implementar dos funcionalidades nuevas? ¿Qué tal fue tu experiencia? ¿Encontraste útil implementar CI/CD a la hora de realizar cambios y despliegues? ¿Por qué? ¿Qué no fue tan útil?
Fue facil, luego de hacer el push con las nuevas funcionalidades, no hicimos nada mas y ya todo quedo desplegado en prod.
Si fue util implementar CI/CD ya que cuando realizamos cambios y desplegamos, al ver todos los jobs en verde, ya sabiamos que todas las pruebas pasaron y estan funcionando en produccion o si en algun job fallaba pues tambien era mucho mas facil detectar el problema.
Algo que no fue tan util o nos incomodo un poco, fue que para cualquer cambio toca esperar como 12 minutos a que se despliegue todo