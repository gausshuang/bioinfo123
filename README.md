# 生物信息数据库导航 - NAR 2025

## 🧬 项目简介

这是一个专业的生物信息资源导航页面，收录了NAR 2024-2025中的804个重要生物信息资源。页面提供了直观的分类浏览、类型筛选、智能搜索、中英文对照等功能，帮助研究人员快速找到所需的生物信息资源。

## ✨ 主要特性

- 📊 **804个资源**: 包含475个数据库和329个Web工具，涵盖8个生物学领域
- 🔍 **智能搜索**: 支持资源名称和描述的实时搜索
- 🏷️ **双重筛选**: 按生物学领域分类 + 按资源类型筛选
- 🌐 **中英对照**: 英文描述配中文翻译，鼠标悬停显示
- 📱 **响应式设计**: 完美适配桌面端和移动端
- ❤️ **收藏功能**: 可收藏常用资源
- 🎨 **现代UI**: 参考学术网站设计，专业美观

## 🗂️ 资源分类

- **生物信息工具** (210个) - 数据库126个, Web工具84个
- **基因组学** (195个) - 数据库105个, Web工具90个
- **蛋白质** (163个) - 数据库55个, Web工具108个
- **医学生物学** (105个) - 数据库83个, Web工具22个
- **组学** (63个) - 数据库48个, Web工具15个
- **微生物学** (33个) - 数据库25个, Web工具8个
- **植物生物学** (22个) - 数据库22个, Web工具0个
- **进化生物学** (13个) - 数据库11个, Web工具2个

## 🚀 在线访问

GitHub Pages: [https://your-username.github.io/gitPages20250820](https://your-username.github.io/gitPages20250820)

## 💻 本地部署

### 方法1: 直接打开
```bash
# 克隆仓库
git clone https://github.com/your-username/gitPages20250820.git
cd gitPages20250820

# 直接在浏览器中打开 index.html
```

### 方法2: HTTP服务器
```bash
# Python 3
python -m http.server 8000

# 或者 Python 2
python -m SimpleHTTPServer 8000

# 然后访问 http://localhost:8000
```

## 📁 文件结构

```
gitPages20250820/
├── index.html                 # 主页面文件
├── databases_processed.json   # 数据库数据文件
├── read_excel.py             # Excel数据读取脚本
├── categorize_databases.py   # 数据分类处理脚本
├── nar2025databases.xlsx     # 原始Excel数据
├── log.md                    # 开发日志
└── README.md                 # 项目说明
```

## 🛠️ 技术栈

- **前端**: HTML5 + CSS3 + JavaScript (ES6+)
- **图标**: FontAwesome 6.4.0
- **数据处理**: Python + Pandas + OpenPyXL
- **部署**: GitHub Pages

## 🎯 核心功能

### 1. 智能搜索
- 实时搜索数据库名称和描述
- 支持中英文关键词搜索
- 防抖优化，提升用户体验

### 2. 分类筛选
- 8个生物学领域分类
- 动态显示各分类数量
- 一键切换查看不同领域

### 3. 多语言支持
- 英文描述配中文翻译
- 鼠标悬停显示中文提示
- 支持中英文搜索

### 4. 现代化界面
- 卡片式设计，信息层次清晰
- 悬停动效，交互体验佳
- 响应式布局，适配多设备

## 📊 数据来源

数据来源于NAR (Nucleic Acids Research) 2024-2025年数据库特刊，包含503个精选的生物信息资源（276个数据库 + 227个Web工具）。

## 🔧 开发说明

如需修改数据或添加新数据库：

1. 编辑 `nar2025databases.xlsx` 文件
2. 运行 `python read_excel.py` 读取数据
3. 运行 `python categorize_databases.py` 处理分类
4. 页面将自动加载新数据

## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📧 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
