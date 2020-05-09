### Terms

https://docs.amazonaws.cn/index.html

- EC2 - Elastic Compute Cloud

  https://docs.amazonaws.cn/ec2/?id=docs_gateway

  Amazon Elastic Compute Cloud (Amazon EC2) 是一种提供可调节计算容量的 Web 服务 – 简单来说，就是 Amazon 数据中心里的服务器 – 您可以使用它来构建和托管您的软件系统。

- S3 - Simple Storage Service

  https://docs.amazonaws.cn/s3/?id=docs_gateway

  Amazon Simple Storage Service (Amazon S3) 是一种面向 **Internet** 的存储服务。您可以通过 Amazon S3 随时在 Web 上的任何位置存储和检索的**任意大小**的数据。您可以使用 AWS 管理控制台简单而直观的 web 界面来完成这些任务

  - multiple copies

- S3 Glacier

  https://docs.amazonaws.cn/glacier/?id=docs_gateway

  Amazon Glacier 是一种针对不常用的数据（“**冷数据**”）而经过了优化的存储服务。 这项服务为数据存档和备份提供了**持久且成本极低**的存储解决方案及安全功能。使用 Amazon Glacier，您可以将数据经济高效地存储数月、数年，甚至数十年。Amazon Glacier 可让您将存储扩展到 AWS 并卸下操作以及管理负担，这样，您就不必担心容量规划、硬件配置、数据复制、硬件故障检测和恢复，或者耗时的硬件迁移等问题。

  - long period, retain long audit log

- ELB - Elastic Load Balancing

  https://docs.amazonaws.cn/elasticloadbalancing/?id=docs_gateway

  Elastic Load Balancing 自动分配间应用程序的传入流量在多个目标， 如Amazon EC2 实例。它监控健康目标上的已注册目标和流量路的健康状况。Elastic Load Balancing 支持三种负载均衡器：

  - 应用程序负载均衡器
    - WebSockets
    - Steaming
    - Real-time
  - 网络负载均衡器
  - Classic 负载均衡器。

- EBS - Elastic Block Store

  https://docs.amazonaws.cn/ebs/?id=docs_gateway

  Amazon Elastic Block Store (Amazon EBS) 是一种 Web 服务，可提供数据块级存储卷以用于 EC2 实例。EBS 卷是高度可用的**可靠**存储卷，可以挂载到任何正在运行的实例，并可像硬盘驱动器一样使用。

- IAM - Identity and Access Management

  https://docs.amazonaws.cn/iam/?id=docs_gateway

  AWS Identity and Access Management (IAM) 是一项用于安全地控制 AWS 服务访问的 Web 服务。借助 IAM，您可以集中管理用户、访问密钥等安全凭证，以及控制用户和应用程序可以访问哪些 AWS 资源的权限。

- DynamoDB

  https://docs.amazonaws.cn/dynamodb/?id=docs_gateway

  Amazon DynamoDB 是一种完全托管的 **NoSQL** 数据库服务，提供快速而可预测的性能，能够实现**无缝扩展**。您可以使用 Amazon DynamoDB 创建一个数据库表来存储和检索任何大小的数据，并处理任何级别的请求流量。Amazon DynamoDB 可自动将表的数据和流量分布到足够多的服务器中，以处理客户指定的请求容量和数据存储量，同时保持**一致**的性能和**高效**的访问。

  - User session
  - key-value
  - structured
  - low latency

- SQS - Simple Queue Service

  https://docs.amazonaws.cn/sqs/?id=docs_gateway

  Amazon Simple Queue Service (Amazon SQS) 是一种完全托管的消息队列服务，可轻松分离和扩展微服务、分布式系统及无服务器应用程序。Amazon SQS 用于在分布式应用程序组件之间传送数据，可帮助您**分离**这些组件。

  - Separate
  - large request in queue
  - RESTful call

- VPC - Virtual Private Cloud

  https://docs.amazonaws.cn/vpc/?id=docs_gateway

  Amazon Virtual Private Cloud (Amazon VPC) 允许您在已经定义的虚拟网络内启动 Amazon Web Services (AWS) 资源。这个虚拟网络与您在数据中心中运行的传统网络极其相似，并会为您提供使用 AWS 的可扩展基础设施的优势。
  - NAT - Network Address Translation
  - Need public IP address inside a subnet in order to access Internet Gateway

- Redshift

  https://docs.amazonaws.cn/redshift/?id=docs_gateway

  Amazon Redshift 是一种快速、完全托管的 PB 级数据仓库服务，它使得用现有商业智能工具对您的所有数据进行高效分析变得简单而实惠。它为从几百 GB 到 1PB 或更大的数据集而优化，且每年每 TB 花费不到 1 000 USD，为最传统数据仓库存储解决方案成本的十分之一。

- RDS - Rational Database Service

  https://docs.amazonaws.cn/rds/?id=docs_gateway

  Amazon Relational Database Service (Amazon RDS) 是一种 Web 服务，可让用户更轻松地在云中设置、操作和扩展关系数据库。它可以经济有效的为用户提供一个容量可调的行业标准的关系数据库，并承担常见的数据库管理任务。

  - MariaDB
  - MS SQL server
  - MySQL
  - Postgres
  - Oracle

- CloudWatch

  https://docs.amazonaws.cn/cloudwatch/?id=docs_gateway

  Amazon CloudWatch 提供可靠、可调整且灵活的监测解决方案，让您可在短短几分钟内开始使用。您不再需要设置、管理和扩展**监控系统和基础设施**了。

- CloudTrail

  https://docs.amazonaws.cn/cloudtrail/?id=docs_gateway

  利用 AWS CloudTrail，可获取您账户的 **API 调用**历史记录，包括通过 AWS 管理控制台、AWS 软件开发工具包、命令行工具、较高级 AWS 服务进行的 API 调用，进而监控您在云上的 AWS 部署。您还可以**确定哪些用户和账户**为支持 CloudTrail 的服务调用了 AWS API、发出调用的源 IP 地址以及调用发生的时间。您可将 CloudTrail 集成到使用 API 的应用程序、为您的组织自动创建跟踪、检查跟踪的状态和控制管理员启用和关闭 CloudTrail 日志记录的方式。

  - identify account owner
  - log AWS KMS
  - audit log of accounts

- ElastiCache

  https://docs.amazonaws.cn/elasticache/?id=docs_gateway

  Amazon ElastiCache 可让用户在 AWS 云中轻松设置、管理和扩展分布式内存中的缓存环境。它可以提供高性能、可调整大小且符合成本效益的内存缓存，同时消除部署和管理分布式缓存环境产生的相关复杂性。ElastiCache 与 Redis 和 Memcached 引擎一起工作；要查看哪个最适合您，请参见任一用户指南中的“比较 Memcached 和 Redis”主题。

  - store session

- CloudFront

  https://docs.amazonaws.cn/cloudfront/?id=docs_gateway

  Amazon CloudFront 可加快**分发**静态和动态 Web 内容（例如，.html、.css、.php、图像和媒体文件）的过程。当用户请求内容时，CloudFront 通过可提供低延迟和高性能的全球边缘站点网络交付相应内容。

  - Use Edge (data center)

- Elastic Beanstalk

  https://docs.amazonaws.cn/elastic-beanstalk/?id=docs_gateway

  AWS Elastic Beanstalk 可让您迅速地在 AWS 云中**部署和管理应用程序**，而无需为运行这些应用程序的基础设施操心。AWS Elastic Beanstalk 可降低管理的复杂性，但不会影响选择或控制。您只需上传应用程序，AWS Elastic Beanstalk 将自动处理有关容量预配置、负载均衡、扩展和应用程序运行状况监控的部署细节。

- CloudFormation

  https://docs.amazonaws.cn/cloudformation/?id=docs_gateway

  借助 AWS CloudFormation，您可以有预见性地、重复地创建和预置 AWS **基础设施部署**。它可以帮助您利用 AWS 产品 (如 Amazon EC2、Amazon Elastic Block Store、Amazon SNS、Elastic Load Balancing 和 Auto Scaling) 在云中构建高度可靠、高度可扩展且经济高效的应用程序，为您免除创建和配置底层 AWS 基础设施之忧。借助 AWS CloudFormation，您可以使用模板文件，将资源集作为一个单元 (堆栈) 进行创建和删除。

- CodeDeploy

  https://docs.amazonaws.cn/codedeploy/?id=docs_gateway

  AWS CodeDeploy 是一种**部署服务**，让开发人员能够实现将应用程序部署到实例的自动化，并根据需要**更新应用程序**。

- Cognito
  https://docs.amazonaws.cn/cognito/?id=docs_gateway
  Amazon Cognito 为您的 Web 和移动应用程序提供身份验证、授权和用户管理。您的用户可使用用户名和密码直接登录，也可以通过第三方（例如 Facebook、Amazon、Google 或 Apple）登录。

- EFS - Elastic File System

  https://aws.amazon.com/cn/efs/

  Amazon Elastic File System (Amazon EFS) 可提供简单、可扩展、完全托管的弹性 **NFS** 文件系统，以与 AWS 云服务和本地资源配合使用。它可在不中断应用程序的情况下按需扩展到 PB 级，随着添加或删除文件自动扩展或缩减，无需预置和管理容量，可自适应增长。

  - Similar size folder
  - Network File System
  - Critical and access frequently
  -  maximize availability and durability

- Lambda

  https://docs.amazonaws.cn/lambda/?id=docs_gateway

  利用 AWS Lambda，您无需预置或管理服务器即可运行代码。您只需为使用的计算时间付费，在代码未运行期间不产生任何费用。您可以为几乎任何类型的应用程序或后端服务运行代码，而无需任何管理。只需上传您的代码，Lambda 会处理运行和扩展高可用性代码所需的一切工作。您可以将您的代码设置为自动从其他 AWS 服务触发，或者直接从任何 Web 或移动应用程序调用。

  - Node.js
  - Python
  - Ruby
  - Java
  - Go
  - C#
  - Powershell

- Amazon Athena

  https://aws.amazon.com/athena/

  Amazon Athena is an interactive **query service** that makes it easy to analyze data in Amazon S3 using standard SQL. Athena is serverless, so there is **no infrastructure** to manage, and you pay only for the queries that you run.

  Athena -> S3

- Amazon Kinesis

  https://docs.amazonaws.cn/kinesis/?id=docs_gateway

  Amazon Kinesis 可以轻松地实时**收集**、处理和分析视频和数据流。

  - collect page click for website

- AWS STS - Security Token Service

  https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_credentials_temp.html

  可以使用 AWS Security Token Service (AWS STS) 创建可控制对您的 AWS 资源的访问的临时安全凭证，并将这些凭证提供给受信任用户。临时安全凭证的工作方式与您的 IAM 用户可使用的长期访问密钥凭证的工作方式几乎相同

  - IAM roles with amazon ECS instances
  - Web federated identity

- SES - Simple Email Service



- Amazon Aurora

  Transactional Database

  Exponential grow

  TB level


