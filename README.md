# FAQ知识库系统

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green)
![License](https://img.shields.io/badge/License-MIT-green)

一个基于PyQt5和SQLite的专业FAQ知识库管理系统，提供完整的Excel数据导入导出解决方案。

## 功能特性

### 核心功能
- 📁 Excel文件导入/导出（支持.xlsx格式）
- 🔍 多条件组合查询与关键字搜索
- ✏️ FAQ条目增删改查（CRUD）操作
- 🔄 数据自动保存与恢复

### 高级功能
- 🖥️ 响应式GUI界面
- 📊 数据统计与报表生成
- ⚙️ 用户偏好设置保存
- 📤 数据批量导出功能

## 环境要求
- Python 3.13+
- Windows 10/11 或 Linux with X11
- 内存：最低512MB，推荐1GB
- 磁盘空间：100MB可用空间

## 安装指南

### 从源码运行
```bash
# 克隆仓库
git clone https://github.com/bjkdgh/faq-system.git
cd faq-system

# 创建虚拟环境（推荐）
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/MacOS

# 安装依赖
pip install -r requirements.txt

# 运行程序
python src/faq_system.py
```

### 使用打包版本
1. 从[Release页面](https://github.com/bjkdgh/faq-system/releases)下载最新版本
2. 解压zip文件
3. 双击运行faq_system.exe

## 使用说明
1. 首次运行会自动创建数据库
2. 通过菜单栏"文件"→"导入"加载Excel数据
3. 使用搜索框快速查找FAQ条目
4. 右键点击条目进行编辑/删除操作

![界面截图](docs/screenshot.png)

## 开发指南
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 打包程序
pyinstaller --clean faq_system.spec
```

## 贡献说明
欢迎通过Issue和Pull Request参与贡献：
1. Fork本项目
2. 创建特性分支（git checkout -b feature/xxx）
3. 提交修改（git commit -am 'Add some feature'）
4. 推送分支（git push origin feature/xxx）
5. 创建Pull Request

## 文档资源
- [技术架构说明](技术手册.md)
- [系统维护指南](维护手册.md)
- [API接口文档](docs/api.md)

## 开源协议
本项目采用 [MIT License](LICENSE) 授权
