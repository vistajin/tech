* k8s资源打包工具
* * chart: 包含创建k8s一个应用实例的必要资源
* * tiller: 应用发布的必要配置信息
* * release: 一个chart的运行实例
* * repo: 存放chart
* * helm: 通过gRPC协议与tiller交互，提供增删查改chart，release，repo的功能
