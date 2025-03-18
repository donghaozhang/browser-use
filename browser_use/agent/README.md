# Browser-Use Agent Module

## Overview

The `agent` module represents the cognitive core of the Browser-Use framework, implementing a sophisticated orchestration layer between Large Language Models (LLMs) and web browsers. This advanced subsystem enables AI agents to perceive, reason about, and interact with web interfaces through a multi-stage pipeline architecture. At its foundation, the module transforms raw DOM structures and visual elements into semantic representations optimized for LLM comprehension, then interprets the model's reasoning into precise browser automation commands.

The system incorporates several key innovations: (1) a bidirectional state translation mechanism that maps between browser DOM states and LLM-interpretable formats; (2) a context-aware memory system that maintains coherent task execution despite the limited context windows of LLMs; (3) a flexible action execution framework supporting both high-level semantic operations and low-level DOM manipulations; and (4) robust error recovery strategies that allow agents to reason about and recover from unexpected states. This architecture enables unprecedented capabilities in web automation, allowing AI systems to perform complex multi-step tasks involving dynamic content, form interactions, and decision-making based on page content—all while maintaining a stateful understanding of the ongoing task that persists across multiple page transitions and application states.

## Architecture

The agent module follows a modular design that separates concerns between:
- AI model communication
- Browser state representation
- Action execution
- Memory and state management

### Core Components

```
browser_use/agent/
├── service.py        # Main Agent implementation
├── views.py          # Data models and structures
├── prompts.py        # LLM prompt templates
├── system_prompt.md  # Core system instructions for the LLM
├── gif.py            # GIF recording functionality
├── tests.py          # Unit tests
└── message_manager/  # Message handling components
    └── service.py    # Message management implementation
```

## Key Files

### service.py

The central implementation file containing the `Agent` class. This orchestrates:
- Communication with the LLM
- Browser state processing
- Action execution
- History and memory management

### views.py

Defines data models used throughout the agent system:
- `AgentOutput`: Structured output from the LLM
- `AgentBrain`: Internal state representation
- `ActionResult`: Results of browser actions
- Other supporting data structures

### prompts.py

Contains prompt templates used to communicate with the LLM:
- System prompts
- Reflection prompts
- Planning prompts
- Action generation prompts

### system_prompt.md

The primary system prompt that guides the LLM on how to:
- Interpret web page content
- Generate valid actions
- Reason about task progress
- Handle error cases

### gif.py

Provides functionality to record browser interactions as GIF animations for:
- Visualization
- Debugging
- Demonstrations

### message_manager/service.py

Handles all message-related operations between the agent and LLM:
- **Token Management**: Tracks and controls token usage to stay within LLM context limits
- **Message History**: Maintains the conversation history with proper formatting
- **Message Transformation**: 
  - Converts browser states to LLM-friendly formats
  - Processes action results into messages
  - Handles images and text content
- **Memory Optimization**:
  - Implements token cutting strategies when approaching limits
  - Prioritizes important content when trimming is needed
- **Security Features**:
  - Filters sensitive data from messages
  - Supports placeholder substitution for secrets

The `MessageManager` class handles the lifecycle of all messages:
1. Initializes with system prompts and task instructions
2. Adds browser state updates as human messages
3. Records LLM outputs as AI messages
4. Manages tool messages for action results
5. Implements intelligent trimming to stay within token limits

## Working Principle

1. **Initialization**:
   - Agent configured with an LLM model and browser instance
   - System prompts loaded to guide LLM behavior

2. **Execution Loop**:
   - Capture current browser state (DOM, screenshot, URL)
   - Format state into LLM-understandable messages
   - LLM analyzes page content and decides next action
   - Agent interprets LLM response and executes browser actions
   - Results are captured and fed back to the LLM

3. **Memory Management**:
   - Maintains history of actions and results
   - Provides context for future decisions
   - Implements summarization for efficiency

4. **Action Execution**:
   - Supports navigation, clicking, typing, and other browser operations
   - Handles errors and retries when needed
   - Validates actions for safety and feasibility

## Usage

The Agent module is typically used as follows:

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="Search for information about AI and summarize the results",
    llm=ChatOpenAI(model="gpt-4o"),
)

result = await agent.run()
print(result)
```

## Extension Points

The agent module is designed for extensibility:
- Custom actions can be added through the controller registry
- Alternative LLM providers can be integrated
- Message handling can be customized for different use cases
- Prompt engineering can be refined for specific domains 

---

# Browser-Use Agent 模块

## 概述

`agent` 模块是 Browser-Use 框架的认知核心，实现了大型语言模型（LLM）与网页浏览器之间的高级协调层。这个先进的子系统通过多阶段流水线架构，使 AI 代理能够感知、推理并与网页界面交互。在其基础上，该模块将原始 DOM 结构和视觉元素转换为针对 LLM 理解而优化的语义表示，然后将模型的推理解释为精确的浏览器自动化命令。

该系统包含几项关键创新：(1) 双向状态转换机制，在浏览器 DOM 状态和 LLM 可解释格式之间建立映射；(2) 上下文感知的记忆系统，尽管 LLM 的上下文窗口有限，但仍能保持连贯的任务执行；(3) 灵活的动作执行框架，支持高级语义操作和低级 DOM 操作；(4) 强大的错误恢复策略，允许代理对意外状态进行推理和恢复。这种架构实现了网页自动化的前所未有的能力，使 AI 系统能够执行涉及动态内容、表单交互和基于页面内容决策的复杂多步骤任务——同时在多个页面转换和应用程序状态之间维持任务的持续理解。

## 架构

agent 模块采用模块化设计，将以下关注点分离：
- AI 模型通信
- 浏览器状态表示
- 动作执行
- 内存和状态管理

### 核心组件

```
browser_use/agent/
├── service.py        # Agent 主要实现
├── views.py          # 数据模型和结构
├── prompts.py        # LLM 提示模板
├── system_prompt.md  # LLM 的核心系统指令
├── gif.py            # GIF 录制功能
├── tests.py          # 单元测试
└── message_manager/  # 消息处理组件
    └── service.py    # 消息管理实现
```

## 关键文件

### service.py

包含 `Agent` 类的核心实现文件。它协调：
- 与 LLM 的通信
- 浏览器状态处理
- 动作执行
- 历史和内存管理

### views.py

定义了整个代理系统中使用的数据模型：
- `AgentOutput`：来自 LLM 的结构化输出
- `AgentBrain`：内部状态表示
- `ActionResult`：浏览器动作的结果
- 其他支持性数据结构

### prompts.py

包含用于与 LLM 通信的提示模板：
- 系统提示
- 反思提示
- 计划提示
- 动作生成提示

### system_prompt.md

指导 LLM 如何操作的主要系统提示：
- 解释网页内容
- 生成有效的动作
- 推理任务进度
- 处理错误情况

### gif.py

提供将浏览器交互录制为 GIF 动画的功能：
- 可视化
- 调试
- 演示

### message_manager/service.py

处理代理与 LLM 之间的所有消息相关操作：
- **令牌管理**：跟踪和控制令牌使用，以保持在 LLM 上下文限制内
- **消息历史**：维护格式正确的对话历史
- **消息转换**：
  - 将浏览器状态转换为 LLM 友好的格式
  - 将操作结果处理为消息
  - 处理图像和文本内容
- **内存优化**：
  - 在接近限制时实施令牌削减策略
  - 在需要修剪时优先考虑重要内容
- **安全功能**：
  - 从消息中过滤敏感数据
  - 支持秘密的占位符替换

`MessageManager` 类处理所有消息的生命周期：
1. 使用系统提示和任务指令初始化
2. 将浏览器状态更新添加为人类消息
3. 将 LLM 输出记录为 AI 消息
4. 管理操作结果的工具消息
5. 实施智能修剪以保持在令牌限制内

## 工作原理

1. **初始化**：
   - 使用 LLM 模型和浏览器实例配置 Agent
   - 加载系统提示以指导 LLM 行为

2. **执行循环**：
   - 捕获当前浏览器状态（DOM、截图、URL）
   - 将状态格式化为 LLM 可理解的消息
   - LLM 分析页面内容并决定下一步操作
   - Agent 解释 LLM 响应并执行浏览器操作
   - 捕获结果并反馈给 LLM

3. **内存管理**：
   - 维护操作和结果的历史记录
   - 为未来决策提供上下文
   - 实现摘要以提高效率

4. **动作执行**：
   - 支持导航、点击、输入和其他浏览器操作
   - 在需要时处理错误和重试
   - 验证操作的安全性和可行性

## 使用示例

Agent 模块的典型使用方式如下：

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="搜索关于人工智能的信息并总结结果",
    llm=ChatOpenAI(model="gpt-4o"),
)

result = await agent.run()
print(result)
```

## 扩展点

agent 模块设计为可扩展的：
- 可以通过控制器注册表添加自定义操作
- 可以集成替代的 LLM 提供商
- 可以为不同的用例定制消息处理
- 可以针对特定领域优化提示工程 