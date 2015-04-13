中间件实验 SOAP 示例代码
=====================

基于 Python Flask 开发的天气预报网站。

## 依赖

* Flask
* suds

## 运行

在项目目录下使用

    python -m SimpleHTTPServer
    
创建一个小型的 HTTP Server，主要是为了 Serve 那两个 xsd 文件。

然后执行

    python WeatherReport.py
    
在浏览器中通过 localhost:5000 访问
