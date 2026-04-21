# cicd_entregable3

ALB URL Staging: http://calculadora-staging-alb-820526134.us-east-1.elb.amazonaws.com/
ALB URL Production: http://calculadora-production-alb-1937976631.us-east-1.elb.amazonaws.com/

Explica brevemente el flujo de trabajo nuevo completo que implementaste con Terraform (commit -> CI -> Build/Push Imagen -> Deploy TF Staging -> Update Service Staging -> Test Staging -> Deploy TF Prod -> Update Service Prod -> Smoke Test Prod). Sé específico sobre qué artefacto se mueve, qué hace cada job principal, y qué valida cada tipo de prueba.
  0. El pipeline corre con un push a main.
  1. build-test-publish (CI): Corre linters (Black, Pylint, Flake8), pruebas unitarias con pytest, análisis de SonarCloud, y si todo pasa en main, construye y hace push de la imagen a Docker
   Hub con el tag SHA y latest.                             
  - deploy-tf-staging: Toma el SHA del job anterior, hace terraform apply en el workspace de staging (estado en S3 en staging/terraform.tfstate), creando/actualizando el cluster ECS, ALB,  
  security groups y task definition apuntando a esa imagen exacta.                                                                                                                           
  - update-service-staging: Hace aws ecs update-service --force-new-deployment y espera con ecs wait services-stable hasta que el contenedor nuevo esté corriendo y el health check /health
  responda 200.                                                                                                                                                                              
  - test-staging: Con la URL del ALB de staging (output de Terraform), ejecuta test_acceptance_app.py — pruebas end-to-end que validan flujos completos de usuario contra el entorno real
  desplegado.                                                                                                                                                                                
  - deploy-tf-prod / update-service-prod: Mismo proceso que staging pero con key=production/terraform.tfstate, infraestructura completamente separada, usando la misma imagen que ya fue
  validada en staging.                                                                                                                                                                       
  - smoke-test-prod: Ejecuta test_smoke_app.py contra el ALB de producción para confirmar que el servicio arrancó y responde correctamente.
                                                                                                                                             

¿Qué ventajas y desventajas encontraste al usar Terraform o infraestructura como código en vez de desplegar manualmente? ¿Qué te pareció definir la infraestructura en HCL?
Ventajas: La infraestructura es reproducible, versionada e inmutable — si el cluster se daña, un terraform apply lo recrea idéntico. El mismo main.tf sirve para staging y producción solo cambiando environment_name evitando errores manuales. La destrucción de toda la infra también se puede automatizar para optimizar recursos.                                                                                   
Desventajas: Las credenciales temporales de AWS Academy expiran y deben rotarse antes de cada ejecucción.  

¿Qué ventajas y desventajas tiene introducir un entorno de Staging en el pipeline de despliegue a AWS? ¿Cómo impacta esto la velocidad vs. la seguridad del despliegue?
Ventajas: Los bugs de infra o negocio se detectan en staging antes de pasar el deploy a producción ya que los tests de aceptación corren contra infraestructura real en AWS (ALB real, Fargate real, red real) antes de tocar producción. Se puede hacer QA en un entorno de testing seguro y controlado.
Desventajas: El pipeline se demora más ya que todos los checks de terraform se duplican. También implica el doble de costos en AWS y el doble de recursos a mantener.


¿Qué diferencia hay entre las pruebas ejecutadas contra Staging (test-staging) y las ejecutadas contra Producción (smoke-test-production) en tu pipeline? ¿Por qué esta diferencia?
En la etapa de test-staging corren pruebas de aceptación para validar el funcionamiento correcto de la lógica de negocio mientras que en la etapa de smoke-test-production corre solamente test_smoke_test para validar que el servicio esta up y listo para recibir tráfico. Esta diferencia se hace porque se supone que si llega a prod ya las pruebas de aceptación debieron haber pasado.  

Considerando un ciclo completo de DevOps, ¿qué partes importantes (fases, herramientas, prácticas) crees que aún le faltan a este pipeline de CI/CD que has construido? (Menciona 2, explica por qué son importantes y cómo podrían implementarse brevemente).
Dos partes importantes a incorporar son la observabilidad y el rollback automático. 

¿Cómo te pareció implementar dos funcionalidades nuevas? ¿Qué tal fue tu experiencia? ¿Encontraste útil implementar CI/CD a la hora de realizar cambios y despliegues? ¿Por qué? ¿Qué no fue tan útil?