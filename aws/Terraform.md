Terraform是HashiCorp公司旗下的Provision Infrastructure产品, 是AWS APN Technology Partner与AWS DevOps Competency Partner。Terraform是一个IT基础架构自动化编排工具，它的口号是“Write, Plan, and Create Infrastructure as Code”, 是一个“基础设施即代码”工具，类似于[AWS CloudFormation](https://aws.amazon.com/cloudformation/)，允许您创建、更新和版本控制的AWS基础设施。

Terraform 几乎可以支持所有市面上能见到的云服务。



使用 terraform 比 ansible 好在哪里？

- 并发创建，速度快
- 扩容/缩容 很方便，改一个数字就行
- state 文件记录资源状态



### 配置

Terraform配置的语法称为HashiCorp配置语言（HCL）。

Terraform使用文本文件来描述基础设施和设置变量。这些文件称为Terraform 配置，并以 .tf结尾。本节介绍这些文件的格式以及它们的加载方式。

配置文件的格式可以有两种格式：Terraform格式和JSON。Terraform格式更加人性化，支持注释，并且是大多数Terraform文件通常推荐的格式。JSON格式适用于机器创建，修改和更新，也可以由Terraform操作员完成。Terraform格式后缀名以.tf结尾，JSON格式后缀名以.tf.json结尾。

https://www.terraform.io/docs/configuration/index.html

https://www.terraform.io/docs/configuration/syntax.html

编辑器插件：http://hashivim.github.io/vim-terraform/

### Provider 配置

https://www.terraform.io/docs/providers/aws/index.html



### 命令

```
./terraform init
./terraform plan
./terraform apply
./terraform destroy
./terraform fmt xxx.tf
```

在执行像 terraform plan或 terraform apply等命令的时候，可以按下 ctrl + c让控制台输出详细的日志信息。





### 参考

https://aws.amazon.com/cn/blogs/china/aws-china-region-guide-series-terraform1/