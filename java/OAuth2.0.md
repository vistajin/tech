

http://www.ruanyifeng.com/blog/2019/04/oauth_design.html

OAuth 就是一种授权机制。数据的所有者告诉系统，同意授权第三方应用进入系统，获取这些数据。系统从而产生一个短期的进入令牌（token），用来代替密码，供第三方应用使用。





Spring Cloud Security (http://cloud.spring.io/spring-cloud-security/1.2.x/single/spring-cloud-security.html)

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-oauth2</artifactId>
</dependency>
```

```java
@EnableResourceServer // 启用资源服务器
public class AuthorizationServerApplication {
    // ...
}
```

https://blog.csdn.net/kefengwang/article/details/81213025