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

### Feign

https://cloud.spring.io/spring-cloud-openfeign/reference/html/

Integrated Ribbon & Hystrix

interface

```xml
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
```

**@EnableFeignClients**

```java
@FeignClient(value = "MICROSERVICECLOUD-DEPT")
public interface DeptClientService {
    
    @RequestMapping(value = "/dept/get/{id}", method = RequestMethod.GET)
    public Dept get(@PathVariable("id") long id);

    @RequestMapping(value = "/dept/list", method = RequestMethod.GET)
    public List<Dept> list();

    @RequestMapping(value = "/dept/add", method = RequestMethod.POST)
    public boolean add(Dept dept);
    
    @GetMapping(path = "/demo")
    String demoEndpoint(@SpringQueryMap Params params);
    
    @GetMapping("/objects/links/{matrixVars}")
    Map<String, List<String>> getObjects(@MatrixVariable Map<String, List<String>> matrixVars);
}

// Params.java
public class Params {
    private String param1;
    private String param2;

    // [Getters and setters omitted for brevity]
}
```



```java
@RestController
public class DeptController_Consumer {

    @Autowired
    private DeptClientService service = null;

    @RequestMapping(value = "/consumer/dept/get/{id}")
    public Dept get(@PathVariable("id") Long id) {
        return this.service.get(id);
    }

    @RequestMapping(value = "/consumer/dept/list")
    public List<Dept> list() {
        return this.service.list();
    }

    @RequestMapping(value = "/consumer/dept/add")
    public Object add(Dept dept) {
        return this.service.add(dept);
    }
}
```



