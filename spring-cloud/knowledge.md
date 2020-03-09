### Eureka

- [ ] Consistency（一致性）

- [x] Availability（可用性）
- [x] Partition tolerance（分区容错性）

#### Server

- self preservation mode, default enabled, not recommend to turn off
- when enable, do not remove an service when it failed to register due to some issues like network broken.
- turn off self preservation:

```yaml
server:
  enable-self-preservation: false
```





#### Client

- no need @EnableEurekaClient if have **spring-cloud-starter-netflix-eureka-client** on classpath

```yaml
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
```

- 