### Eureka

- [ ] Consistency（一致性）

- [x] Availability（可用性）
- [x] Partition tolerance（分区容错性）

eureka 2.x discontinued

#### Server

- self preservation mode, default enabled, not recommend to turn off
- when enable, do not remove an service when it failed to register due to some issues like network broken.
- turn off self preservation:

```yaml
server:
  enable-self-preservation: false
```

http://cloud.spring.io/spring-cloud-netflix/single/spring-cloud-netflix.html#spring-cloud-eureka-server

#### Client

- no need @EnableEurekaClient if have **spring-cloud-starter-netflix-eureka-client** on classpath

```yaml
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
```

http://cloud.spring.io/spring-cloud-netflix/single/spring-cloud-netflix.html#netflix-eureka-client-starter



### Ribbon

Client Side Load Balancer: https://cloud.spring.io/spring-cloud-netflix/multi/multi_spring-cloud-ribbon.html

- RestTemplate

```java
@Bean
@LoadBalanced
public RestTemplate restTemplate() {
    return new RestTemplate();
}
```

- LoadBalancerClient

```java
@AutoWired
private LoadBalancerClient loadBalancer;

ServiceInstance instance = loadBalancer.choose("service-id");
```

#### feign

https://cloud.spring.io/spring-cloud-openfeign

