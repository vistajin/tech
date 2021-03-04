# day1-20210304

## WebMvcConfigurer

### addInterceptors method

```java
// addInterceptor方法是注册一个生命周期拦截器
// addPathPatterns方法是拦截的url地址
// excludePathPatterns是排除那些地址不拦截
// order方法是拦截顺序，就是拦截器执行链的执行顺序，值越大，拦截就越靠后,这里注册两个是为了验证顺序的
registry.addInterceptor(new ZyInterceptor()).addPathPatterns("/**").excludePathPatterns("/test").order(1);
registry.addInterceptor(new OtherInterceptor()).addPathPatterns("/**").excludePathPatterns("/test").order(2);
```

拦截器定义：

```java
public class ZyInterceptor implements HandlerInterceptor {

    /**
     * 在Controller请求执行之前，
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        System.out.println("zy");
        // 返回值表示是否向下执行，如果返回false，那么中止执行链。通常发送HTTP错误或编写自定义响应给请求端
        return true;
    }

    /**
     * Controller处理之后，渲染完成之前
     */
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    /**
     * 整个请求完成执行完之后
     */
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
```

