学习flask
参考：https://tutorial.helloflask.com/


### 测试
```shell
pip install coverage
```

```shell
# 执行测试并检查测试覆盖率
coverage run --source=app test_watchlist.py
# 查看覆盖率报告
coverage report
# 获取详细的HTML格式的覆盖率报告
# 它会在当前目录生成一个htmlcov文件夹，打开其中的index.html即可查看覆盖率报告
# 点击文件名可以看到具体的代码覆盖情况
coverage html
```
