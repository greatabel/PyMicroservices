@“Write a paper promising salvation, make it a structured something or a virtual something, or abstract, distributed or higher-order or applicative and you can almost be certain of having started a new cult.
- Edsger W. Dijkstra
”

@The following points summarize the pros and cons of the monolithic approach:
Starting a project as a monolith is easy, and probably the best approach.
单体应用开始一个工程更容易，很可能是最好的方式

A centralized database simplifies the design and organization of the data.
中心化的数据库可以简化数据的组织和设计

Deploying one application is simple.
部署一个应用更简单

Any change in the code can impact unrelated features. When something breaks, the whole application may break.
修改可能影响所有特性，整个应用可能挂掉

Solutions to scale your application are limited: you can deploy several instances, 
but if one particular feature inside the app takes all the resources, it impacts everything.
应用的可扩展平衡是有限的。如果一个特性需要所有的资源，它就影响每件事

As the code base grows, it's hard to keep it clean and under control.
代码库增长，特别难以保持干净和可控

@@@@微服务益处：
Separation of concerns
关注点的分离：每一个微服务都可以独立出来，变成一个团队维护开发。它们自己的编程语言和数据库，只要他们有文档化的API。
    如果“支付系统”改变了于银行互动方式，只影响服务内部，应用其他部分都不受影响。松耦合的哲学类似：单职责原则。


Smaller projects to deal with
更小的工程：你可以重构更频繁，更短的发布，保持领先。更小的工程也减少了改进应用的风险：如果想试试新的编程语言和框架，
他们可以快速微服务api的实现原型，实验，比较，是否进一步。

More scaling and deployment options
更多的收缩和部署选择。比如可以把PDF生成功能部署到更强大的CPU服务器群上。

@@@@    微服务痛点
Illogical splitting
    有些需要拆分成微服务的用例很明显，但有些有来来回回修改。让微服务的设计成熟，你需要经历“尝试-失败-再尝试”的迭代。你可能通过不明显的暂不拆分来缓解这个问题。“过早拆分是万恶之源”

More network interactions
    单体应用因为在一个进程，就算代码很乱，你不需要调用特别多后台服务。
    每个后台服务怎么被调用，会有很多需要考虑的地方。
Data storing and sharing
    一个有效的微服务需要各个微服务的数据库之间是独立的，理想状态下不应该共享数据库。微服务怎么尽可能的避免数据重复是个挑战

Compatibility issues
    当一个feature修改影响多个微服务时候。如果修改影响了数据在微服务之间传递的向后兼容性
Testing
    现在你想要做端对端的测试、部署整个应用，你要面对很多的砖块。你需要一个健壮、敏捷的环境流程。
    你需要和整个应用打交道当你开发时候。你不能完整的测试一小块的东西了。

@WSGI（ Web Server Gateway Interface）允许你用线程池同时服务多个请求。但是你不能同时运行几千个，你的线程池会耗尽。
    这就是为什么non-WSGI的框架Twisted and Tornado，或者js领域的node.js变得流行，他们是完全异步
    但是（同步）synchronous框架也可以构建微服务，如果你的部署考虑了 one request == one thread 的WSGI限制。

@“The way the Python core developers coded asyncio, and how they elegantly extended 
the language with the async and await keywords to implement coroutines, 
made asynchronous applications built with vanilla Python 3.5+ code look very elegant 
and close to synchronous programming.
Coroutines are functions that can suspend and resume their execution.”
python的核心开发者开发了asyncio，可以通过async await关键字实现协程。

@in any case, no matter how much energy you spend on tests and documentation, 
there's one golden rule: testing, documenting, and coding your projects should be done continuously . 
In other words, changes in the code should ideally be reflected in the tests and documentation as they happen.
不管你花了多少精力到测试和文档，金科玉律：测试、文档化、代码应该被持续的完成。
你代码的改变应该被反应到测试和文档中

@
在flask层面，你可以使用flask-profiler,收集每个request多久，提供dashboard让你看各自的时间
你也可以把细节通过StatsD度量，和用一个更精细的图标Graphite

@
brew install rabbitmq
brew services start rabbitmq
brew services stop  rabbitmq
brew services restart rabbitmq

































