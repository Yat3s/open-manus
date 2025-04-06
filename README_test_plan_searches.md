# 测试 DeepResearchManager.\_plan_searches 方法 (真实API版本)

这个测试文件用于对 `DeepResearchManager` 类中的 `_plan_searches` 方法进行真实环境测试，该方法负责生成搜索计划。

## 文件结构

- `src/core/deep_research/tests/test_plan_searches.py`: 测试文件
- `src/core/deep_research/tests/__init__.py`: 测试包初始化文件

## 测试内容

测试文件包含以下真实测试用例：

1. `test_plan_searches_real`: 使用真实API测试搜索计划生成

   - 验证返回的搜索计划结构正确
   - 验证搜索计划包含合理数量的搜索项
   - 验证每个搜索项包含必要的字段

2. `test_plan_searches_different_queries`: 验证不同查询会产生不同的搜索计划
   - 对比两个不同主题的查询结果
   - 分析搜索项的重叠程度

## 运行测试

可以使用以下命令运行测试：

```bash
# 从项目根目录运行
python -m unittest src.core.deep_research.tests.test_plan_searches
```

## 注意事项

1. 这是一个真实环境测试，需要确保所有必要的API密钥和服务都已正确配置
2. 测试会消耗API配额，因为它会实际调用外部AI服务
3. 测试运行可能需要较长时间，因为它涉及多次API调用
4. 测试结果会打印在控制台，包括生成的搜索计划概要

## 环境要求

1. 必须设置正确的环境变量（如API密钥）
2. 必须有网络连接
3. 测试使用了 `asyncio.run()` 来运行异步函数

## 使用到的模拟技术

测试使用了以下模拟技术：

1. `patch`: 用于模拟 `Runner` 类
2. `MagicMock`: 用于模拟返回结果
3. `AsyncMock`: 用于模拟异步函数

## 注意事项

1. 测试依赖于 `unittest` 和 `unittest.mock` 库
2. 测试假设 `Runner.run` 返回的对象有 `final_output_as` 方法
