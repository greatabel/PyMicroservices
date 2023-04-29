Amazon CloudFront 是一个内容分发网络 (CDN)，可以安全地向全球客户分发数据、视频、应用程序和 API。 它与其他 Amazon Web Services 产品集成，为开发人员和企业提供了一种以低延迟、高传输速度和最低成本向最终用户分发内容的简便方法。

API Gateway 是一项完全托管的服务，可让开发人员轻松创建、发布、维护、监控和保护任何规模的 API。 API 网关处理与接受和处理多达数十万个并发 API 调用相关的所有任务，包括流量管理、授权和访问控制、监控和 API 版本管理。

CloudFront 和 API Gateway 之间的主要区别在于，CloudFront 是一种 CDN 服务，可以根据用户的地理位置向用户提供 HTML、图像、视频等内容，而 API Gateway 是一种使开发人员能够创建、发布、 和管理 API。 CloudFront 通常用于分发静态内容，而 API 网关用于构建和管理 API。


Amazon CloudFront is a content delivery network (CDN) that securely delivers data, videos, applications, and APIs to customers globally. It integrates with other Amazon Web Services products to give developers and businesses an easy way to distribute content to end users with low latency, high transfer speeds, and minimal costs.

API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. API Gateway handles all of the tasks associated with accepting and processing up to hundreds of thousands of concurrent API calls, including traffic management, authorization and access control, monitoring, and API version management.

The main difference between CloudFront and API Gateway is that CloudFront is a CDN service that delivers content such as HTML, images, videos, etc. to users based on their geographic location, while API Gateway is a service that enables developers to create, publish, and manage APIs. CloudFront is typically used to distribute static content, while API Gateway is used for building and managing API's.

2.

根据您当前正在开发的应用程序架构，您是在实施 AWS Cloud Front 还是 API Gateway？
如果是，请描述您如何使用它/它们。 你为什么选择它？
否则（如果不使用其中任何一个），请指出您将选择哪一个用于您的体系结构中的未来实现？ 你为什么选择它？

如果您的应用程序需要以低延迟和高传输速度向全球用户分发图像、视频和其他静态文件等内容，那么您应该考虑使用 CloudFront。 CloudFront 可以将这些文件缓存在世界各地的边缘位置，以便当用户请求它们时，它们会从最近的边缘位置交付。 这可以大大提高应用程序的性能。

另一方面，如果您的应用程序需要公开一组 API 以供其他系统使用，那么您应该考虑使用 API 网关。 API Gateway 允许您以安全且可扩展的方式创建、发布和管理 API。 它还提供身份验证、访问控制、监控和版本管理等功能。

在未来的实施中，两者之间的选择将取决于应用程序的具体用例和要求。 当应用程序需要以低延迟和高传输速度分发内容时，应使用 CloudFront。 当应用程序需要创建、发布和管理 API 时，应使用 API 网关。 这两种服务可以集成在一起。

if your application needs to distribute content such as images, videos, and other static files to users globally with low latency and high transfer speeds, then you should consider using CloudFront. CloudFront can cache these files at edge locations around the world, so that when users request them, they are delivered from the nearest edge location. This can greatly improve the performance of your application.

On the other hand, if your application needs to expose a set of APIs to be consumed by other systems, then you should consider using API Gateway. API Gateway allows you to create, publish, and manage APIs in a secure and scalable manner. It also provides features such as authentication, access control, monitoring, and version management.

In future implementations, the choice between the two will depend on the specific use case and requirements of the application. CloudFront should be used when the application needs to distribute content with low latency and high transfer speeds. API Gateway should be used when the application needs to create, publish, and manage APIs. Both services can be integrated together.


3.

演讲：
Title: Leveraging AWS Services for a Malaysia Automotive Industry Blog Platform

Introduction:
Ladies and gentlemen, today I am excited to present to you how we have utilized Amazon Web Services (AWS) to enhance our blog platform, which primarily focuses on the automotive industry in Malaysia. Our platform serves as a vertical information hub to provide insights, news, and analysis related to the Malaysian automotive sector.

Slide 1: AWS Services Overview
In our journey to improve our platform's performance and reliability, we have integrated several AWS services, with a primary focus on Amazon S3 and DynamoDB. We have also made use of AWS CloudWatch and X-Ray for monitoring and analyzing our application's performance.

Slide 2: Amazon S3 Integration
Amazon Simple Storage Service (S3) is an object storage service that offers industry-leading scalability, data availability, security, and performance. We use S3 to store and manage all the images associated with our blog posts. By hosting our images on S3, we can ensure high availability, redundancy, and fast content delivery, resulting in an enhanced user experience on our platform.

Slide 3: Amazon DynamoDB Integration
Amazon DynamoDB is a managed NoSQL database service that provides fast and predictable performance with seamless scalability. We have replaced our previous database solution with DynamoDB to store all our blog data, including titles, text, and associated metadata. With DynamoDB's low-latency, auto-scaling capabilities, and high availability, we can serve our growing audience efficiently, regardless of the volume of requests or data.

Slide 4: AWS CloudWatch and X-Ray for Monitoring and Analysis
As our platform continues to grow, it becomes essential to monitor and analyze its performance. AWS CloudWatch and X-Ray services allow us to do just that. CloudWatch helps us collect metrics, logs, and alarms for our AWS resources, while X-Ray provides insights into the request tracing of our distributed application.

Slide 5: Latency Testing and Performance Analysis
With the help of CloudWatch and X-Ray, we continuously monitor the latency of our /home route and analyze its performance. By identifying bottlenecks and implementing optimization strategies like caching, pagination, and database indexing, we can ensure that our platform remains fast and responsive, providing a seamless browsing experience for our users.

Conclusion:
In conclusion, by integrating Amazon S3, DynamoDB, CloudWatch, and X-Ray into our blog platform, we have successfully created a more robust, efficient, and scalable information hub for the Malaysian automotive industry. These AWS services have allowed us to enhance our user experience, improve performance, and ensure that our platform can adapt and grow with the ever-changing automotive landscape in Malaysia. Thank you for your attention.




