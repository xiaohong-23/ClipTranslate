# ClipTranslate 运行日志功能设计

## 背景

用户希望在软件运行过程中保留一份可溯源的运行日志，当程序出现 bug 时能通过日志查看当时的操作、异常堆栈和线程上下文。

## 目标

- 将现有日志输出增强为“可轮转、带线程名、带异常堆栈”的运行日志。
- 不引入新的第三方依赖。
- 不新增 UI 窗口，日志以文件形式存在，便于手动查看。

## 设计决策

### 方案选择

采用 Python 标准库 `logging.handlers.RotatingFileHandler`，原因：

- 与项目现有 `logging.getLogger(__name__)` 调用完全兼容，改动最小。
- 不需要新增依赖。
- 支持按文件大小自动轮转和备份保留。

### 日志配置

| 配置项 | 值 | 说明 |
| --- | --- | --- |
| 日志文件 | `resource/app.log` | 与现有配置文件、图标资源放同一目录，方便打包后定位 |
| 日志级别 | `DEBUG` | 记录尽量详细的信息，便于排错 |
| 格式 | `%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s` | 包含时间、级别、线程名、模块名 |
| 时间格式 | `%Y-%m-%d %H:%M:%S` | 保留毫秒由 asctime 默认提供 |
| 单文件上限 | 5 MB | 防止单个日志文件过大 |
| 备份数量 | 3 | 最多保留 `app.log.1` ~ `app.log.3` |

### 异常捕获

- 通过 `sys.excepthook` 捕获主线程未处理异常，确保崩溃信息写入日志。
- 在业务代码中，出现 `Exception` 时优先使用 `logger.exception(...)`，自动附带完整 traceback。

### 需要改动的文件

1. `main.py`
   - 将 `FileHandler` 替换为 `RotatingFileHandler`。
   - 调整日志格式，增加 `threadName`。
   - 注册 `sys.excepthook`，记录未处理异常。

2. `translator.py`
   - `TranslationEngine.translate` 中的异常捕获使用 `logger.exception`。
   - `ClipboardTranslator._execute` 中的异常捕获使用 `logger.exception`。
   - 其他异常日志如 `copy` / `paste` 失败同样使用 `logger.exception`。

3. `app_ui.py`
   - 关键操作（启动、退出、托盘图标创建/失败、热键绑定/失败）保持或增强日志。
   - 异常分支使用 `logger.exception`。

4. `config.py` / `notifier.py`
   - 失败分支如有异常对象，改用 `logger.exception`。

## 日志效果示例

```
2026-07-05 14:22:59,123 [INFO] [MainThread] app_ui: Tray icon started
2026-07-05 14:23:01,456 [ERROR] [Dummy-1] translator: Translation workflow error
Traceback (most recent call last):
  File "F:\Desktop\Pyproject\ClipTranslate\translator.py", line 255, in _execute
    result = self._engine.translate(source_text)
  File "F:\Desktop\Pyproject\ClipTranslate\translator.py", line 93, in translate
    response = client.call_json("TextTranslate", json.loads(params))
  ...
TencentCloudSDKException: ...
```

## 非目标

- 不在界面中新增日志查看窗口。
- 不改用 `loguru` 等第三方日志库。
- 不调整日志文件存放位置。
- 不改业务逻辑，仅改进日志记录方式。

## 验证方式

1. 运行 `python ClipTranslate.py` 或 `python main.py`。
2. 检查 `resource/app.log` 是否生成并按格式记录启动日志。
3. 触发一次翻译失败（如断网或错误密钥），检查日志中是否包含 `ERROR` 和完整 traceback。
