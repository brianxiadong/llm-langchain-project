# Weather MCP Server 代码解析

本文档详细解析 `weather.py` 的代码结构、设计模式和实现细节。

## 📁 文件结构分析

```python
weather.py (98行)
├── 导入模块 (1-3行)
├── 服务器初始化 (5-10行)
├── 工具函数 (12-25行)
├── 数据格式化 (27-35行)
├── MCP工具定义 (37-96行)
└── 服务器启动 (97-98行)
```

## 🔍 逐行代码解析

### 1. 模块导入部分 (1-3行)

```python
from typing import Any, Dict, Optional, Union
import httpx
from fastmcp import FastMCP
```

**分析**：
- `typing`：提供类型注解支持，增强代码可读性和IDE支持
- `httpx`：现代异步HTTP客户端，比requests更适合异步编程
- `fastmcp`：MCP服务器框架，简化MCP协议实现

**设计考虑**：
- 使用类型注解提高代码质量
- 选择异步HTTP库支持高并发
- 采用高级MCP框架减少样板代码

### 2. 服务器初始化 (5-10行)

```python
# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
```

**分析**：
- **服务器实例**：创建名为"weather"的MCP服务器
- **常量定义**：将API基础URL和User-Agent提取为常量
- **配置集中化**：便于维护和修改

**设计模式**：
- **单例模式**：全局唯一的MCP服务器实例
- **常量模式**：避免硬编码，提高可维护性

### 3. HTTP请求工具函数 (12-25行)

```python
async def make_nws_request(url: str) -> Optional[Dict[str, Any]]:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
```

**代码分析**：

#### 函数签名
- **异步函数**：`async def` 支持非阻塞操作
- **类型注解**：`Optional[Dict[str, Any]]` 明确返回类型
- **参数类型**：`url: str` 确保输入类型正确

#### 请求头设置
```python
headers = {
    "User-Agent": USER_AGENT,        # 标识客户端
    "Accept": "application/geo+json"  # 指定响应格式
}
```

#### 异步上下文管理
```python
async with httpx.AsyncClient() as client:
```
- **资源管理**：自动处理连接的创建和关闭
- **异步支持**：支持并发请求处理

#### 错误处理策略
```python
try:
    response = await client.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()  # 检查HTTP状态码
    return response.json()
except Exception:
    return None  # 统一错误处理，返回None
```

**设计优点**：
- **防御性编程**：捕获所有异常，避免服务器崩溃
- **超时控制**：30秒超时防止请求挂起
- **状态码检查**：确保HTTP请求成功

### 4. 数据格式化函数 (27-35行)

```python
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""
```

**代码分析**：

#### 数据提取
```python
props = feature["properties"]
```
- **数据结构理解**：NWS API返回GeoJSON格式，警报信息在properties字段

#### 安全访问模式
```python
props.get('event', 'Unknown')
```
- **防御性编程**：使用`.get()`方法避免KeyError
- **默认值策略**：提供有意义的默认值

#### 字符串格式化
- **f-string模板**：使用三引号多行字符串
- **结构化输出**：固定格式便于解析和显示

**设计模式**：
- **数据转换器模式**：将原始API数据转换为用户友好格式
- **模板方法模式**：固定的格式化模板

### 5. MCP工具定义

#### 5.1 天气警报工具 (37-55行)

```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)
```

**代码分析**：

#### 装饰器模式
```python
@mcp.tool()
```
- **声明式编程**：通过装饰器将函数注册为MCP工具
- **框架集成**：FastMCP自动处理工具注册和调用

#### URL构建
```python
url = f"{NWS_API_BASE}/alerts/active/area/{state}"
```
- **字符串插值**：动态构建API端点
- **RESTful设计**：遵循REST API约定

#### 数据验证
```python
if not data or "features" not in data:
    return "Unable to fetch alerts or no alerts found."

if not data["features"]:
    return "No active alerts for this state."
```
- **多层验证**：检查数据存在性和结构完整性
- **用户友好错误**：返回可理解的错误信息

#### 数据处理
```python
alerts = [format_alert(feature) for feature in data["features"]]
return "\n---\n".join(alerts)
```
- **列表推导式**：简洁的数据转换
- **分隔符连接**：使用`---`分隔多个警报

#### 5.2 天气预报工具 (57-96行)

```python
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)
```

**代码分析**：

#### 两阶段API调用
```python
# 第一阶段：获取预报网格信息
points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
points_data = await make_nws_request(points_url)

# 第二阶段：获取实际预报数据
forecast_url = points_data["properties"]["forecast"]
forecast_data = await make_nws_request(forecast_url)
```

**设计分析**：
- **API设计理解**：NWS API采用HATEOAS设计，需要两步获取数据
- **异步链式调用**：两个异步请求的顺序执行
- **错误传播**：每个阶段都有独立的错误处理

#### 数据切片和格式化
```python
for period in periods[:5]:  # Only show next 5 periods
```
- **数据限制**：只显示前5个时段，避免信息过载
- **性能考虑**：减少数据处理量

#### 结构化输出
```python
forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
```
- **模板化输出**：固定格式便于解析
- **多字段组合**：整合温度、风力、详细预报

### 6. 服务器启动 (97-98行)

```python
if __name__ == "__main__":
    import asyncio
    # Initialize and run the server
    mcp.run()
```

**分析**：
- **模块保护**：只在直接运行时启动服务器
- **异步导入**：按需导入asyncio模块
- **框架启动**：调用FastMCP的run方法

## 🏗️ 架构设计模式

### 1. 分层架构
```
表示层：MCP工具接口 (@mcp.tool())
业务层：数据处理和格式化 (format_alert, 数据验证)
数据层：HTTP请求处理 (make_nws_request)
```

### 2. 异步编程模式
- **协程函数**：所有IO操作使用async/await
- **并发支持**：支持多个客户端同时请求
- **资源管理**：使用异步上下文管理器

### 3. 错误处理策略
- **防御性编程**：所有外部调用都有错误处理
- **优雅降级**：错误时返回友好信息而非崩溃
- **统一错误格式**：一致的错误返回格式

### 4. 数据转换模式
- **适配器模式**：将NWS API数据适配为用户友好格式
- **管道模式**：数据获取 → 验证 → 格式化 → 返回

## 🔧 代码质量特点

### 优点
1. **类型安全**：完整的类型注解
2. **异步支持**：高并发处理能力
3. **错误处理**：完善的异常处理机制
4. **代码复用**：公共函数提取
5. **文档完整**：详细的docstring

### 可改进点
1. **配置管理**：可以使用配置文件管理常量
2. **日志记录**：添加结构化日志
3. **缓存机制**：添加数据缓存减少API调用
4. **测试覆盖**：添加单元测试和集成测试
5. **错误细分**：更详细的错误类型和处理

## 📊 性能分析

### 时间复杂度
- `get_alerts`: O(n) - n为警报数量
- `get_forecast`: O(1) - 固定5个时段

### 空间复杂度
- 内存使用主要取决于API响应大小
- 无持久化存储，内存占用较小

### 并发性能
- 异步设计支持高并发
- 每个请求独立，无共享状态
- 受限于NWS API的速率限制

---

*这个代码实现展示了现代Python异步编程的最佳实践，结合了MCP协议的强大功能。* 